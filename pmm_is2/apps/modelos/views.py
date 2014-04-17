from django.template import RequestContext
from django.shortcuts import render_to_response

from pmm_is2.apps.modelos.forms import UserForm
from pmm_is2.apps.modelos.forms import RolForm



# Create your views here.
def index(request):

    context = RequestContext(request)

    context_dict = {'boldmessage': "Soy un mensaje en negrita del contexto"}

    return render_to_response('modelos/index.html', context_dict, context)

def registrar(request):
    context = RequestContext(request)

    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)

        if user_form.is_valid():
            Usuario=user_form.save()
            Usuario.save()
            registered = True

        else:
            print user_form.errors

    else:
        user_form = UserForm()

    return render_to_response(
        'modelos/registrar.html',
            {'user_form': user_form, 'registered': registered},
            context)


####################CREATE_ROL####################
def registryRol(request):
    context = RequestContext(request)

    registered = False

    if request.method == 'POST':
        rol_form = RolForm(data=request.POST)

        if rol_form.is_valid():
            Rol=rol_form.save()
            Rol.save()
            registered = True

        else:
            print rol_form.errors

    else:
        rol_form = RolForm()

    return render_to_response(
        'modelos/rol.html',
        {'rol_form': rol_form, 'registered': registered},
        context)