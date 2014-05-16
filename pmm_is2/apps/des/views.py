from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from pmm_is2.apps.adm.models import Fase
from pmm_is2.apps.adm.utils import get_project_list, get_phases_list

from pmm_is2.apps.des.forms import TipoItemForm
from pmm_is2.apps.des.models import TipoItem
from pmm_is2.apps.des.forms import ItemForm

from pmm_is2.apps.des.forms import ArchivoAdjuntoForm
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
        if tipo_item_form.is_valid():
            tipo_item = tipo_item_form.save()
            tipo_item.save()
            creado = True
        else:
            print tipo_item_form.errors

    else:
        tipo_item_form = TipoItemForm()

    return render_to_response('des/crear_tipo_item.html',
                              {
                                  'tipo_item_form': tipo_item_form,
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
            item.save()
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
    item_form = ItemForm(request.POST or None, instance=item)
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


def ver_tipo_item(request, pk):
    context = RequestContext(request)
    tipo_item = get_object_or_404(TipoItem, pk=pk)

    context_dict = {'tipo_item': tipo_item}

    return render_to_response('des/tipo_item.html', context_dict, context)


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
def archivoadjunto_page(request,pk):
    context = RequestContext(request)
    creado=False
    print pk

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


def desasignar(request,pk):
    context = RequestContext(request)
    print pk
    existe=ArchivoAdjunto.objects.filter(id_item_relacionado=pk).exists()
    if existe:
        traer=ArchivoAdjunto.objects.filter(id_item_relacionado=pk)
        print traer

        return render_to_response('des/desasignar.html',
                              {
                                 'traer':traer,
                             },
                             context)
    
    else:
        return redirect('listar_item')


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


def phases_list(request, pk):

    context = RequestContext(request)
    phases_list = get_phases_list(pk)
    context_dict = {}
    context_dict['object_list'] = phases_list

    return render_to_response('des/phases_list.html', context_dict, context)


