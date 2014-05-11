from django.shortcuts import redirect


#le paso el proyecto al cual agregar la fase
from pmm_is2.apps.adm.models import Proyecto


#decorador para evitar que se puedan crear fases si no el duenho del proyecto
def not_can_create_phase(view_func):
    def _wrapped_view_func(request, *args, **kwargs):
        id_proyecto = kwargs['pk']
        proyecto = Proyecto.objects.get(id_proyecto=id_proyecto)
        print request.user
        print proyecto.lider_proyecto
        if not proyecto.lider_proyecto == request.user:
            return redirect('/adm/')
        return view_func(request, *args, **kwargs)
    return _wrapped_view_func


