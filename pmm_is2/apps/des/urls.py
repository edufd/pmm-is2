from django.conf.urls import patterns, url
from pmm_is2.apps.des import views

__author__ = 'Eduardo'
urlpatterns = patterns('',

        url(r'^$', views.index, name='index'),
        url(r'^crear_tipo_item/$', views.crear_tipo_item, name='crear_tipo_item'),
        url(r'^listar_tipo_item/$', views.listar_tipo_item, name='listar_tipo_item'),
        url(r'^editar_tipo_item/(?P<pk>\d+)$', views.editar_tipo_item, name='editar_tipo_item'),
        url(r'^eliminar_tipo_item/(?P<pk>\d+)$', views.eliminar_tipo_item, name='eliminar_tipo_item'),
        url(r'^tipo_item/(?P<pk>\d+)$', views.ver_tipo_item, name='tipo_item'),
        url(r'^suggest_tipo_item/$', views.suggest_tipo_item, name='suggest_tipo_item'),

        #agregado para probar mi parte
        url(r'^crear_item/(?P<pk>\d+)$', views.crear_item, name='crear_item'),
        url(r'^listar_item/$', views.listar_item, name='listar_item'),
        url(r'^editar_item/(?P<pk>\d+)$', views.editar_item, name='editar_item'),
        url(r'^eliminar_item/(?P<pk>\d+)$', views.eliminar_item, name='eliminar_item'),
        url(r'^item/(?P<pk>\d+)$', views.ver_item, name='item'),
        url(r'^suggest_tipo_item/$', views.suggest_tipo_item, name='suggest_tipo_item'),
        url(r'^suggest_item/$', views.suggest_item, name='suggest_item'),
        url(r'^adjuntarArchivo_item/(?P<pk>\d+)$', views.archivoadjunto_page, name='adjuntarArchivo_item'),

        url(r'^crear_archivoAdjunto/$', views.crear_archivoAdjunto, name='crear_archivoAdjunto'),

        url(r'^desasignar/(?P<pk>\d+)$', views.desasignar, name='desasignar'),
        url(r'^eliminar_adjunto/(?P<pk>\d+)$', views.eliminar_adjunto, name='eliminar_adjunto'),

        url(r'^project_list/$', views.project_list, name='project_list'),
        url(r'^phases_list/(?P<pk>\d+)$', views.phases_list, name='phases_list'),
        url(r'^historial_item/(?P<pk>\d+)$', views.historial_item, name='historial_item'),
        url(r'^agregar_relaciones/$', views.agregar_relaciones, name='agregar_relaciones'),
)