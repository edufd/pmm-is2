__author__ = 'VICTOR'
from django.conf.urls import patterns, url
from pmm_is2.apps.gdc import views

urlpatterns = patterns('',

        url(r'^$', views.index, name='index'),


        url(r'^project_list/$', views.project_list, name='project_list'),
        url(r'^listar_linea_base/(?P<pk>\d+)$', views.listar_linea_base, name='listar_linea_base'),
        url(r'^phases_list/(?P<pk>\d+)$', views.phases_list, name='phases_list'),
        url(r'^crear_linea_base/(?P<pk>\d+)$', views.crear_linea_base, name='crear_linea_base'),
        url(r'^linea_base_update/(?P<pk>\d+)$', views.linea_base_update, name='linea_base_update'),

        url(r'^project_profile/(?P<pk>\d+)$', views.project_profile, name='project_profile'),

        url(r'^suggest_linea_base/$', views.suggest_linea_base, name='suggest_linea_base'),
        url(r'^linea_base_profile/(?P<pk>\d+)$', views.linea_base_profile, name='linea_base_profile'),
)