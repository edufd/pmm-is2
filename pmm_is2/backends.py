__author__ = 'adriana'

from pmm_is2.apps.adm import SESSION_KEY
from django.contrib.auth.models import User, Group, Permission
from pmm_is2.apps.adm import SESSION_KEY_MSG


def iniciar_sesion(request, usuario):
    if usuario is None:
        usuario = request.user
    if SESSION_KEY in request.session:
        if request.session[SESSION_KEY] != usuario.username:
            request.session.flush()
    else:
        request.session.cycle_key()
        request.session[SESSION_KEY] = usuario.username
        print request.session[SESSION_KEY]
        request.session[SESSION_KEY_MSG] = ["hola"]
    if hasattr(request, 'user'):
        request.user = usuario


def cerrar_sesion(request):
    request.session.flush()
    if hasattr(request, 'user'):
        request.user = None


#def usuario_verificarRolUsuario(request):
    #   valido = False
    #    alias=request.session[SESSION_KEY]
    #  print alias
    #  UsuarioId = User.objects.get(username=alias)
    # valido=UsuarioId.has_perm ('adm.add_user')
        # return valido


def verificar_rol_usuario(user):
    valido = False
    if user:
        print user.groups.filter(name='Administrador').exists()
        valido = user.groups.filter(name='Administrador').exists()
    return valido