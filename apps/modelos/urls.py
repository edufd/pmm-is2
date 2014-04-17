from django.conf.urls import patterns, url

from apps.modelos import views


urlpatterns = patterns('',
        url(r'^$', views.index, name='index'),
        url(r'^registrar/$', views.registrar, name='register'),
        url(r'^rol/$', views.registryRol, name='registryRol'),
)