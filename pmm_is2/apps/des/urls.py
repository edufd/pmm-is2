from django.conf.urls import patterns, url
from pmm_is2.apps.des import views

__author__ = 'Eduardo'
urlpatterns = patterns('',

        url(r'^$', views.index, name='index'),


)