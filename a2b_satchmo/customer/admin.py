from django.contrib import admin
from django.forms import ModelForm, Textarea, TextInput
from a2b_satchmo.customer.forms import *
from a2b_satchmo.customer.models import *
from a2b_satchmo.customer.function_def import *
#from django.contrib.sites.models import Site
#from django.contrib.admin.views.main import ChangeList
from satchmo_store.shop.models import Order, OrderItem
from satchmo_store.shop.admin import OrderOptions
from django.views.decorators.cache import never_cache
from django.conf.urls.defaults import *
from datetime import *

# Language
class LanguageAdmin(admin.ModelAdmin):
    list_display = ('name','lname','charset')
    list_display_links = ('name',)
    #list_editable = ('code','charset')
    list_filter = ['charset']
    
admin.site.register(Language, LanguageAdmin)


class TrunkAdmin(admin.ModelAdmin):
    list_display = ('id_trunk', 'trunkcode', 'trunkprefix','providertech','providerip')
    list_display_links = ('id_trunk', 'trunkcode',) 

admin.site.register(Trunk, TrunkAdmin)


class AlarmAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'periode','type')
    list_display_links = ('id', 'name',) 

admin.site.register(Alarm, AlarmAdmin)



class CardAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            
            'fields': ('username', 'useralias','uipass','credit','id_group', 'serial','lastname','firstname',
                       'email','address','city','state','country','zipcode','phone','fax','company_name',
                       'company_website','typepaid','tariff','id_didgroup','id_timezone','currency','language',
                       'status','simultaccess','runservice','creditlimit','credit_notification','notify_email',
                       'email_notification','id_campaign','firstusedate','enableexpire','expirationdate',
                       'expiredays','sip_buddy','iax_buddy','mac_addr','inuse','autorefill','initialbalance',
                       'invoiceday','vat','vat_rn','discount','traffic','traffic_target','restriction')            
        }),
    )
    
    list_display = ('id', 'username', 'useralias','lastname','id_group','ba','tariff','status','language','action')
    search_fields = ('useralias', 'username')
    ordering = ('id',)
    list_filter = ['status','id_group','language']
    readonly_fields = ('username','credit','firstusedate')    
    
    def __init__(self, *args, **kwargs):
        super(CardAdmin, self).__init__(*args, **kwargs)
        self.list_display_links = ('username', )
    """
    def my_view(self,request):
        cxt = {
            'app_label': '',
        }
        #return super(CardAdmin, self).my_view(request, card_id)
        return render_to_response('admin/view/detail_view.html' , cxt, RequestContext(request))
    
    def get_urls(self):
        urls = super(CardAdmin, self).get_urls()
        my_urls = patterns('',url(r'^admin/view/$', self.admin_site.admin_view(self.my_view)),
        #(r'^admin/view/(?P<card_id>\d+)/$', 'a2b_satchmo.customer.admin_views.card_view_detail'),
        )
        return my_urls + urls        
    """
    def action(self,form):
        opts = self.model._meta
        app_label = opts.app_label
        return '<a href=\"/admin/%s/view/%d/\">view</a>' % (opts.object_name.lower(),form.id)
    action.allow_tags = True

admin.site.register(Card, CardAdmin)

class CallAdmin(admin.ModelAdmin):
    list_display = ('starttime','src','dnid','calledstation','destination_name' ,'card_id','id_trunk','buy','call_charge','duration','terminatecauseid','sipiax')
    list_filter = ['starttime', 'calledstation']
    #search_fields = ('card_id', 'dst', 'src','starttime',)
    date_hierarchy = ('starttime')
    ordering = ('-id',)    
    change_list_template = 'admin/customer/call/change_list.html'    
    
    def __init__(self, *args, **kwargs):
        super(CallAdmin, self).__init__(*args, **kwargs)
        self.list_display_links = (None, )
    
    def get_urls(self):
        urls = super(CallAdmin, self).get_urls()
        my_urls = patterns('',(r'^admin/customer/call/$', self.admin_site.admin_view(self.changelist_view)),                             
        )        
        return my_urls + urls
        
    def queryset(self, request):
        kwargs = {}
        kwargs = call_record_common_fun(request,form_require="no")        
        qs = super(CallAdmin, self).queryset(request)
        return qs.select_related('prefix__destination', 'destination').filter(**kwargs).order_by('-starttime')
    
    def changelist_view(self, request,  extra_context=None):        
        if request.method == 'POST':            
            form = call_record_common_fun(request,form_require="yes")                                               
        else:
            #result = 'min'
            form = SearchForm(initial={'currency': config_value('base_currency').upper(),'phone_no_type':1,'show':0,'result':'min'})                
        ctx = {
            'form': form,            
            'has_add_permission': '',
        }
        return super(CallAdmin, self).changelist_view(request,  extra_context=ctx)
admin.site.register(Call, CallAdmin)

#Config Group List
class ConfigGroupAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {

            'fields': ('group_title','group_description'),
        }),
    )
    list_display = ('group_title','group_description')
    search_fields = ('group_title', 'group_description')    
    ordering = ('id',)

admin.site.register(ConfigGroup, ConfigGroupAdmin)

#Admin side Config Model
class ConfigAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('config_group_title','config_title','config_key','config_value','config_description',),
        }),
    )    
    form = ConfigForm    
    list_display = ('config_title','config_key','config_value','config_description','config_group_title',)
    search_fields = ('config_title', 'config_key','config_description')
    #readonly_fields = ('config_title','config_key','config_description',)
    list_filter = ['config_group_title']
    ordering = ('config_group_title',)
    #formfield_overrides = {
    #    models.CharField: {'widget': TextInput(attrs={'readonly':'readonly',})},
    #    models.TextField: {'widget': Textarea(attrs={'readonly':'readonly',})},
    #}

admin.site.register(Config, ConfigAdmin)

class OrderExtend:
    def order_sku(self):
        allsku = ''
        for item in self.orderitem_set.all():
            allsku += "%s<br />" % item.product.sku
        return allsku
    order_sku.allow_tags = True
    order_sku.short_description = "Order SKUs"

Order.__bases__ += (OrderExtend,)

admin.site.unregister(Order)

class CustomOrderAdmin(OrderOptions):
    list_display = ('id', 'order_sku', 'contact', 'time_stamp',
                    'order_total', 'balance_forward', 'status',
                    'invoice', 'packingslip')

admin.site.register(Order, CustomOrderAdmin)

