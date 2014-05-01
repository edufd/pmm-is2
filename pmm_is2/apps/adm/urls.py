from django.conf.urls import patterns, url
from pmm_is2.apps.adm import views


urlpatterns = patterns('',

        url(r'^register/$', views.register, name='register'),
        url(r'^$', views.index, name='index'),
        url(r'^profile/$', views.profile, name='profile'),
        url(r'^user_list/$', views.user_list, name='user_list'),
        url(r'^usuario/$', views.usuario, name='usuario'),
        url(r'^roles/$', views.roles, name='roles'),
        url(r'^permisos/$', views.permisos, name='permisos'),
        url(r'^proyectos/$', views.proyectos, name='proyectos'),
        url(r'^user_edit/(?P<pk>\d+)$', views.user_update, name='user_edit'),
        url(r'^user_delete/(?P<pk>\d+)$', views.user_delete, name='user_delete'),
        url(r'^group_create/$', views.group_create, name='group_create'),
        url(r'^project_create/$', views.project_create, name='project_create'),
        url(r'^group_list/$', views.group_list, name='group_list'),
        url(r'^group_edit/(?P<pk>\d+)$', views.group_update, name='group_edit'),
        url(r'^group_delete/(?P<pk>\d+)$', views.group_delete, name='group_delete'),
        url(r'^suggest_category/$', views.suggest_category, name='suggest_category'),
        url(r'^suggest_rol/$', views.suggest_rol, name='suggest_rol'),
        url(r'^suggest_permiso/$', views.suggest_permiso, name='suggest_rol'),
        url(r'^perfil/(?P<pk>\d+)$', views.perfil, name='perfil'),
        url(r'^rol/(?P<pk>\d+)$', views.rol, name='rol'),
        url(r'^permiso/(?P<pk>\d+)$', views.permiso, name='permiso'),
        url(r'^project_list/$', views.project_list, name='project_list'),
        url(r'^fase_create/(?P<pk>\d+)$', views.fase_create, name='fase_create'),
        url(r'^comite_create/$', views.comite_create, name='comite_create'),

        url(r'^comite_edit/(?P<pk>\d+)$', views.comite_update, name='comite_edit'),
        url(r'^comite_list/$', views.comite_list, name='comite_list'),

)