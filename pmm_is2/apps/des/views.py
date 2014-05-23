from pmm_is2.apps.adm.utils import get_project_list, get_phases_list
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from pmm_is2.apps.adm.models import Proyecto, Comite
from pmm_is2.apps.des.forms import *
from django.http import HttpResponse
from io import BytesIO
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table
from reportlab.lib.units import cm


_all_ = [Proyecto, Comite]

@login_required
def index(request):
    context = RequestContext(request)
    proyectos = get_project_list()
    context_dict = {'proyectos': proyectos}
    return render_to_response('des/index.html', context_dict, context)


@login_required
def crear_tipo_item(request):
    """Funcion para Crear Tipo Item.
    Retorna la pagina correspondiente con el formulario para la creacion del Tipo ITem

    :param request: Parametro a ser procesado.
    :type request: HttpRequest.
    :returns: La pagina correspondiente.
    :rtype: El response correspondiente.
    """
    context = RequestContext(request)
    creado = False
    if request.method == 'POST':
        tipo_item_form = TipoItemForm(data=request.POST)
        atributo_tipo_item_form = AtributoTipoItemForm(data=request.POST)
        if tipo_item_form.is_valid() and atributo_tipo_item_form.is_valid():
            tipo_item = tipo_item_form.save()
            tipo_item.save()
            atributo = atributo_tipo_item_form.save(commit=False)
            atributo.tipo_item = tipo_item
            atributo.save()
            creado = True
        else:
            print tipo_item_form.errors
            print atributo_tipo_item_form.errors

    else:
        tipo_item_form = TipoItemForm()
        atributo_tipo_item_form = AtributoTipoItemForm()

    return render_to_response('des/crear_tipo_item.html',
                              {
                                  'tipo_item_form': tipo_item_form,
                                  'atributo_tipo_item_form': atributo_tipo_item_form,
                                  'creado': creado,
                              },
                              context
    )


@login_required
def crear_item(request, pk):
    """Funcion para Crear Item.
    Retorna la pagina con el formulario correspondiente para la modificacion
    del Tipo Item.

    :param request: Parametro a ser procesado.
    :param pk: Parametro a ser procesado.
    :type request: HttpRequest.
    :type pk: int.
    :returns: La pagina correspondiente.
    :rtype: El response correspondiente.
    """
    context = RequestContext(request)
    creado = False
    fase = pk
    objeto_fase = get_object_or_404(Fase, pk=pk)

    if request.method == 'POST':
        item_form = ItemForm(data=request.POST, id_fase=pk)
        if item_form.is_valid():
            item_form.instance.id_fase = objeto_fase
            item = item_form.save()
            creado = True
        else:
            print item_form.errors

    else:
        item_form = ItemForm(id_fase=pk)

    return render_to_response('des/crear_item.html',
                              {
                                  'item_form': item_form,
                                  'creado': creado,
                                  'fase': fase,
                                  'objeto_fase': objeto_fase,
                              },
                              context
    )


def get_lista_tipo_item():
    lista_tipo_item = TipoItem.objects.all()
    return lista_tipo_item


def get_lista_item():
    lista_item = Item.objects.all()
    return lista_item


@login_required
def listar_tipo_item(request):
    """Funcion para Listar tipo de Item.
    Retorna la pagina correspondiente con la lista de tipos de item

    :param request: Parametro a ser procesado.
    :type request: HttpRequest.
    :returns: La pagina correspondiente.
    :rtype: El response correspondiente.
    """
    context = RequestContext(request)
    lista_tipo_item = get_lista_tipo_item()
    context_dict = {}
    context_dict['lista_tipo_item'] = lista_tipo_item

    return render_to_response('des/lista_tipo_item.html', context_dict, context)


def listar_item(request):
    """Funcion para Listar Item.
    Retorna la pagina correspondiente con la lista de item

    :param request: Parametro a ser procesado.
    :type request: HttpRequest.
    :returns: La pagina correspondiente.
    :rtype: El response correspondiente.
    """
    context = RequestContext(request)
    lista_item = get_lista_item()
    context_dict = {}
    context_dict['lista_item'] = lista_item

    return render_to_response('des/lista_item.html', context_dict, context)


