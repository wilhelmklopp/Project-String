from django.conf.urls import patterns, url

from pstring import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    )
