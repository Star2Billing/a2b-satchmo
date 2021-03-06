import os
from a2b_satchmo.customer.views import *
from a2b_satchmo.customer.forms import *
from a2b_satchmo.customer.models import Language

from django.conf import settings
from django.conf.urls.defaults import *
#from django.contrib import databrowse

#from django.contrib.billing.urls import urlpatterns as billingpattern
from satchmo_store.urls import urlpatterns 
from satchmo_utils.urlhelper import replace_urlpattern
from product.models import Product

#import django_cron
#django_cron.autodiscover()

# Uncomment the next two lines to enable the admin:
from django.contrib import admin 
admin.autodiscover()

product_list = Product.objects.filter(featured=True)

replacement = url(r'^quick_order/$', 'satchmo_store.shop.views.cart.add_multiple', {'products': product_list}, 'satchmo_quick_order')
replace_urlpattern(urlpatterns, replacement)

#replacement = url(r'^accounts/register/$', 'from satchmo_store.accounts.views.register',{'form_class': 'UserRegistrationForm'}, 'registration_register')
#replace_urlpattern(urlpatterns, replacement)

#urlpatterns += billingpattern

urlpatterns += patterns('',
    # redirect
    #('^$', 'django.views.generic.simple.redirect_to', {'url': 'shop/'}),
    #(r'^/', include('a2b_satchmo.urls')),
    (r'^resources/(?P<path>.*)$',  'django.views.static.serve',{ 'document_root': settings.MEDIA_ROOT } ),    
    url(r'^admin_tools/', include('admin_tools.urls')),
    (r'^grappelli/', include('grappelli.urls')),
    #(r'^databrowse/(.*)', databrowse.site.root),
    #To set the correct paypal notify_url
    (r'^checkout_ipn_process/', include('paypal.standard.ipn.urls')),

    (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    (r'^admin/language/$', 'a2b_satchmo.customer.admin_views.my_admin_language_view'),
    (r'^admin/card/$', 'a2b_satchmo.customer.admin_views.my_admin_card_view'),
    (r'^admin/cdr/$', 'a2b_satchmo.customer.admin_views.my_admin_cdr_view'),    
    (r'^admin/', include(admin.site.urls)),
    (r'^api/', include('a2b_satchmo.api.urls')),
)


urlpatterns += patterns('a2b_satchmo.customer.views',
    #(r'^$', 'index_view'),
    (r'^login/$', 'check_login'),
    (r'^logout/$', 'logout_view'),
    (r'^profile/$', 'profile_view'),
    (r'^cdr/$', 'call_detail'),
    (r'^checkout_payment/$', 'checkout_payment'),
    (r'^checkout_confirmation/$', 'checkout_confirmation'),
    (r'^checkout_process/$', 'checkout_process'),
    # Jqgrid
    url (r'^examplegrid/$', grid_handler, name='grid_handler'),
    url (r'^examplegrid/cfg/$', grid_config, name='grid_config'),   
)

urlpatterns += patterns('a2b_satchmo.localsite.views',
    url(r'^make_call/$', 'make_call',{},'make_call'),
    url(r'^invoice/(?P<order_id>\d+)/$', 'invoice',{},'invoice'),
    url(r'^print/(?P<id>\d+)', 'invoice_print', {}, 'invoice_print'),   
)