@login_required
def editar_tipo_item(request, pk):
    """Funcion para Modificar un Tipo Item.
    Retorna la pagina con el formulario correspondiente para la modificacion
    del Tipo Item.

    :param request: Parametro a ser procesado.
    :param pk: Parametro a ser procesado el identificador del tipo de Item que va a modificarse.
    :type request: HttpRequest.
    :type pk: int.
    :returns: La pagina correspondiente.
    :rtype: El response correspondiente.
    """
    context = RequestContext(request)
    tipo_item = get_object_or_404(TipoItem, pk=pk)
    tipo_item_form = TipoItemForm(request.POST or None, instance=tipo_item)
    if tipo_item_form.is_valid():
        tipo_item_form.save()
        return redirect('listar_tipo_item')

    return render_to_response('des/editar_tipo_item.html', {'tipo_item_form': tipo_item_form}, context)


@login_required
def editar_item(request, pk):
    """Funcion para Modificar un Item.
    Retorna la pagina con el formulario correspondiente para la modificacion
    del Item.

    :param request: Parametro a ser procesado.
    :param pk: Parametro a ser procesado el identificador del Item que va a modificarse.
    :type request: HttpRequest.
    :type pk: int.
    :returns: La pagina correspondiente.
    :rtype: El response correspondiente.
    """
    context = RequestContext(request)
    item = get_object_or_404(Item, pk=pk)
    item_form = ItemForm(request.POST or None, instance=item, id_fase=item.id_fase)
    if item_form.is_valid():
        item_form.save()
        return redirect('listar_item')

    return render_to_response('des/editar_item.html', {'item_form': item_form}, context)


@login_required
def eliminar_tipo_item(request, pk):
    """Funcion para Eliminar un Tipo Item.

    :param request: Parametro a ser procesado.
    :param pk: Parametro a ser procesado el identificador del tipo de Item que va a eliminarse.
    :type request: HttpRequest.
    :type pk: int.
    :returns: La pagina correspondiente.
    :rtype: El response correspondiente.
    """
    context = RequestContext(request)
    tipo_item = get_object_or_404(TipoItem, pk=pk)
    if request.method == 'POST':
        tipo_item.delete()
        return redirect('listar_tipo_item')

    return render_to_response('des/confirmar_eliminacion_tipo_item.html', {'tipo_item': tipo_item}, context)


@login_required
def eliminar_item(request, pk):
    """Funcion para Eliminar un Item.

    :param request: Parametro a ser procesado.
    :param pk: Parametro a ser procesado el identificador del Item que va a eliminarse.
    :type request: HttpRequest.
    :type pk: int.
    :returns: La pagina correspondiente.
    :rtype: El response correspondiente.
    """
    context = RequestContext(request)
    item = get_object_or_404(Item, pk=pk)
    if request.method == 'POST' and item.estado == 'ACTIVO':
        item.estado = 'INACTIVO'
        item.save()
        return redirect('listar_item')

    return render_to_response('des/confirmar_eliminacion_item.html', {'item': item}, context)


@login_required
def ver_tipo_item(request, pk):
    context = RequestContext(request)
    tipo_item = get_object_or_404(TipoItem, pk=pk)

    context_dict = {'tipo_item': tipo_item}

    return render_to_response('des/tipo_item.html', context_dict, context)

@login_required
def ver_item(request, pk):
    context = RequestContext(request)
    item = get_object_or_404(Item, pk=pk)

    context_dict = {'item': item}

    return render_to_response('des/item.html', context_dict, context)


#realiza la busqueda del texto solicitado y usa la funcion correspondiente para buscar en la base de datos
#y mostrarla en la vista
def suggest_tipo_item(request):
        context = RequestContext(request)
        cat_list = []
        starts_with = ''
        if request.method == 'GET':
                starts_with = request.GET['suggestion']
        cat_list = get_tipo_item_list(2, starts_with)

        return render_to_response('des/tipo_item_list.html', {'cat_list': cat_list}, context)


def suggest_item(request):
        context = RequestContext(request)
        cat_list = []
        starts_with = ''
        if request.method == 'GET':
                starts_with = request.GET['suggestion']
        cat_list = get_item_list(2, starts_with)

        return render_to_response('des/item_list.html', {'cat_list': cat_list}, context)


#busca el texto ingresado en permisos
def get_tipo_item_list(max_results=0, starts_with=''):
        cat_list = []
        if starts_with:
            starts_with = starts_with + '%'
            cat_list = TipoItem.objects.filter(nombre_tipo_item__like=starts_with)
        # else:
        #         cat_list = User.objects.all()
        #
        # print cat_list

        if max_results > 0:
                if len(cat_list) > max_results:
                        cat_list = cat_list[:max_results]

        return cat_list


