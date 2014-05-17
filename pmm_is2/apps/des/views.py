from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from pmm_is2.apps.adm.models import Fase
from pmm_is2.apps.adm.utils import get_project_list, get_phases_list

from pmm_is2.apps.des.forms import TipoItemForm, AtributoTipoItemForm
from pmm_is2.apps.des.models import TipoItem, VersionItem, Relacion
from pmm_is2.apps.des.forms import ItemForm

from pmm_is2.apps.des.forms import ArchivoAdjuntoForm, RelacionesForm
from pmm_is2.apps.des.models import ArchivoAdjunto

from pmm_is2.apps.des.models import Item


@login_required
def index(request):
    context = RequestContext(request)
    return render_to_response('des/index.html', context)


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
                              },
                              context
    )


def get_lista_tipo_item():
    lista_tipo_item = TipoItem.objects.all()
    return lista_tipo_item


def get_lista_item():
    lista_item =Item.objects.all()
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
    if (request.method == 'POST' and item.estado != 'A'):
        item.delete()
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
    """Funcion para Crear Item.
    Retorna la pagina correspondiente con el formulario para la creacion del ITem

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
def desasignar(request,pk):
    context = RequestContext(request)
    existe=ArchivoAdjunto.objects.filter(id_item_relacionado=pk).exists()
    if existe:
        traer=ArchivoAdjunto.objects.filter(id_item_relacionado=pk)

        return render_to_response('des/desasignar.html',
                              {
                                 'traer':traer,
                             },
                             context)
    
    else:
        return redirect('listar_item')

@login_required
def eliminar_adjunto(request, pk):
    """Funcion para Eliminar un Tipo Item.

    :param request: Parametro a ser procesado.
    :param pk: Parametro a ser procesado el identificador del tipo de Item que va a eliminarse.
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
    item_historial_list = VersionItem.objects.filter(item_id=pk).order_by('version_item')
    return item_historial_list

def historial_item(request, pk):

    context = RequestContext(request)
    item_historial_list = get_historial_item_list(pk)
    context_dict = {}
    context_dict['object_list'] = item_historial_list

    return render_to_response('des/historial_item.html', context_dict, context)

@login_required
def agregar_relaciones(request):

    context = RequestContext(request)
    creado = False
    if request.method == 'POST':
        relacion_form = RelacionesForm(data=request.POST)
        if relacion_form.is_valid():
            itemA = relacion_form.cleaned_data['del_item']
            itemB = relacion_form.cleaned_data['al_item']
            tipo = relacion_form.cleaned_data['tipo']
            if tipo == 'e':
                error = "Debe elegir un tipo de relacion"
                return render_to_response('des/agregar_relaciones.html',
                              {
                                  'relacion_form': relacion_form,
                                  'error': error,
                              },
                              context
                )
            if itemA.id_item != itemB.id_item:
                if itemA.id_fase == itemB.id_fase and tipo == "P":
                    relacion = relacion_form.save()
                    relacion.save()
                    creado = True
                elif itemA.id_fase != itemB.id_fase and tipo == "A":
                    relacion = relacion_form.save()
                    relacion.save()
                    creado = True
                else:
                    if tipo == "P":
                        error = "El tipo de relacion no puede ser Padre-Hijo ya que los items" \
                                " no pertenecen a la misma fase. Cambie el tipo de relacion"
                    else:
                        error = "El tipo de relacion no puede ser Antecesor-Sucesor ya que los items" \
                            " pertenecen a la misma fase. Cambie el tipo de relacion"

                    return render_to_response('des/agregar_relaciones.html',
                              {
                                  'relacion_form': relacion_form,
                                  'error': error,
                              },
                              context
                    )
            else:
                error = "No se puede crear una relacion en el mismo ITEM"
                return render_to_response('des/agregar_relaciones.html',
                              {
                                  'relacion_form': relacion_form,
                                  'error': error,
                              },
                              context
                )
        else:
            print relacion_form.errors
    else:
        relacion_form = RelacionesForm()

    return render_to_response('des/agregar_relaciones.html',
                              {
                                  'relacion_form': relacion_form,
                                  'creado': creado,
                              },
                              context
    )

def get_lista_relacion():
    lista_relacion = Relacion.objects.all()
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
    lista_item = Item.objects.filter(id_fase=pk)
    return lista_item

@login_required
def listar_relaciones(request):
    context = RequestContext(request)
    lista_relacion = get_lista_relacion()
    context_dict = {}
    context_dict['lista_relacion'] = lista_relacion

    return render_to_response('des/lista_relacion.html', context_dict, context)

@login_required
def eliminar_relacion(request, pk):
    context = RequestContext(request)
    relacion = get_object_or_404(Relacion, pk=pk)
    if request.method == 'POST':
        relacion.delete()
        return redirect('listar_relaciones')

    return render_to_response('des/confirmar_eliminacion_relacion.html', {'relacion': relacion}, context)

def get_relaciones(id_item):
    lista_relacion = Relacion.objects.filter(del_item=id_item)
    return lista_relacion


@login_required
def calcular_impacto_y_costo_item(request, pk):
    """
    Retorna el impacto calculado correspondiente al item.
    @type item: item
    @param item: el item cuyo impacto se desea calcular
    @rtype: int
    @return: retorna el valor calculado del impacto del item
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
    """Funcion que calcula el costo total del proyecto"""
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