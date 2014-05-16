from django.conf.urls import patterns, url
from pmm_is2.apps.adm import views


urlpatterns = patterns('',

        url(r'^register/$', views.register, name='register'),
        url(r'^$', views.index, name='index'),
        url(r'^index2', views.index2, name='index2'),
        url(r'^profile/$', views.profile, name='profile'),
        url(r'^user_list/$', views.user_list, name='user_list'),
        url(r'^usuarios/$', views.usuarios, name='usuarios'),
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
        url(r'^suggest_proyecto/$', views.suggest_proyecto, name='suggest_proyecto'),
        url(r'^perfil/(?P<pk>\d+)$', views.perfil, name='perfil'),
        url(r'^rol/(?P<pk>\d+)$', views.rol, name='rol'),
        url(r'^project_profile/(?P<pk>\d+)$', views.project_profile, name='project_profile'),
        url(r'^permiso/(?P<pk>\d+)$', views.permiso, name='permiso'),
        url(r'^project_list/$', views.project_list, name='project_list'),
        url(r'^project_import_list/$', views.project_import_list, name='project_import_list'),
        url(r'^project_update/(?P<pk>\d+)$', views.project_update, name='project_update'),

        url(r'^project_delete/(?P<pk>\d+)$', views.project_delete, name='project_delete'),
        url(r'^phase_create/(?P<pk>\d+)$', views.phase_create, name='phase_create'),
        url(r'^phases_list/(?P<pk>\d+)$', views.phases_list, name='phases_list'),
        url(r'^phase_update/(?P<pk>\d+)$', views.phase_update, name='phase_update'),
        url(r'^phase_delete/(?P<pk>\d+)$', views.phase_delete, name='phase_delete'),
        url(r'^comite_create/$', views.comite_create, name='comite_create'),
        url(r'^comite_edit/(?P<pk>\d+)$', views.comite_update, name='comite_edit'),
        url(r'^comite_list/$', views.comite_list, name='comite_list'),
        #imports
        url(r'^import_project/(?P<pk>\d+)$', views.import_project, name='import_project'),

)