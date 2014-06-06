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

        url(r'^crear_atributo_tipo_item/$', views.crear_atributo_tipo_item, name='crear_atributo_tipo_item'),
        url(r'^listar_atributo_tipo_item/$', views.listar_atributo_tipo_item, name='listar_atributo_tipo_item'),
        url(r'^editar_atributo_tipo_item/(?P<pk>\d+)$', views.editar_atributo_tipo_item, name='editar_atributo_tipo_item'),
        url(r'^eliminar_atributo_tipo_item/(?P<pk>\d+)$', views.eliminar_atributo_tipo_item, name='eliminar_atributo_tipo_item'),
        url(r'^atributo_tipo_item/(?P<pk>\d+)$', views.ver_atributo_tipo_item, name='atributo_tipo_item'),

        #agregado para probar mi parte
        url(r'^crear_item/(?P<pk>\d+)$', views.crear_item, name='crear_item'),
        url(r'^listar_item/$', views.listar_item, name='listar_item'),
        url(r'^lista_item_revivir/(?P<id_fase>\d+)$', views.lista_item_revivir, name='lista_item_revivir'),
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
        url(r'^revivir_item/(?P<pk>\d+)$', views.revivir_item, name='revivir_item'),
        url(r'^item_reversion/(?P<pk>\d+)$', views.item_reversion, name='item_reversion'),
        url(r'^item_reversion_list/(?P<pk>\d+)$', views.item_reversion_list, name='item_reversion_list'),
        url(r'^revivir/(?P<pk>\d+)$', views.revivir, name='revivir'),
        url(r'^agregar_relaciones/(?P<id_fase>\d+)$', views.agregar_relaciones, name='agregar_relaciones'),
        url(r'^relation_fix/(?P<item_id>\d+)$', views.relation_fix, name='relation_fix'),
        url(r'^relation_fix_revive/(?P<item_id>(\d+))/(?P<item_id_sucesor>(\d+))/$', views.relation_fix_revive, name='relation_fix_revive'),
        url(r'^listar_relaciones/(?P<id_fase>(\d+))/$', views.listar_relaciones, name='listar_relaciones'),
        url(r'^eliminar_relacion/(?P<pk>\d+)$', views.eliminar_relacion, name='eliminar_relacion'),
        url(r'^project_profile/(?P<pk>\d+)$', views.project_profile, name='project_profile'),
        url(r'^phase_item_list/(?P<id_proyecto>(\d+))/(?P<id_fase>(\d+))/$', views.phase_item_list, name='phase_item_list'),

        #imports
        url(r'^import_item/(?P<pk>\d+)$', views.import_item, name='import_item'),
        url(r'^item_import_list/(?P<pk>\d+)$', views.item_import_list, name='item_import_list'),
        url(r'^calcular/(?P<pk>\d+)$', views.calcular_impacto_y_costo_item, name='calcular'),
        url(r'^calcular_costo_total/(?P<pk>\d+)$', views.calcular_costo_total, name='calcular_costo_total'),


        #url(r'^crear_solicitud/$', views.crear_solicitud, name='crear_solicitud'),
        #url(r'^listar_solicitud/$', views.listar_solicitud, name='listar_solicitud'),
        #url(r'^editar_solicitud/(?P<pk>\d+)$', views.editar_solicitud, name='editar_solicitud'),
        url(r'^crear_solicitud/(?P<id_proyecto>(\d+))/(?P<id_fase>(\d+))/$', views.crear_solicitud, name='crear_solicitud'),
        url(r'^listar_solicitud/(?P<id_proyecto>(\d+))/(?P<id_fase>(\d+))/$', views.listar_solicitud, name='listar_solicitud'),

        url(r'^imprimir_solicitud/(?P<pk>\d+)$', views.imprimir_solicitud, name='imprimir_solicitud'),
        url(r'^enviar_solicitud/(?P<pk>\d+)$', views.enviar_solicitud, name='enviar_solicitud'),
        url(r'^listar_solicitudRecibido/$', views.listar_solicitudRecibido, name='listar_solicitudRecibido'),
        url(r'^editar_solicitudRecibido/(?P<pk>\d+)$', views.editar_solicitudRecibido, name='editar_solicitudRecibido'),

)