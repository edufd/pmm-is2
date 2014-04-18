from django.conf.urls import patterns, url
from pmm_is2.apps.adm import views


urlpatterns = patterns('',

        url(r'^register/$', views.register, name='register'),
        url(r'^$', views.index, name='index'),
        url(r'^profile/$', views.profile, name='profile'),
        url(r'^user_list/$', views.user_list, name='user_list'),
        url(r'^usuario/$', views.usuario, name='usuario'),
        url(r'^user_edit/(?P<pk>\d+)$', views.user_update, name='user_edit'),
        url(r'^user_delete/(?P<pk>\d+)$', views.user_delete, name='user_delete'),
        url(r'^group_create/$', views.group_create, name='group_create'),
        url(r'^group_list/$', views.group_list, name='group_list'),
        url(r'^group_edit/(?P<pk>\d+)$', views.group_update, name='group_edit'),
        url(r'^group_delete/(?P<pk>\d+)$', views.group_delete, name='group_delete'),
        url(r'^asignar_roles/$', views.asignar_roles, name='asignar_roles'),
        url(r'^asignar/(?P<pk>\d+)$', views.asignar, name='asignar'),
)