def get_item_list(max_results=0, starts_with=''):
        cat_list = []
        if starts_with:
            starts_with = starts_with + '%'
            cat_list = Item.objects.filter(nombre_item__like=starts_with)
        # else:
        #         cat_list = User.objects.all()
        #
        # print cat_list

        if max_results > 0:
                if len(cat_list) > max_results:
                        cat_list = cat_list[:max_results]

        return cat_list


#agregado Adri
@login_required
def archivoadjunto_page(request,pk):
    """Funcion para Adjuntar un archivo a un Item.
    Retorna la pagina con el formulario correspondiente para la modificacion
    del item.

    :param request: Parametro a ser procesado.
    :param pk: Parametro a ser procesado el identificador del Item al que se le va a adjuntar el archivo.
    :type request: HttpRequest.
    :type pk: int.
    :returns: La pagina correspondiente.
    :rtype: El response correspondiente.
    """
    context = RequestContext(request)
    creado=False

    if request.method == 'POST':
        archivoAdjunto_form = ArchivoAdjuntoForm(request.POST, request.FILES)
        if archivoAdjunto_form.is_valid():
            archivoAdjunto_form.save()
            creado = True
            return render_to_response('des/archivoadjunto.html',
                              {
                                  'archivoAdjunto_form':archivoAdjunto_form,
                                  'creado': creado,
                              },
                              context)
        else:
            print archivoAdjunto_form.errors
    else:
        archivoAdjunto_form = ArchivoAdjuntoForm()
        item = get_object_or_404(Item, pk=pk)
        datap = {'id_item_relacionado':item}
        archivoAdjunto_form = ArchivoAdjuntoForm(initial=datap)
    return render_to_response('des/archivoadjunto.html',
                              {
                                  'archivoAdjunto_form':archivoAdjunto_form,
                                  'creado': creado,'item':item,
                              },
                              context)


@login_required
def crear_archivoAdjunto(request):
    """Funcion para Agregar un archivo adjunto eligiendo a cual item adjuntar.
    Retorna la pagina correspondiente con el formulario para la agregacion

    :param request: Parametro a ser procesado.
    :type request: HttpRequest.
    :returns: La pagina correspondiente.
    :rtype: El response correspondiente.
    """
    context = RequestContext(request)
    creado = False
    if request.method == 'POST':
        archivoAdjunto_form = ArchivoAdjuntoForm(request.POST, request.FILES)
        if archivoAdjunto_form.is_valid():
            archivoAdjunto_form.save()
            creado = True
        else:
            print archivoAdjunto_form.errors

    else:
        archivoAdjunto_form = ArchivoAdjuntoForm()

    return render_to_response('des/crear_archivoAdjunto.html',
                              {
                                  'archivoAdjunto_form':archivoAdjunto_form,
                                  'creado': creado,
                              },
                              context
    )


@login_required
def desasignar(request, pk):

    context = RequestContext(request)
    existe=ArchivoAdjunto.objects.filter(id_item_relacionado=pk).exists()
    if existe:
        traer=ArchivoAdjunto.objects.filter(id_item_relacionado=pk)

        return render_to_response('des/desasignar.html',
                              {
                                 'traer': traer,
                             },
                             context)
    
    else:
        return redirect('listar_item')


@login_required
def eliminar_adjunto(request, pk):
    """Funcion para Eliminar o Desasignar un Archivo Adjunto.

    :param request: Parametro a ser procesado.
    :param pk: Parametro a ser procesado el identificador del Archivo Adjunto que va a eliminarse.
    :type request: HttpRequest.
    :type pk: int.
    :returns: La pagina correspondiente.
    :rtype: El response correspondiente.
    """
    context = RequestContext(request)
    adjunto = get_object_or_404(ArchivoAdjunto, pk=pk)
    if request.method == 'POST':
        adjunto.delete()
        return redirect('listar_item')

    return render_to_response('des/confirmar_eliminacion_adjunto.html', {'adjunto': adjunto}, context)


@login_required
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

    return render_to_response('des/project_list.html', context_dict, context)


@login_required
def phases_list(request, pk):

    context = RequestContext(request)
    phases_list = get_phases_list(pk)
    context_dict = {}
    context_dict['object_list'] = phases_list

    return render_to_response('des/phases_list.html', context_dict, context)


def get_historial_item_list(pk):
    item_historial_list = VersionItem.objects.filter(item_id=pk, estado='ACTIVO').order_by('version_item')
    return item_historial_list


