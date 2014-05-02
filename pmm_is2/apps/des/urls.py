from django.conf.urls import patterns, url
from pmm_is2.apps.des import views

__author__ = 'Eduardo'
urlpatterns = patterns('',

        url(r'^$', views.index, name='index'),
        url(r'^crear_tipo_item/$', views.crear_tipo_item, name='crear_tipo_item'),
        url(r'^listar_tipo_item/$', views.listar_tipo_item, name='listar_tipo_item'),
        url(r'^editar_tipo_item/(?P<pk>\d+)$', views.editar_tipo_item, name='editar_tipo_item'),
        url(r'^eliminar_tipo_item/(?P<pk>\d+)$', views.eliminar_tipo_item, name='eliminar_tipo_item'),


)