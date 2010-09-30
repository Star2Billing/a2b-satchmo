import os
from a2b_satchmo.customer.views import *
from a2b_satchmo.customer.forms import *
from a2b_satchmo.customer.models import Language

from django.conf import settings
from django.conf.urls.defaults import *
from satchmo_store.urls import urlpatterns
from satchmo_utils.urlhelper import replace_urlpattern
from product.models import Product

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

product_list = Product.objects.filter(featured=True)

replacement = url(r'^quick_order/$', 'satchmo_store.shop.views.cart.add_multiple',
            {'products': product_list}, 'satchmo_quick_order')
replace_urlpattern(urlpatterns, replacement)

urlpatterns += patterns('',
    # redirect
    #('^$', 'django.views.generic.simple.redirect_to', {'url': 'accounts/login/'}),
    #(r'^/', include('a2b_satchmo.urls')),
    (r'^resources/(?P<path>.*)$',  'django.views.static.serve',{ 'document_root': settings.MEDIA_ROOT } ),

    url(r'^admin_tools/', include('admin_tools.urls')),
    (r'^grappelli/', include('grappelli.urls')),

    #To set the correct paypal notify_url
    (r'^checkout_ipn_process/', include('paypal.standard.ipn.urls')),

    (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    (r'^admin/language/$', 'a2b_satchmo.customer.views.my_admin_language_view'),
    (r'^admin/card/$', 'a2b_satchmo.customer.views.my_admin_card_view'),
    (r'^admin/cdr/$', 'a2b_satchmo.customer.views.my_admin_cdr_view'),
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