def historial_item(request, pk):
    """Funcion para el historial de item.
    Retorna la pagina correspondiente con el historial del item

    :param request: Parametro a ser procesado.
    :param pk: Parametro a ser procesado. Identificador del item del cual se solicita el historial.
    :type request: HttpRequest.
    :returns: La pagina correspondiente.
    :rtype: El response correspondiente.
    """
    context = RequestContext(request)
    item_historial_list = get_historial_item_list(pk)
    context_dict = {}
    context_dict['object_list'] = item_historial_list

    return render_to_response('des/historial_item.html', context_dict, context)


@login_required
def agregar_relaciones(request, id_fase):
    """Funcion para agregar relaciones de item.
    Retorna la pagina correspondiente de la agregacion del item

    :param request: Parametro a ser procesado.
    :param id_fase: Parametro a ser procesado. Identificador de la fase.
    :type request: HttpRequest.
    :returns: La pagina correspondiente.
    :rtype: El response correspondiente.
    """
    context = RequestContext(request)
    creado = False
    pk = id_fase
    object_fase = get_object_or_404(Fase, pk=pk)

    if request.method == 'POST':
        print('mierda ', id_fase)
        relacion_form = RelacionesForm(data=request.POST, id_fase=id_fase)
        if relacion_form.is_valid():
            itemA = relacion_form.cleaned_data['del_item']
            itemB = relacion_form.cleaned_data['al_item']
            tipo = relacion_form.cleaned_data['tipo']

            if itemA.id_item != itemB.id_item:
                if itemA.id_fase == itemB.id_fase and tipo == "PADRE-HIJO":
                    relacion_form.instance.fase = object_fase
                    relacion = relacion_form.save()
                    relacion.save()
                    creado = True
                elif itemA.id_fase != itemB.id_fase and tipo == "ANTECESOR-SUCESOR":
                    relacion_form.instance.fase = object_fase
                    relacion = relacion_form.save()
                    relacion.save()
                    creado = True
                else:
                    if tipo == "PADRE-HIJO":
                        error = "El tipo de relacion no puede ser Padre-Hijo ya que los items" \
                                " no pertenecen a la misma fase. Cambie el tipo de relacion"
                    else:
                        error = "El tipo de relacion no puede ser Antecesor-Sucesor ya que los items" \
                            " pertenecen a la misma fase. Cambie el tipo de relacion"

                    return render_to_response('des/agregar_relaciones.html',
                              {
                                  'relacion_form': relacion_form,
                                  'error': error,
                                  'fase': id_fase,
                              },
                              context
                    )
            else:
                error = "No se puede crear una relacion en el mismo ITEM"
                return render_to_response('des/agregar_relaciones.html',
                              {
                                  'relacion_form': relacion_form,
                                  'error': error,
                                  'fase': id_fase,
                              },
                              context
                )
        else:
            print relacion_form.errors
    else:
        print('ok ', pk)
        relacion_form = RelacionesForm(id_fase=id_fase)

    return render_to_response('des/agregar_relaciones.html',
                              {
                                  'relacion_form': relacion_form,
                                  'creado': creado,
                                  'fase': id_fase,
                              },
                              context
    )


def get_lista_relacion(id_fase):
    lista_relacion = Relacion.objects.filter(fase_id=id_fase)
    return lista_relacion


@login_required
def import_item(request, pk):
    """Funcion para Importar Item.

    :param request: Parametro a ser procesado.
    :param pk: Parametro a ser procesado. Identificador del Item
    :type request: HttpRequest.
    :returns: La pagina correspondiente.
    :rtype: El response correspondiente.
    """
    registered = False
    id_fase = pk
    context = RequestContext(request)
    item = get_object_or_404(Item, pk=pk)
    item.pk = None
    item.nombre_item = 'import_'+item.nombre_item
    item_form = ItemForm(request.POST or None, instance=item, id_fase=item.id_fase)

    if item_form.is_valid():
        item_form.save()
        registered = True

    return render_to_response('des/import_item.html',
                              {'project_form': item_form, 'registered': registered, 'id_fase': id_fase}, context)


@login_required
def item_import_list(request, pk):

    context = RequestContext(request)
    project_list = get_item_import_list(pk=pk)
    context_dict = {}
    context_dict['object_list'] = project_list

    return render_to_response('des/item_import_list.html', context_dict, context)


def get_item_import_list(pk):
    lista_item = Item.objects.filter(id_fase=pk, estado='ACTIVO')
    return lista_item


