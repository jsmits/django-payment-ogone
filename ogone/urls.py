from django.conf.urls.defaults import *

urlpatterns = patterns('ogone.views',
    url(r'^test/', 'test_form3'),
    url(r'^ogone/$', 'ogone'),
    
    url(r'^status/$', 'order_status_update'),
    
    url(r'^accepted/', 'order_status_update'),
    url(r'^declined/', 'order_status_update'),
    url(r'^exception/', 'order_status_update'),
    url(r'^cancelled/', 'order_status_update'),
    
    url(r'^to_ogone/$', 'to_ogone'),
)