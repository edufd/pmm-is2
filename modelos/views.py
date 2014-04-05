from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from modelos.forms import UserForm

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
            user = user_form.save()
            user.save()
            registered = True

        else:
            print user_form.errors

    else:
        user_form = UserForm()

    return render_to_response(
        'modelos/registrar.html',
            {'user_form': user_form, 'registered': registered},
            context)