@login_required
def listar_relaciones(request, id_fase):
    """Funcion para Listar relaciones de Items de una fase especifica.

    :param request: Parametro a ser procesado.
    :param pk: Parametro a ser procesado. Identificador de la fase
    :type request: HttpRequest.
    :returns: La pagina correspondiente.
    :rtype: El response correspondiente.
    """
    context = RequestContext(request)
    lista_relacion = get_lista_relacion(id_fase)
    context_dict = {}
    context_dict['lista_relacion'] = lista_relacion
    context_dict['id_fase'] = id_fase

    return render_to_response('des/lista_relacion.html', context_dict, context)


@login_required
def eliminar_relacion(request, pk):
    """Funcion para eliminar relaciones de Items de una fase especifica.

    :param request: Parametro a ser procesado.
    :param pk: Parametro a ser procesado. Identificador de la relacion a eliminarse
    :type request: HttpRequest.
    :returns: La pagina correspondiente.
    :rtype: El response correspondiente.
    """
    context = RequestContext(request)
    relacion = get_object_or_404(Relacion, pk=pk)
    if request.method == 'POST':
        relacion.delete()
        return redirect('/des/')

    return render_to_response('des/confirmar_eliminacion_relacion.html',
                              {'relacion': relacion, 'fase': relacion.fase_id}, context)


def get_relaciones(id_item):
    lista_relacion = Relacion.objects.filter(del_item=id_item)
    return lista_relacion


@login_required
def calcular_impacto_y_costo_item(request, pk):
    """
    Retorna el impacto calculado correspondiente al item.

    :param pk: el item cuyo impacto se desea calcular
    :param request: Parametro a ser procesado
    :returns: retorna el valor calculado del impacto del item
    """
    context = RequestContext(request)
    lista_item = get_lista_item()
    max_id_item = lista_item.order_by('id_item').reverse()[0]
    global suma_costo, suma_impacto, visitados
    visitados = [0]*(int(max_id_item.id_item) + 1)
    suma_costo= 0
    suma_impacto= 0
    recorrer(pk)
    context_dict = {}
    context_dict['suma_costo'] = suma_costo
    context_dict['suma_impacto'] = suma_impacto

    return render_to_response('des/calcular_impacto_y_costo_item.html', context_dict, context)


def recorrer(pk):
    """Funcion recursiva que calcula sumas de los items recorriendo el grafo en profundidad"""
    global suma_costo, suma_impacto, visitados
    num = int(pk)
    visitados[num] = 1
    item = get_object_or_404(Item, id_item=pk)
    suma_costo = suma_costo + item.costo
    suma_impacto = suma_impacto + item.complejidad
    relaciones = get_relaciones(pk)
    for relacion in relaciones:
        num = int(relacion.al_item.id_item)
        if(visitados[num] == 0):
            recorrer(relacion.al_item.id_item)


@login_required
def calcular_costo_total(request, pk):
    """Funcion que calcula el costo total del proyecto.

    :param request: Parametro a ser procesado.
    :param pk: Parametro a ser procesado. Identificador del Proyecto.
    :type request: HttpRequest.
    :returns: La pagina correspondiente.
    :rtype: El response correspondiente.
    """
    context = RequestContext(request)
    context_dict = {}
    costo_total = 0

    lista = getItemsProyecto(pk)
    for item in lista:
        costo_total = costo_total + item.costo

    context_dict['costo_total'] = costo_total
    return render_to_response('des/calcular_costo_total.html', context_dict, context)


def getItemsProyecto(pk):
    """Funcion que retorna todos los items de un proyecto"""
    lista = []
    fases = Fase.objects.filter(proyecto=pk)
    for fase in fases:
        items = Item.objects.filter(id_fase=fase.id_fase)
        for item in items:
            if not(item.estado == 'E' or item.estado == 'P'):
                lista.append(item)
    return lista


def lista_item_revivir(request, id_fase):
    """Funcion para Listar Item Revivir.
    Retorna la pagina correspondiente con la lista de item a revivir.

    :param request: Parametro a ser procesado.
    :type request: HttpRequest.
    :returns: La pagina correspondiente.
    :rtype: El response correspondiente.
    """
    context = RequestContext(request)
    lista_item = get_lista_item_revivir(id_fase)
    context_dict = {}
    context_dict['lista_item'] = lista_item

    return render_to_response('des/lista_item_revivir.html', context_dict, context)


