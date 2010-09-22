from django.conf.urls.defaults import *


urlpatterns = patterns('',
    (r'example/', 'a2b_satchmo.localsite.views.example', {}),
)
