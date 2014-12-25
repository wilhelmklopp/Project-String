from django.conf.urls import patterns, url

from pstring import views

urlpatterns = patterns('',
    # 
    url(r'^$', views.index, name='index'),
    # 
    #url(r'^(?P<short>[-bcdfghjkmnpqrstvwxyzBCDFGHJKMNPQRSTVWXY3456789]+)/$', views.resolve_landing, name='resolve_landing'),
)
