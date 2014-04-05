__author__ = 'eduardo'
from django.conf.urls import patterns, url
from adm import views

urlpatterns = patterns('',
        url(r'^$', views.index, name='index'),
        url(r'^register/$', views.register, name='register'),
        )