def get_lista_item_revivir(id_fase):
    lista_version_item = VersionItem.objects.filter(id_fase_id=id_fase, estado='INACTIVO')#.values('item_id', 'nombre_item').annotate()
    print('lista_version_item', lista_version_item)
    return lista_version_item


def revivir_item(request, pk):
    """Funcion para Revivir Item.
    Retorna la pagina correspondiente de revivir item.

    :param request: Parametro a ser procesado.
    :param pk: Parametro a ser procesado. Identificador del item a ser procesado
    :type request: HttpRequest.
    :returns: La pagina correspondiente.
    :rtype: El response correspondiente.
    """
    context = RequestContext(request)
    item_historial_list = get_historial_item_list(pk)
    context_dict = {}
    context_dict['object_list'] = item_historial_list

    return render_to_response('des/revivir_item.html', context_dict, context)


def revivir(request, pk):
    context = RequestContext(request)
    version_item = get_object_or_404(VersionItem, pk=pk)
    creado = False

    if version_item:

        item = Item(nombre_item=version_item.nombre_item, version_item=version_item.version_item,
            prioridad=version_item.prioridad, estado=version_item.estado,
            descripcion=version_item.descripcion, observaciones=version_item.observaciones,
            complejidad=version_item.complejidad, costo=version_item.costo,
            ultima_version_item_id=version_item.ultima_version_item_id, id_tipo_item=version_item.id_tipo_item,
            id_fase=version_item.id_fase)

        item.save()
        creado = True

    else:
        return render_to_response('des/revivir_item.html', context)

    return render_to_response('des/revivir_item.html', {'creado': creado}, context)


@login_required
def project_profile(request, pk):

    context = RequestContext(request)
    project = get_object_or_404(Proyecto, pk=pk)
    phases_list = get_phases_list(pk)
    context_dict = {'project': project, 'phases_list': phases_list}

    return render_to_response('des/project_profile.html', context_dict, context)


def phase_item_list(request, id_proyecto, id_fase):
    """Funcion para Listar Item de una fase.
    Retorna la pagina correspondiente con la lista de item de una fase.

    :param request: Parametro a ser procesado.
    :param id_proyecto: Parametro a ser procesado. Identificador del Proyecto
    :param id_fase: Parametro a ser procesado.Identificador de la Fase
    :type request: HttpRequest.
    :returns: La pagina correspondiente.
    :rtype: El response correspondiente.
    """
    fase = get_object_or_404(Fase, pk=id_fase)
    context = RequestContext(request)
    lista_item = get_phase_item_list(id_fase)
    context_dict = {}
    context_dict['lista_item'] = lista_item
    context_dict['proyecto'] = fase.proyecto
    context_dict['fase'] = fase

    return render_to_response('des/phase_item_list.html', context_dict, context)


def get_phase_item_list(id_fase):
    lista_item = Item.objects.filter(id_fase_id=id_fase, estado='ACTIVO').all()
    return lista_item


def crear_solicitud(request):
    """Funcion para Crear Solicitud.
    Retorna la pagina correspondiente con el formulario para la creacion de la Solicitud

    :param request: Parametro a ser procesado.
    :type request: HttpRequest.
    :returns: La pagina correspondiente.
    :rtype: El response correspondiente.
    """
    context = RequestContext(request)
    creado = False
    if request.method == 'POST':
        solicitud_form = SolicitudForm(data=request.POST)
        if solicitud_form.is_valid():
            solicitud = solicitud_form.save()
            solicitud.save()
            creado = True
        else:
            print solicitud_form.errors

    else:
        solicitud_form = SolicitudForm()

    return render_to_response('des/crear_solicitud.html',
                              {
                                  'solicitud_form':solicitud_form,
                                  'creado': creado,
                              },
                              context
    )


def get_listar_solicitud():
    lista_solicitud = Solicitud.objects.filter(estado='EN-ESPERA')
    return lista_solicitud


@login_required
def listar_solicitud(request):
    context = RequestContext(request)
    lista_solicitud = get_listar_solicitud()
    context_dict = {}
    context_dict['lista_solicitud'] = lista_solicitud

    return render_to_response('des/lista_solicitud.html', context_dict, context)


