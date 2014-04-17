from django.conf.urls import patterns, url

from pmm_is2.apps.adm import views


urlpatterns = patterns('',

        url(r'^register/$', views.register, name='register'),
        url(r'^restricted/$', views.restricted, name='restricted'),

        url(r'^profile/$', views.profile, name='profile'),
        url(r'^user_list/$', views.user_list, name='user_list'),
        url(r'^edit/(?P<pk>\d+)$', views.user_update, name='user_edit'),
        url(r'^delete/(?P<pk>\d+)$', views.user_delete, name='user_delete'),
)