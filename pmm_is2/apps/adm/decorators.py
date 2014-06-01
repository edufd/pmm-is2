from django.shortcuts import redirect
from pmm_is2.apps.adm.models import Fase, Proyecto


#decorators
def not_in_admin_group(user):
    valido = False
    if user:
        combined_queryset = user.groups.filter(name='Administrador').exists() | \
                            user.groups.filter(name='Lider de Proyecto').exists()
        #print combined_queryset
        valido = combined_queryset and user.is_authenticated()
    return valido


#decorador para evitar que se puedan crear fases si no es el duenho del proyecto
def can_manage_phase(view_func):
    def _wrapped_view_func(request, *args, **kwargs):
        id_fase = kwargs['pk']
        fase = Fase.objects.get(id_fase=id_fase)
        print request.user
        print fase.proyecto.lider_proyecto
        if not fase.proyecto.lider_proyecto == request.user:
            return redirect('/adm/')
        return view_func(request, *args, **kwargs)
    return _wrapped_view_func


def can_create_phase(view_func):
    def _wrapped_view_func(request, *args, **kwargs):
        id_proyecto = kwargs['pk']
        proyecto = Proyecto.objects.get(id_proyecto=id_proyecto)
        print request.user
        print proyecto.lider_proyecto
        if not proyecto.lider_proyecto == request.user:
            return redirect('/adm/proyectos/')
        elif proyecto.fase_set.all().__len__() == proyecto.numero_fases:
            return redirect('/adm/proyectos/')
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