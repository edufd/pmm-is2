from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, render_to_response, get_object_or_404

# Create your views here.
from django.template import RequestContext
from pmm_is2.apps.adm.models import Fase
from pmm_is2.apps.adm.utils import get_project_list, get_phases_list, not_in_admin_group
from pmm_is2.apps.gdc.forms import LineaBaseForm
from pmm_is2.apps.gdc.models import LineaBase


@login_required
@user_passes_test(not_in_admin_group)
def index(request):
    context = RequestContext(request)
    return render_to_response('gdc/index.html', context)


def project_list(request):
    """Funcion para Listar Proyectos.
    Retorna la pagina correspondiente con la lista de Proyectos

    :param request: Parametro a ser procesado.
    :type request: HttpRequest.
    :returns: La pagina correspondiente.
    :rtype: El response correspondiente.
    """
    context = RequestContext(request)
    project_list = get_project_list()
    context_dict = {}
    context_dict['object_list'] = project_list

    valido = False
    if request.user.is_superuser:
        valido = True

    context_dict['valido'] = valido

    return render_to_response('gdc/project_list.html', context_dict, context)


def phases_list(request, pk):

    context = RequestContext(request)
    phases_list = get_phases_list(pk)
    context_dict = {}
    context_dict['object_list'] = phases_list

    return render_to_response('gdc/phases_list.html', context_dict, context)


def crear_linea_base(request, pk):
    """Funcion para Crear Item.
    Retorna la pagina correspondiente con el formulario para la creacion del ITem

    :param request: Parametro a ser procesado.
    :type request: HttpRequest.
    :returns: La pagina correspondiente.
    :rtype: El response correspondiente.
    """
    context = RequestContext(request)
    creado = False
    fase = pk
    objeto_fase = get_object_or_404(Fase, pk=pk)

    if request.method == 'POST':
        item_form = LineaBaseForm(data=request.POST, id_fase=pk)
        if item_form.is_valid():
            item_form.instance.fase = objeto_fase
            item = item_form.save()
            creado = True
        else:
            print item_form.errors

    else:
        item_form = LineaBaseForm(id_fase=pk)

    return render_to_response('gdc/crear_linea_base.html',
                              {
                                  'item_form': item_form,
                                  'creado': creado,
                                  'fase': fase,
                              },
                              context
    )


def listar_linea_base(request, pk):
    """Funcion para Listar Proyectos.
    Retorna la pagina correspondiente con la lista de Proyectos

    :param request: Parametro a ser procesado.
    :type request: HttpRequest.
    :returns: La pagina correspondiente.
    :rtype: El response correspondiente.
    """
    context = RequestContext(request)
    project_list = get_linea_base_list(pk)
    context_dict = {}
    context_dict['object_list'] = project_list

    valido = False
    if request.user.is_superuser:
        valido = True

    context_dict['valido'] = valido

    return render_to_response('gdc/listar_linea_base.html', context_dict, context)


#busca el texto ingresado en fases
def get_linea_base_list(pk):
    phases_list = LineaBase.objects.filter(fase=pk).order_by('id_linea_base')
    return phases_list


def linea_base_update(request, pk):

    """Funcion para Modificar un Proyecto.
    Retorna la pagina con el formulario correspondiente para la modificacion
    del proyecto.

    :param request: Parametro a ser procesado.
    :param pk: Parametro a ser procesado el identificador del proyecto que va a modificarse.
    :type request: HttpRequest.
    :type pk: int.
    :returns: La pagina correspondiente.
    :rtype: El response correspondiente.
    """

    registered = False
    context = RequestContext(request)
    proyecto = get_object_or_404(LineaBase, pk=pk)
    project_form = LineaBaseForm(request.POST or None, instance=proyecto, id_fase=pk)
    id_proyecto = pk
    if project_form.is_valid():
        project_form.save()
        registered = True

    return render_to_response('gdc/linea_base_update.html',
                              {'project_form': project_form, 'id_proyecto': id_proyecto,
                               'registered': registered}, context)