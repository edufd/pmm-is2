from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group, Permission
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.http import HttpResponse
from pmm_is2.apps.adm.forms import UserForm, UserProfileForm, GroupForm
from pmm_is2.apps.adm.models import UserProfile
from pmm_is2.apps.adm import SESSION_KEY
from pmm_is2.apps.adm import SESSION_KEY_MSG
from pmm_is2.apps.adm.backends import usuario_verificarRolUsuario

@login_required
def index(request):
    context = RequestContext(request)
    return render_to_response('adm/index.html', context)


@login_required
def usuario(request):
    context = RequestContext(request)
    current_user = request.user
    user_list = get_user_list(current_user.id)

    context_dict= {}
    context_dict['object_list'] = user_list
    return render_to_response('adm/usuario.html', context_dict, context)


@login_required
def group_create(request):
    context = RequestContext(request)
    registered = False
    if request.method == 'POST':
        group_form = GroupForm(data=request.POST)
        if group_form.is_valid():
            group = group_form.save()
            group.save()
            registered = True
        else:
            print group_form.errors

    else:
        group_form = GroupForm()

    return render_to_response('adm/group_create.html', {'group_form': group_form, 'registered': registered}, context)

@login_required
def restricted(request):
    return HttpResponse("Como estas logeado, puedes ver este texto!")


@login_required
def profile(request):

    context = RequestContext(request)
    u = User.objects.get(username=request.user)

    try:
        up = UserProfile.objects.get(user=u)
    except:
        up = None

    context_dict = {'user': u, 'userprofile': up}

    return render_to_response('adm/profile.html', context_dict, context)


def encode_url(name):
    return name.replace(' ', '_')


def decode_url(url):
    return url.replace('_', ' ')



def get_user_list(user_id):

    #user_list = User.objects.exclude(id=user_id).order_by('id')
    #join quilombo trae todos los elementos de las dos relaciones
    user_list = User.objects.exclude(id=user_id).select_related("userprofile").all().order_by('id')
    print user_list

    return user_list

def get_group_list():

    group_list = Group.objects.all()
    return group_list

@login_required
def group_list(request):

    context = RequestContext(request)
    group_list = get_group_list()
    context_dict = {}
    context_dict['object_list'] = group_list

    return render_to_response('adm/group_list.html', context_dict, context)

@login_required
def user_list(request):

    current_user = request.user
    context = RequestContext(request)
    user_list = get_user_list(current_user.id)

    context_dict = {}
    context_dict['object_list'] = user_list

    return render_to_response('adm/user_list.html', context_dict, context)


@login_required
def user_update(request, pk):
    context = RequestContext(request)
    user = get_object_or_404(User, pk=pk)
    user_form = UserForm(request.POST or None, instance=user)
    print('userid', user.id)
    profile_user = get_object_or_404(UserProfile, user_id=user.id)
    print('profile', profile_user.nombre)
    profile_form = UserProfileForm(request.POST or None, instance=profile_user)
    if user_form.is_valid() and profile_form.is_valid():

        user.set_password(user.password)
        user_form.save()
        profile_form.save()

        return redirect('user_list')

    return render_to_response('adm/user_form.html', {'userform': user_form, 'profile_form': profile_form}, context)


@login_required
def group_update(request, pk):
    context = RequestContext(request)
    group = get_object_or_404(Group, pk=pk)
    group_form = GroupForm(request.POST or None, instance=group)
    if group_form.is_valid():
        group_form.save()
        return redirect('group_list')

    return render_to_response('adm/group_form.html', {'groupform': group_form}, context)


@login_required
def user_delete(request, pk):
    context = RequestContext(request)
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        user.is_active = False
        user.save()
        return redirect('user_list')

    return render_to_response('adm/user_confirm_delete.html', {'object':user}, context)

@login_required
def group_delete(request, pk):
    context = RequestContext(request)
    group = get_object_or_404(Group, pk=pk)
    if request.method == 'POST':
        group.delete()
        return redirect('group_list')

    return render_to_response('adm/group_confirm_delete.html', {'object':group}, context)


@login_required
def asignar_roles(request):

    current_user = request.user
    context = RequestContext(request)
    user_list = get_user_list(current_user.id)

    context_dict = {}
    context_dict['object_list'] = user_list

    return render_to_response('adm/user_group.html', context_dict, context)


@login_required
def asignar(request, pk):
    context = RequestContext(request)
    registered = False
    if request.method == 'POST':
        user = get_object_or_404(User, pk=pk)
        user_group = UserGroup(request.POST or None, instance=user)
        if user_group.is_valid():
            user= user_group.save()
            user.save()
            registered = True
        else:
             print user_group.errors
    else:
        user_group = UserGroup()

    return render_to_response('adm/group_user.html', {'user_group': user_group,'registered': registered}, context)


@login_required
def register(request):
    context = RequestContext(request)
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            registered = True
        else:
            print user_form.errors, profile_form.errors
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
    return render_to_response(
        'adm/register.html',
        {'user_form': user_form, 'profile_form': profile_form, 'registered': registered},
        context)


def get_category_list(max_results=0, starts_with=''):
        cat_list = []
        if starts_with:
            cat_list = User.objects.filter(username=starts_with)
        # else:
        #         cat_list = User.objects.all()
        #
        # print cat_list

        if max_results > 0:
                if len(cat_list) > max_results:
                        cat_list = cat_list[:max_results]

        for cat in cat_list:
                cat.url = encode_url(cat.username)

        return cat_list


def suggest_category(request):
        context = RequestContext(request)
        cat_list = []
        starts_with = ''
        if request.method == 'GET':
                starts_with = request.GET['suggestion']
        cat_list = get_category_list(2, starts_with)

        return render_to_response('adm/category_list.html', {'cat_list': cat_list }, context)


def get_roles_list(max_results=0, starts_with=''):
        cat_list = []
        if starts_with:
            cat_list = Group.objects.filter(name=starts_with)
        # else:
        #         cat_list = User.objects.all()
        #
        # print cat_list

        if max_results > 0:
                if len(cat_list) > max_results:
                        cat_list = cat_list[:max_results]

        for cat in cat_list:
                cat.url = encode_url(cat.name)

        return cat_list


def suggest_rol(request):
        context = RequestContext(request)
        cat_list = []
        starts_with = ''
        if request.method == 'GET':
                starts_with = request.GET['suggestion']
        cat_list = get_roles_list(2, starts_with)

        return render_to_response('adm/roles_list.html', {'cat_list': cat_list }, context)


#busca el texto ingresado en permisos
def get_permisos_list(max_results=0, starts_with=''):
        cat_list = []
        if starts_with:
            cat_list = Permission.objects.filter(name=starts_with)
        # else:
        #         cat_list = User.objects.all()
        #
        # print cat_list

        if max_results > 0:
                if len(cat_list) > max_results:
                        cat_list = cat_list[:max_results]

        for cat in cat_list:
                cat.url = encode_url(cat.name)

        return cat_list


#realiza la busqueda del texto solicitado y usa la funcion correspondiente para buscar en la base de datos
#y mostrarla en la vista
def suggest_permiso(request):
        context = RequestContext(request)
        cat_list = []
        starts_with = ''
        if request.method == 'GET':
                starts_with = request.GET['suggestion']
        cat_list = get_permisos_list(2, starts_with)

        return render_to_response('adm/permisos_list.html', {'cat_list': cat_list }, context)