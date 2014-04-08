__author__ = 'eduardo'
from django.conf.urls import patterns, url
from adm import views

urlpatterns = patterns('',
        url(r'^$', views.index, name='index'),
        url(r'^home/$', views.home, name='home'),
        url(r'^register/$', views.register, name='register'),
        url(r'^login/$', views.user_login, name='user_login'),
        url(r'^restricted/$', views.restricted, name='restricted'),
        url(r'^logout/$', views.user_logout, name='logout'),
        url(r'^profile/$', views.profile, name='profile'),
        url(r'^user_list/$', views.user_list, name='user_list'),
        url(r'^edit/(?P<pk>\d+)$', views.user_update, name='user_edit'),
        url(r'^delete/(?P<pk>\d+)$', views.user_delete, name='user_delete'),
)