@login_required
def editar_solicitud(request, pk):
    """Funcion para Modificar una Solicitud.
    Retorna la pagina con el formulario correspondiente para la modificacion
    de la Solicitud.

    :param request: Parametro a ser procesado.
    :param pk: Parametro a ser procesado el identificador de la Solicitud que va a modificarse.
    :type request: HttpRequest.
    :type pk: int.
    :returns: La pagina correspondiente.
    :rtype: El response correspondiente.
    """
    context = RequestContext(request)
    solicitud = get_object_or_404(Solicitud, pk=pk)
    solicitud_form = SolicitudForm(request.POST or None, instance=solicitud)
    if solicitud_form.is_valid():
        solicitud_form.save()
        return redirect('listar_solicitud')

    return render_to_response('des/editar_solicitud.html', {'solicitud_form': solicitud_form}, context)


@login_required
def imprimir_solicitud(request, pk):
    """Funcion para Imprimir una Solicitud.
    Retorna la pagina con el formulario correspondiente a la visualizacion de
    de la solicitud

    :param request: Parametro a ser procesado.
    :param pk: Parametro a ser procesado el identificador de la Solicitud.
    :type request: HttpRequest.
    :type pk: int.
    :returns: La pagina correspondiente.
    :rtype: El response correspondiente.
    """
    context = RequestContext(request)
    solicitud = get_object_or_404(Solicitud, pk=pk)
    response = HttpResponse(mimetype='application/pdf')
    response['Content-Disposition'] = 'filename="Solicitud.pdf"'
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []
    style = ParagraphStyle(
 		name='Normal',
 		fontName='Helvetica-Bold',
 		fontSize=12,
 		alignment=TA_CENTER
 	)
    elements.append(Paragraph("SOLICITUD", style))
    elements.append(Spacer(1, 1 * cm))

    LEFTMARGIN = 1 * cm
    RIGHTMARGIN = 1 * cm
    TOPMARGIN = 1 * cm
    BOTTONMARGIN = 1 * cm

    COLOR_FONDO_CABECERA_1 = colors.blueviolet
    COLOR_TEXTO_CABECERA_1 = colors.white

    COLOR_FONDO_CABECERA_2 = colors.cadetblue
    COLOR_TEXTO_CABECERA_2 = colors.black

    COLOR_FONDO_CABECERA_3 = colors.gray
    COLOR_TEXTO_CABECERA_3 = colors.white

    ESTILO_GENERAL = [
    ('BOX', (0, 0), (-1, -1), 1.0, colors.black),
    ('GRID', (0, 0), (-1, -1), 1.0, colors.black),
    ('BACKGROUND', (0, 0), (-1, -1), colors.transparent),
    ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
    ('FONTSIZE', (0, 0), (-1, -1), 10),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ('LEFTPADDING', (0, 0), (-1, -1), 3),
    ('RIGHTPADDING', (0, 0), (-1, -1), 3),
    ]

    #data= [['comentarios','descripcion','nombre_linea_base','tipo']]
    data= [['fecha_inicio','nombre_proyecto','nombre_fase','nombre_item']]
    data.append([
            solicitud.fecha_inicio,
 			solicitud.nombre_proyecto,
 			solicitud.nombre_fase,
 			solicitud.nombre_item,
            #solicitud.usuario,
            #solicitud.estado,
            #solicitud.prioridad,
            #solicitud.comentarios,
            #solicitud.descripcion,
            #solicitud.nombre_linea_base,
 			#solicitud.tipo
 	])
    columnas = [100, 100, 100, 100]
    t=Table(data, columnas)
    t.setStyle(ESTILO_GENERAL)

    t.setStyle([

    ('SPAN', (0, 0), (0, 0)),
    ('BACKGROUND', (0, 0), (0, 0), COLOR_FONDO_CABECERA_3),
    ('TEXTCOLOR', (0, 0), (0, 0), COLOR_TEXTO_CABECERA_3),
    ('FONTNAME', (0, 0), (0, 0), 'Helvetica'),
    ('FONTSIZE', (0, 0), (0, 0), 11),


    ('SPAN', (1, 0), (1, 0)),
    ('BACKGROUND', (1, 0), (1, 0), COLOR_FONDO_CABECERA_3),
    ('TEXTCOLOR', (1, 0), (1, 0), COLOR_TEXTO_CABECERA_3),
    ('FONTNAME', (1, 0), (1, 0), 'Helvetica'),
    ('FONTSIZE', (1, 0), (1, 0), 11),
    ('ALIGN', (1, 0), (1, 0), 'LEFT'),
    #('SPAN', (1, 0), (3, 3)),
    #('SPAN', (0, 3), (3, 3)),
    #('SPAN', (0, 4), (1, 4)),
     ])

    elements.append(t)

    elements.append(Spacer(0, 5))

    data1= [['usuario']]
    data1.append([
            solicitud.usuario,

 	])
    columnas1 = [100]

    t1=Table(data1, columnas1)
    t1.setStyle(ESTILO_GENERAL)
    elements.append(t1)

    doc.build(elements)
    response.write(buffer.getvalue())
    buffer.close()
    return response
    return render_to_response("des/index1.html", context_instance=RequestContext(request))


