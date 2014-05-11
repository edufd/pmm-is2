from django.shortcuts import redirect
from pmm_is2.apps.adm.models import Proyecto
from django.contrib.auth.models import User, Group, Permission


#decorador para evitar que se puedan crear fases si no el duenho del proyecto
def can_manage_phase(view_func):
    def _wrapped_view_func(request, *args, **kwargs):
        id_proyecto = kwargs['pk']
        proyecto = Proyecto.objects.get(id_proyecto=id_proyecto)
        print request.user
        print proyecto.lider_proyecto
        if not proyecto.lider_proyecto == request.user:
            return redirect('/adm/')
        return view_func(request, *args, **kwargs)
    return _wrapped_view_func


def can_manage_project(view_func):
    def _wrapped_view_func(request, *args, **kwargs):
        id_proyecto = kwargs['pk']
        lider_proyecto = Proyecto.objects.filter(id_proyecto=id_proyecto, lider_proyecto=request.user).exists()
        administrador = request.user.groups.filter(name='Administrador').exists()
        valido = lider_proyecto | administrador
        if not valido:
            return redirect('/adm/')
        return view_func(request, *args, **kwargs)
    return _wrapped_view_func