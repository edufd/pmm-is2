from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext

from pmm_is2.apps.des.forms import TipoItemForm
from pmm_is2.apps.des.models import TipoItem


@login_required
def index(request):
    context = RequestContext(request)
    return render_to_response('des/index.html', context)

@login_required
def crear_tipo_item(request):
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


def get_lista_tipo_item():
    lista_tipo_item = TipoItem.objects.all()
    return lista_tipo_item

@login_required
def listar_tipo_item(request):
    context = RequestContext(request)
    lista_tipo_item = get_lista_tipo_item()
    context_dict = {}
    context_dict['lista_tipo_item'] = lista_tipo_item

    return render_to_response('des/lista_tipo_item.html', context_dict, context)

@login_required
def editar_tipo_item(request, pk):
    context = RequestContext(request)
    tipo_item = get_object_or_404(TipoItem, pk=pk)
    tipo_item_form = TipoItemForm(request.POST or None, instance=tipo_item)
    if tipo_item_form.is_valid():
        tipo_item_form.save()
        return redirect('listar_tipo_item')

    return render_to_response('des/editar_tipo_item.html', {'tipo_item_form': tipo_item_form}, context)

@login_required
def eliminar_tipo_item(request, pk):
    context = RequestContext(request)
    tipo_item = get_object_or_404(TipoItem, pk=pk)
    if request.method == 'POST':
        tipo_item.delete()
        return redirect('listar_tipo_item')

    return render_to_response('des/confirmar_eliminacion_tipo_item.html', {'tipo_item': tipo_item}, context)