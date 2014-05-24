from pmm_is2.apps.adm.models import Fase
from pmm_is2.apps.adm.utils import not_in_admin_group, get_project_list, get_phases_list
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from pmm_is2.apps.adm.models import Proyecto
from pmm_is2.apps.gdc.forms import *


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
    """Funcion para Crear Linea Base.
    Retorna la pagina correspondiente con el formulario para la creacion de la Linea Base

    :param request: Parametro a ser procesado.
    :type request: HttpRequest.
    :param pk: Parametro a ser procesado. Identificador de la Fase donde se creara la Linea Base.
    :returns: La pagina correspondiente.
    :rtype: El response correspondiente.
    """
    context = RequestContext(request)
    creado = False
    fase = pk
    objeto_fase = get_object_or_404(Fase, pk=pk)

    if request.method == 'POST':
        linea_base_from = LineaBaseForm(data=request.POST, id_fase=pk)
        if linea_base_from.is_valid():
            linea_base_from.instance.fase = objeto_fase
            item = linea_base_from.save()
            creado = True
        else:
            print linea_base_from.errors

    else:
        linea_base_from = LineaBaseForm(id_fase=pk)

    return render_to_response('gdc/crear_linea_base.html',
                              {
                                  'linea_base_from': linea_base_from,
                                  'creado': creado,
                                  'fase': fase,
                                  'objeto_fase': objeto_fase,
                              },
                              context
    )


def listar_linea_base(request, pk):
    """Funcion para Listar Linea Base.
    Retorna la pagina correspondiente con la lista de Lineas Base

    :param request: Parametro a ser procesado.
    :type request: HttpRequest.
    :param pk: Parametro a ser procesado. Identificador de la Fase del cual se listara la LB.
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

    """Funcion para Modificar una Linea Base.
    Retorna la pagina con el formulario correspondiente para la modificacion
    de la Linea Base.

    :param request: Parametro a ser procesado.
    :param pk: Parametro a ser procesado el identificador de la Linea Base que va a modificarse.
    :type request: HttpRequest.
    :type pk: int.
    :returns: La pagina correspondiente.
    :rtype: El response correspondiente.
    """

    registered = False
    context = RequestContext(request)
    proyecto = get_object_or_404(LineaBase, pk=pk)
    project_form = LineaBaseFormEdit(request.POST or None, instance=proyecto, id_fase=pk)
    id_proyecto = pk
    if project_form.is_valid():
        project_form.save()
        registered = True

    return render_to_response('gdc/linea_base_update.html',
                              {'project_form': project_form, 'id_proyecto': id_proyecto,
                               'registered': registered}, context)


@login_required
def project_profile(request, pk):

    context = RequestContext(request)
    project = get_object_or_404(Proyecto, pk=pk)
    phases_list = get_phases_list(pk)
    context_dict = {'project': project, 'phases_list': phases_list}

    return render_to_response('gdc/project_profile.html', context_dict, context)


def suggest_linea_base(request):
        context = RequestContext(request)
        cat_list = []
        starts_with = ''
        if request.method == 'GET':
                starts_with = request.GET['suggestion']
        cat_list = get_linea_base_list_search()

        return render_to_response('gdc/linea_base_list.html', {'cat_list': cat_list}, context)


def get_linea_base_list_search():
    linea_base_list = LineaBase.objects.all().order_by('id_linea_base')
    return linea_base_list


@login_required
@user_passes_test(not_in_admin_group, login_url='/login/')
def linea_base_profile(request, pk):

    context = RequestContext(request)
    project = get_object_or_404(LineaBase, pk=pk)
    context_dict = {'project': project}

    return render_to_response('gdc/linea_base_profile.html', context_dict, context)