@login_required
def enviar_solicitud(request, pk):
    """Funcion para enviar solicitud.
    Retorna la pagina con el formulario correspondiente para la emision de la solicitud.

    :param request: Parametro a ser procesado.
    :param pk: Parametro a ser procesado el identificador de la solicitud.
    :type request: HttpRequest.
    :type pk: int.
    :returns: La pagina correspondiente.
    :rtype: El response correspondiente.
    """
    context = RequestContext(request)
    solicitud = get_object_or_404(Solicitud, pk=pk)
    solicitud.estado='EN-PROCESO'
    solicitud.save()

    return render_to_response("des/enviar.html", context_instance=RequestContext(request))


def get_listar_solicitudRecibido():
    lista_solicitud = Solicitud.objects.filter(estado='EN-PROCESO')
    return lista_solicitud


@login_required
def listar_solicitudRecibido(request):
    context = RequestContext(request)
    lista_solicitud = get_listar_solicitudRecibido()
    context_dict = {}
    context_dict['lista_solicitud'] = lista_solicitud

    return render_to_response('des/lista_solicitudRecibido.html', context_dict, context)


@login_required
def editar_solicitudRecibido(request, pk):
    validar=False
    context = RequestContext(request)
    solicitud = get_object_or_404(Solicitud, pk=pk)
    print request

    validar=comprobar(solicitud, request)
    if validar is True\
            and solicitud.votado_por1 != request.user.username \
            and solicitud.votado_por2 != request.user.username \
            and solicitud.votado_por3 != request.user.username:
            print solicitud.votado_por1
            print request.user.username
            solicitud_form = SolicitudRecibidoForm(request.POST or None, instance=solicitud)
            if request.method == 'POST':
                if solicitud.votado_por1=='null':
                    solicitud.votado_por1=request.user.username
                    print solicitud.votado_por1
                else:
                    if solicitud.votado_por2=='null' and request.user.username!= solicitud.votado_por1:
                        solicitud.votado_por2=request.user.username
                        print solicitud.votado_por2
                    else:
                        if solicitud.votado_por3=='null' and request.user.username!=solicitud.votado_por2:
                            solicitud.votado_por3=request.user.username
                        else:
                            return redirect('listar_solicitudRecibido')
                votar=request.POST.getlist('opciones')
                if votar[0]=='1':
                    solicitud.contador =  solicitud.contador + 1
                    solicitud.encontra=solicitud.encontra

                if votar[0]=='2':
                    solicitud.encontra =  solicitud.encontra + 1
                    solicitud.contador=solicitud.contador

                total=solicitud.contador+solicitud.encontra
                if total==3:
                    solicitud.estado='RECHAZADA'
                if solicitud.contador==3:
                    solicitud.estado='APROBADA'
                    solicitud.nombre_fase.estado_fase='ABIERTA'
                    solicitud.nombre_item.estado='REVISION'
                    solicitud.nombre_linea_base.estado='REVISION'
                    solicitud.nombre_fase.save()
                    solicitud.nombre_item.save()
                    solicitud.nombre_linea_base.save()
                if solicitud.encontra==3:
                    solicitud.estado='RECHAZADA'
                commen=request.POST.getlist('comentarios')
                solicitud.comentarios=commen[0]
                solicitud.save()
                return redirect('listar_solicitudRecibido')

            else:
                return render_to_response('des/editar_solicitudRecibido.html', {'solicitud_form': solicitud_form}, context)

    else:
        return redirect('/des/listar_solicitudRecibido/')


def comprobar(self, request):
    proyect = get_object_or_404(Proyecto, nombre_proyecto=self.nombre_proyecto)
    proyect1 = Proyecto.objects.get(nombre_proyecto=self.nombre_proyecto)
    jaja = True
    print 'projec'
    print proyect
    print proyect1
    #comitt=Comite.objects.filter(proyecto=self.nombre_proyecto).exists()
    comitt = Comite.objects.filter(proyecto=self.nombre_proyecto).exists() &\
                            Comite.objects.filter(usuario=request.user).exists()
    print 'comite'
    print comitt

    return comitt