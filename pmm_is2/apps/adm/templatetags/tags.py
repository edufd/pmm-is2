__author__ = 'adriana'

#Archivo que contiene las definiciones de los tags y filtros utilizados en los templates

from django.template import Library
from pmm_is2.apps.adm.backends import usuario_verificarRolUsuario
register = Library()



@register.filter(name='verificarRolUsuario')
def verificarRolUsuario(usuario):
    """
    Retorna True si el usuario tiene el permiso correspondiente, False de lo contrario.
    """
    return usuario_verificarRolUsuario(usuario)

