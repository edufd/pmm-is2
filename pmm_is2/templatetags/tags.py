__author__ = 'adriana'

#Archivo que contiene las definiciones de los tags y filtros utilizados en los templates

from django.template import Library
from pmm_is2.backends import verificar_rol_usuario
register = Library()


@register.filter(name='verificarRol')
def verificarRol(usuario):
    """
    Retorna True si el usuario tiene el permiso correspondiente, False de lo contrario.
    """
    return verificar_rol_usuario(usuario)

