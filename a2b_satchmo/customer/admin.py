from django.contrib import admin
from a2b_satchmo.customer.forms import *
from a2b_satchmo.customer.models import *
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
    
    list_display = ('id', 'username', 'useralias','lastname','id_group','ba','tariff','status','language')
    list_display_links = ('id', 'username',)    
    search_fields = ('useralias', 'username')
    ordering = ('id',)
    list_filter = ['status','id_group','language']
    readonly_fields = ('username','credit','firstusedate')

admin.site.register(Card, CardAdmin)

class CallAdmin(admin.ModelAdmin):
    list_display = ('starttime','card_id', 'src', 'calledstation',  'sessiontime', 'real_sessiontime','terminatecauseid')
    list_display_links = []
    list_filter = ['starttime', 'calledstation']
    search_fields = ('card_id', 'dst', 'src','starttime',)
    ordering = ('-id',)
    change_list_template = 'admin/customer/call/change_list.html'

    def get_urls(self):
        urls = super(CallAdmin, self).get_urls()
        my_urls = patterns('',(r'^admin/customer/call/$', self.admin_site.admin_view(self.changelist_view))
        )
        return my_urls + urls


    def queryset(self, request):
        kwargs = {}
        if request.method == 'POST':
            phone_no = variable_value(request,'phone_no')
            phone_no_type = variable_value(request,'phone_no_type')

            if "fromday_chk" in request.POST:
                fromday_chk     = 'on'
                from_day        = int(request.POST['from_day'])
                from_month_year = request.POST['from_month_year']
                from_year       = int(request.POST['from_month_year'][0:4])
                from_month      = int(request.POST['from_month_year'][5:7])
                from_day        = validate_days(from_year,from_month,from_day)
                start_date      = datetime(from_year,from_month,from_day)
            else:
                fromday_chk     = ''
                from_day        = ''
                from_month_year = ''
                from_year       = ''
                from_month      = ''
                from_day        = ''
                start_date      = ''

            if "today_chk" in request.POST:
                today_chk       = 'on'
                to_day          = int(request.POST['to_day'])
                to_month_year   = request.POST['to_month_year']
                to_year         = int(request.POST['to_month_year'][0:4])
                to_month        = int(request.POST['to_month_year'][5:7])
                to_day          = validate_days(to_year,to_month,to_day)
                end_date        = datetime(to_year,to_month,to_day)
            else:
                today_chk       = ''
                to_day          = ''
                to_month_year   = ''
                to_year         = ''
                to_month        = ''
                to_day          = ''
                end_date        = ''

            call_type = variable_value(request,'call_type')
            show = variable_value(request,'show')
            result = variable_value(request,'result')
            currency = variable_value(request,'currency')

            if fromday_chk == 'on' and today_chk == 'on':
                kwargs[ 'starttime__range' ] = (start_date, end_date)
            if fromday_chk == 'on' and today_chk != 'on' :
                kwargs[ 'starttime__gte' ] = start_date
            if today_chk == 'on' and fromday_chk != 'on':
                kwargs[ 'starttime__lte' ] = end_date

            calledstation = source_desti_field_chk(phone_no,phone_no_type,'calledstation')
            for i in calledstation:
                kwargs[i] = calledstation[i]

            if call_type != '' and call_type != '-1':
                calltype_list = call_type_list()
                for i in calltype_list:
                    if int(i[0]) == int(call_type) :
                        kwargs[ 'sipiax' ] = call_type

            if show == 'ANSWER':
                kwargs[ 'terminatecauseid__exact' ] = '1'
            if show == 'ALL':
                dlist = dial_status_list()
                kwargs[ 'terminatecauseid__in' ] = (l[0]  for l in dlist)

            form = SearchForm(initial={'fromday_chk':fromday_chk,'from_day':from_day,'from_month_year':from_month_year,'today_chk':today_chk,'to_day':to_day,'to_month_year':to_month_year,'phone_no':phone_no,'phone_no_type':phone_no_type,'call_type':call_type,'currency':currency,'show':show,'result':result})

            if len(kwargs) == 0:
                form = SearchForm(initial={'currency': config_value('base_currency').upper(),'phone_no_type':1,'show':'ANSWER','result':'min'})
                tday = datetime.today()
                result = 'min'
                kwargs[ 'starttime__gte' ] = datetime(tday.year, tday.month, tday.day)
                currency = config_value('base_currency').upper()

            #return super(CallAdmin, self).get_query_set().filter(**kwargs)
            return Call.objects.filter(**kwargs)
        else:            
            return Call.objects.all()
        



    def changelist_view(self, request, extra_context=None):
        from django.contrib.admin.views.main import ChangeList
        cl = ChangeList(request, self.model, list(self.list_display),
                        self.list_display_links, self.list_filter,
                        self.date_hierarchy, self.search_fields,
                        self.list_select_related,
                        self.list_per_page,
                        self.list_editable,                        
                        self)
        cl.formset = None
               
        if request.method == 'POST':
            
            phone_no = variable_value(request,'phone_no')
            phone_no_type = variable_value(request,'phone_no_type')

            if "fromday_chk" in request.POST:
                fromday_chk     = 'on'
                from_day        = int(request.POST['from_day'])
                from_month_year = request.POST['from_month_year']
                from_year       = int(request.POST['from_month_year'][0:4])
                from_month      = int(request.POST['from_month_year'][5:7])
                from_day        = validate_days(from_year,from_month,from_day)
                start_date      = datetime(from_year,from_month,from_day)
            else:
                fromday_chk     = ''
                from_day        = ''
                from_month_year = ''
                from_year       = ''
                from_month      = ''
                from_day        = ''
                start_date      = ''

            if "today_chk" in request.POST:
                today_chk       = 'on'
                to_day          = int(request.POST['to_day'])
                to_month_year   = request.POST['to_month_year']
                to_year         = int(request.POST['to_month_year'][0:4])
                to_month        = int(request.POST['to_month_year'][5:7])
                to_day          = validate_days(to_year,to_month,to_day)
                end_date        = datetime(to_year,to_month,to_day)
            else:
                today_chk       = ''
                to_day          = ''
                to_month_year   = ''
                to_year         = ''
                to_month        = ''
                to_day          = ''
                end_date        = ''

            call_type = variable_value(request,'call_type')
            show = variable_value(request,'show')
            result = variable_value(request,'result')
            currency = variable_value(request,'currency')
            calledstation = source_desti_field_chk(phone_no,phone_no_type,'calledstation')

            if call_type != '' and call_type != '-1':
                calltype_list = call_type_list()
                
            form = SearchForm(initial={'fromday_chk':fromday_chk,'from_day':from_day,'from_month_year':from_month_year,'today_chk':today_chk,'to_day':to_day,'to_month_year':to_month_year,'phone_no':phone_no,'phone_no_type':phone_no_type,'call_type':call_type,'currency':currency,'show':show,'result':result})                    
            tday = datetime.today()
            result = 'min'
            currency = config_value('base_currency').upper()
                                   
        else:
            form = SearchForm(initial={'currency': config_value('base_currency').upper(),'phone_no_type':1,'show':'ANSWER','result':'min'})
            #cl.result_list = cl.get_query_set()#cl.result_list #.filter(card_id='55')

        #print cl.result_list
        ctx = {
            'form': form,            
            'cl': cl,
        }
        return super(CallAdmin, self).changelist_view(request, extra_context=ctx)


admin.site.register(Call, CallAdmin)




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

