from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from pmm_is2.apps.adm.backends import iniciar_sesion
from pmm_is2.apps.adm.backends import cerrar_sesion
from pmm_is2.apps.adm import SESSION_KEY
from django.contrib.auth.models import User, Group, Permission
from pmm_is2.apps.adm import SESSION_KEY_MSG



def index(request):

    context = RequestContext(request)
    return render_to_response('pmm_is2/index.html', context)


def about(request):
    context = RequestContext(request)
    return render_to_response('pmm_is2/about.html', context)


def contact(request):
    context = RequestContext(request)
    return render_to_response('pmm_is2/contact.html', context)


@login_required
def home(request):
    context = RequestContext(request)
    return render_to_response('pmm_is2/home.html', context)


def user_login(request):
    context = RequestContext(request)
    context_dict = {}
    if SESSION_KEY in request.session.keys():
        return render_to_response('pmm_is2/home.html', context)
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                iniciar_sesion(request,user)
                return HttpResponseRedirect('/home')
            else:
                context_dict['disabled_account'] = True
                return render_to_response('pmm_is2/user_login.html', context_dict, context)
        else:
            print "Invalid login details: {0}, {1}".format(username, password)
            context_dict['bad_details'] = True
            return render_to_response('pmm_is2/user_login.html', context_dict, context)

    else:
        return render_to_response('pmm_is2/user_login.html', context_dict, context)

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')
