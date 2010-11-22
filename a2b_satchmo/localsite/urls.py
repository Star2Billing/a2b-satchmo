from django.conf.urls.defaults import *
#from satchmo_store.accounts.views import register

urlpatterns += patterns('',url(r'^shop_terms/$', 'a2b_satchmo.localsite.views.shop_terms', name="shop_terms"),
                       )
"""
urlpatterns = patterns('',
    (r'example/', 'a2b_satchmo.localsite.views.example', {}),
)
"""