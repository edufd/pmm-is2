__author__ = 'VICTOR'
from django.conf.urls import patterns, url
from pmm_is2.apps.gdc import views

urlpatterns = patterns('',

        url(r'^$', views.index, name='index'),
        url(r'^crear_solicitud/$', views.crear_solicitud, name='crear_solicitud'),
        url(r'^listar_solicitud/$', views.listar_solicitud, name='listar_solicitud'),
        url(r'^editar_solicitud/(?P<pk>\d+)$', views.editar_solicitud, name='editar_solicitud'),
        url(r'^imprimir_solicitud/(?P<pk>\d+)$', views.imprimir_solicitud, name='imprimir_solicitud'),
        url(r'^enviar_solicitud/(?P<pk>\d+)$', views.enviar_solicitud, name='enviar_solicitud'),

        url(r'^listar_solicitudRecibido/$', views.listar_solicitudRecibido, name='listar_solicitudRecibido'),
        url(r'^editar_solicitudRecibido/(?P<pk>\d+)$', views.editar_solicitudRecibido, name='editar_solicitudRecibido'),


)