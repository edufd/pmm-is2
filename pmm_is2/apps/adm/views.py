from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User, Group, Permission
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.http import HttpResponse
from pmm_is2.apps.adm.forms import UserForm, UserProfileForm, GroupForm, ProjectForm, FaseForm
from pmm_is2.apps.adm.models import UserProfile, Proyecto, Fase


def not_in_admin_group(user):
    """Use with a ``user_passes_test`` decorator to restrict access to
    authenticated users who are not in the "Administrador" group."""
    valido = False
    if user:
        combined_queryset = user.groups.filter(name='Administrador').exists() | \
                            user.groups.filter(name='Lider de Proyecto').exists()
        #print combined_queryset
        valido = combined_queryset and user.is_authenticated()
    return valido


@user_passes_test(not_in_admin_group)
@login_required
def index(request):
    context = RequestContext(request)
    return render_to_response('adm/index.html', context)


@user_passes_test(not_in_admin_group)
@login_required
def usuario(request):
    context = RequestContext(request)
    current_user = request.user
    user_list = get_user_list(current_user.id)

    context_dict= {}
    context_dict['object_list'] = user_list
    return render_to_response('adm/usuario.html', context_dict, context)


@user_passes_test(not_in_admin_group)
@login_required
def roles(request):
    context = RequestContext(request)
    current_user = request.user
    roles = Group.objects.all()
    context_dict= {}
    context_dict['object_list'] = roles
    return render_to_response('adm/roles.html', context_dict, context)


@user_passes_test(not_in_admin_group)
@login_required
def permisos(request):
    context = RequestContext(request)
    current_user = request.user
    permisos = Permission.objects.all()
    context_dict= {}
    context_dict['object_list'] = permisos
    return render_to_response('adm/permisos.html', context_dict, context)


@user_passes_test(not_in_admin_group)
@login_required
def proyectos(request):
    context = RequestContext(request)
    return render_to_response('adm/proyectos.html', context)


@login_required
@user_passes_test(not_in_admin_group)
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
@user_passes_test(not_in_admin_group)
def project_create(request):
    context = RequestContext(request)
    registered = False
    if request.method == 'POST':
        #    context = RequestContext(request)
        # user = get_object_or_404(User, pk=pk)
        # user_form = UserForm(request.POST or None, instance=user)
        # profile_user = get_object_or_404(UserProfile, user_id=user.id)
        # profile_form = UserProfileForm(request.POST or None, instance=profile_user)
        project_form = ProjectForm(request.POST or None, instance=Proyecto())
        fase_form = FaseForm(request.POST or None, instance=Fase())
        if project_form.is_valid() and fase_form.is_valid():
            new_project = project_form.save()
            new_project.save()
            new_fase = fase_form.save(commit=False)
            new_fase.proyecto = new_project
            new_fase.save()
            registered = True
        else:
            print project_form.errors

    else:
        project_form = ProjectForm()
        fase_form = FaseForm()

    return render_to_response('adm/project_create.html',
                              {'project_form': project_form, 'fase_form': fase_form,
                               'registered': registered}, context)


@user_passes_test(not_in_admin_group, login_url='/login/')
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

@user_passes_test(not_in_admin_group, login_url='/login/')
@login_required
def user_update(request, pk):
    context = RequestContext(request)
    user = get_object_or_404(User, pk=pk)
    user_form = UserForm(request.POST or None, instance=user)
    profile_user = get_object_or_404(UserProfile, user_id=user.id)
    profile_form = UserProfileForm(request.POST or None, instance=profile_user)
    if user_form.is_valid() and profile_form.is_valid():

        user.set_password(user.password)
        user_form.save()
        profile_form.save()

        return redirect('user_list')

    return render_to_response('adm/user_form.html', {'userform': user_form, 'profile_form': profile_form}, context)

@user_passes_test(not_in_admin_group, login_url='/login/')
@login_required
def group_update(request, pk):
    context = RequestContext(request)
    group = get_object_or_404(Group, pk=pk)
    group_form = GroupForm(request.POST or None, instance=group)
    if group_form.is_valid():
        group_form.save()
        return redirect('group_list')

    return render_to_response('adm/group_form.html', {'groupform': group_form}, context)

@user_passes_test(not_in_admin_group, login_url='/login/')
@login_required
def user_delete(request, pk):
    context = RequestContext(request)
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        user.is_active = False
        user.save()
        return redirect('user_list')

    return render_to_response('adm/user_confirm_delete.html', {'object':user}, context)

@user_passes_test(not_in_admin_group, login_url='/login/')
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


@user_passes_test(not_in_admin_group, login_url='/login/')
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
            starts_with = starts_with + '%'
            print starts_with
            cat_list = User.objects.filter(username__like=starts_with)
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
            starts_with = starts_with + '%'
            cat_list = Group.objects.filter(name__like=starts_with)
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
            starts_with = starts_with + '%'
            cat_list = Permission.objects.filter(name__like=starts_with)
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


@user_passes_test(not_in_admin_group, login_url='/login/')
@login_required
def perfil(request, pk):

    context = RequestContext(request)
    usuario = get_object_or_404(User, pk=pk)

    try:
        datos_personales = get_object_or_404(UserProfile, user_id=usuario.id)
    except:
        datos_personales = None

    context_dict = {'usuario': usuario, 'userprofile': datos_personales}

    print request.user

    return render_to_response('adm/profile.html', context_dict, context)


@user_passes_test(not_in_admin_group, login_url='/login/')
@login_required
def rol(request, pk):

    context = RequestContext(request)
    rol = get_object_or_404(Group, pk=pk)
    context_dict = {'rol': rol}

    return render_to_response('adm/rol.html', context_dict, context)


@user_passes_test(not_in_admin_group, login_url='/login/')
@login_required
def permiso(request, pk):

    context = RequestContext(request)
    permiso = get_object_or_404(Permission, pk=pk)
    context_dict = {'permiso': permiso}

    return render_to_response('adm/permiso.html', context_dict, context)