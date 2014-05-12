from symbol import decorator
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404, redirect
from pmm_is2.apps.adm.decorators import *
from pmm_is2.apps.adm.forms import UserForm, UserProfileForm, GroupForm, ProjectForm, FaseForm, ComiteForm
from pmm_is2.apps.adm.models import UserProfile
from pmm_is2.apps.adm.utils import *


@login_required
@user_passes_test(not_in_admin_group)
def index(request):
    context = RequestContext(request)
    return render_to_response('adm/index.html', context)


@login_required
@user_passes_test(not_in_admin_group)
def index2(request):
    context = RequestContext(request)
    return render_to_response('adm/index2.html', context)


@login_required
@user_passes_test(not_in_admin_group)
@permission_required('auth_user.add_user', login_url='/adm/')
def usuario(request):
    context = RequestContext(request)
    current_user = request.user
    user_list = get_user_list(current_user.id)

    context_dict= {}
    context_dict['object_list'] = user_list
    return render_to_response('adm/usuario.html', context_dict, context)


@login_required
@user_passes_test(not_in_admin_group)
@permission_required('auth_groups.change_group', login_url='/adm/')
def roles(request):
    context = RequestContext(request)
    current_user = request.user
    roles = Group.objects.all()
    context_dict= {}
    context_dict['object_list'] = roles
    return render_to_response('adm/roles.html', context_dict, context)


@login_required
@user_passes_test(not_in_admin_group)
def permisos(request):
    context = RequestContext(request)
    current_user = request.user
    permisos = Permission.objects.all().order_by('id')
    context_dict= {}
    context_dict['object_list'] = permisos
    return render_to_response('adm/permisos.html', context_dict, context)


@login_required
@user_passes_test(not_in_admin_group)
def proyectos(request):
    context = RequestContext(request)
    project_list = get_project_list()
    context_dict = {'project_list': project_list}
    return render_to_response('adm/proyectos.html', context_dict, context)


@login_required
@user_passes_test(not_in_admin_group)
@permission_required('auth_groups.change_group', login_url='/adm/')
def group_create(request):
    """Funcion para crear un Grupo.
    Retorna la pagina con el formulario correspondiente para la creacion
    del Grupo.

    :param request: Parametro a ser procesado.
    :type request: HttpRequest.
    :returns: La pagina correspondiente.
    :rtype: El response correspondiente.
    """
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
@permission_required('adm.add_proyecto', login_url='/adm/')
def project_create(request):

    """Funcion para Crear un Proyecto.
        Retorna la pagina con el formulario correspondiente para la creacion
        del proyecto.

        :param request: Parametro a ser procesado.
        :type request: HttpRequest.
        :returns: La pagina correspondiente.
        :rtype: El response correspondiente.
        """

    context = RequestContext(request)
    registered = False
    if request.method == 'POST':
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
            print fase_form.errors

    else:
        project_form = ProjectForm()
        fase_form = FaseForm()

    return render_to_response('adm/project_create.html',
                              {'project_form': project_form, 'fase_form': fase_form,
                               'registered': registered}, context)


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


@login_required
@permission_required('auth_groups.change_group', login_url='/adm/')
def group_list(request):
    """Funcion para Listar un Grupos.
    Retorna la pagina correspondiente con la lista de grupos

    :param request: Parametro a ser procesado.
    :type request: HttpRequest.
    :returns: La pagina correspondiente.
    :rtype: El response correspondiente.
    """

    context = RequestContext(request)
    group_list = get_group_list()
    context_dict = {}
    context_dict['object_list'] = group_list

    return render_to_response('adm/group_list.html', context_dict, context)


@login_required
@permission_required('auth_user.change_user', login_url='/adm/')
def user_list(request):

    current_user = request.user
    context = RequestContext(request)
    user_list = get_user_list(current_user.id)

    context_dict = {}
    context_dict['object_list'] = user_list

    return render_to_response('adm/user_list.html', context_dict, context)


@login_required
@user_passes_test(not_in_admin_group, login_url='/login/')
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


@login_required
@user_passes_test(not_in_admin_group, login_url='/login/')
def group_update(request, pk):
    context = RequestContext(request)
    group = get_object_or_404(Group, pk=pk)
    group_form = GroupForm(request.POST or None, instance=group)
    if group_form.is_valid():
        group_form.save()
        return redirect('group_list')

    return render_to_response('adm/group_form.html', {'groupform': group_form}, context)


@login_required
@user_passes_test(not_in_admin_group, login_url='/login/')
@can_manage_project
@permission_required('adm.change_proyecto', login_url='/adm/')
def project_update(request, pk):

    """Funcion para Modificar un Proyecto.
    Retorna la pagina con el formulario correspondiente para la modificacion
    del proyecto.

    :param request: Parametro a ser procesado.
    :param pk: Parametro a ser procesado el identificador del proyecto que va a modificarse.
    :type request: HttpRequest.
    :type pk: int.
    :returns: La pagina correspondiente.
    :rtype: El response correspondiente.
    """

    registered = False
    context = RequestContext(request)
    proyecto = get_object_or_404(Proyecto, pk=pk)
    project_form = ProjectForm(request.POST or None, instance=proyecto)
    id_proyecto = pk
    if project_form.is_valid():
        project_form.save()
        registered = True

    return render_to_response('adm/project_update.html',
                              {'project_form': project_form, 'id_proyecto': id_proyecto,
                               'registered': registered}, context)


@login_required
@user_passes_test(not_in_admin_group, login_url='/login/')
@can_manage_phase
def phase_update(request, pk):
    """Funcion para Modificar una Fase.
    Retorna la pagina con el formulario correspondiente para la modificacion
    del proyecto.

    :param request: Parametro a ser procesado.
    :param pk: Parametro a ser procesado el identificador de la fase que va a modificarse.
    :type request: HttpRequest.
    :type pk: int.
    :returns: La pagina correspondiente.
    :rtype: El response correspondiente.
    """
    registered = False
    context = RequestContext(request)
    fase = get_object_or_404(Fase, pk=pk)
    phase_form = FaseForm(request.POST or None, instance=fase)
    id_proyecto = fase.proyecto_id
    id_fase = pk
    if phase_form.is_valid():
        phase_form.save()
        registered = True
        #return redirect('project_list')

    return render_to_response('adm/phase_update.html',
                              {'phase_form': phase_form, 'id_proyecto': id_proyecto, 'id_fase': id_fase,
                               'registered': registered}, context)


@login_required
@user_passes_test(not_in_admin_group, login_url='/login/')
def user_delete(request, pk):
    """Funcion para Eliminar un User.

    :param request: Parametro a ser procesado.
    :param pk: Parametro a ser procesado el identificador del user que va a eliminarse.
    :type request: HttpRequest.
    :type pk: int.
    :returns: La pagina correspondiente.
    :rtype: El response correspondiente.
    """
    context = RequestContext(request)
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        user.is_active = False
        user.save()
        return redirect('user_list')

    return render_to_response('adm/user_confirm_delete.html', {'object':user}, context)


@login_required
@user_passes_test(not_in_admin_group, login_url='/login/')
def group_delete(request, pk):
    """Funcion para Eliminar un Grupo.

    :param request: Parametro a ser procesado.
    :param pk: Parametro a ser procesado el identificador del grupo que va a eliminarse.
    :type request: HttpRequest.
    :type pk: int.
    :returns: La pagina correspondiente.
    :rtype: El response correspondiente.
    """
    context = RequestContext(request)
    group = get_object_or_404(Group, pk=pk)
    if request.method == 'POST':
        group.delete()
        return redirect('group_list')

    return render_to_response('adm/group_confirm_delete.html', {'object':group}, context)


@login_required
@user_passes_test(not_in_admin_group, login_url='/login/')
@can_manage_phase
def phase_delete(request, pk):
    """Funcion para Eliminar una fase.

    :param request: Parametro a ser procesado.
    :param pk: Parametro a ser procesado el identificador de la fase que va a eliminarse.
    :type request: HttpRequest.
    :type pk: int.
    :returns: La pagina correspondiente.
    :rtype: El response correspondiente.
    """
    registered = False
    context = RequestContext(request)
    phase = get_object_or_404(Fase, pk=pk)
    id_proyecto = phase.proyecto_id

    if request.method == 'POST':
        phase.delete()
        registered = True
        #return redirect('phases_list/{{id_proyecto}}')

    return render_to_response('adm/phase_confirm_delete.html',
                              {'object': phase, 'id_proyecto': id_proyecto,
                               'registered': registered}, context)


@login_required
@user_passes_test(not_in_admin_group, login_url='/login/')
@can_manage_project
@permission_required('adm_proyecto.delete_proyecto', login_url='/adm/')
def project_delete(request, pk):

    """Funcion para Eliminar un Proyecto.

    :param request: Parametro a ser procesado.
    :param pk: Parametro a ser procesado el identificador del proyecto que va a eliminarse.
    :type request: HttpRequest.
    :type pk: int.
    :returns: La pagina correspondiente.
    :rtype: El response correspondiente.
    """

    context = RequestContext(request)
    proyecto = get_object_or_404(Proyecto, pk=pk)
    if request.method == 'POST':
        proyecto.delete()
        registered = True
        return redirect('project_list')

    return render_to_response('adm/group_confirm_delete.html',
                              {'object': proyecto}, context)


@login_required
@user_passes_test(not_in_admin_group, login_url='/login/')
@permission_required('auth_user.add_user', login_url='/adm/')
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


def suggest_category(request):
        context = RequestContext(request)
        cat_list = []
        starts_with = ''
        if request.method == 'GET':
                starts_with = request.GET['suggestion']
        cat_list = get_category_list(2, starts_with)

        return render_to_response('adm/category_list.html', {'cat_list': cat_list }, context)


def suggest_rol(request):
        context = RequestContext(request)
        cat_list = []
        starts_with = ''
        if request.method == 'GET':
                starts_with = request.GET['suggestion']
        cat_list = get_roles_list(2, starts_with)

        return render_to_response('adm/roles_list.html', {'cat_list': cat_list }, context)


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


#realiza la busqueda del texto solicitado y usa la funcion correspondiente para buscar en la base de datos
#y mostrarla en la vista
def suggest_proyecto(request):
        context = RequestContext(request)
        cat_list = []
        starts_with = ''
        if request.method == 'GET':
                starts_with = request.GET['suggestion']
        cat_list = get_proyectos_list(2, starts_with)

        return render_to_response('adm/proyectos_list.html', {'cat_list': cat_list}, context)


@login_required
@user_passes_test(not_in_admin_group, login_url='/login/')
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


@login_required
@user_passes_test(not_in_admin_group, login_url='/login/')
def rol(request, pk):

    context = RequestContext(request)
    rol = get_object_or_404(Group, pk=pk)
    context_dict = {'rol': rol}

    return render_to_response('adm/rol.html', context_dict, context)


@login_required
@user_passes_test(not_in_admin_group, login_url='/login/')
def permiso(request, pk):

    context = RequestContext(request)
    permiso = get_object_or_404(Permission, pk=pk)
    context_dict = {'permiso': permiso}

    return render_to_response('adm/permiso.html', context_dict, context)


#probando
@login_required
@user_passes_test(not_in_admin_group, login_url='/login/')
@can_manage_phase
def fase_create(request, pk):
    """Funcion para crear una Fase.
    Retorna la pagina con el formulario correspondiente para la creacion
    de la Fase.

    :param request: Parametro a ser procesado.
    :param pk: Parametro a ser procesado el identificador del proyecto donde se agregara la fase.
    :type request: HttpRequest.
    :returns: La pagina correspondiente.
    :rtype: El response correspondiente.
    """
    context = RequestContext(request)
    registered = False
    id_proyecto = pk
    if request.method == 'POST':
        fase_form = FaseForm(data=request.POST)
        proyecto = get_object_or_404(Proyecto, pk=pk)
        if fase_form.is_valid():
            new_fase = fase_form.save(commit=False)
            new_fase.proyecto = proyecto
            new_fase.save()
            return redirect('project_list')
            registered = True
        else:
            print fase_form.errors

    else:
        fase_form = FaseForm()

    return render_to_response('adm/fase_create.html',
                              {'fase_form': fase_form, 'id_proyecto': id_proyecto, 'registered': registered}, context)


@login_required
@user_passes_test(not_in_admin_group, login_url='/login/')
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

    return render_to_response('adm/project_list.html', context_dict, context)


@login_required
def project_import_list(request):

    context = RequestContext(request)
    project_list = get_project_list()
    context_dict = {}
    context_dict['object_list'] = project_list

    return render_to_response('adm/project_import_list.html', context_dict, context)


@login_required
def phases_list(request, pk):

    context = RequestContext(request)
    phases_list = get_phases_list(pk)
    context_dict = {}
    context_dict['object_list'] = phases_list

    return render_to_response('adm/phases_list.html', context_dict, context)


#probando1
def comite_create(request):
    """Funcion para Crear Comite.
    Retorna la pagina correspondiente con el formulario para la creacion del Comite

    :param request: Parametro a ser procesado.
    :type request: HttpRequest.
    :returns: La pagina correspondiente.
    :rtype: El response correspondiente.
    """
    context = RequestContext(request)
    registered = False
    if request.method == 'POST':
        usuario=request.POST.getlist('usuario')
        cantidad=len(usuario)
        comite_form = ComiteForm(data=request.POST)
        if cantidad == 3:
            if comite_form.is_valid():
                comite = comite_form.save()
                comite.save()
                registered = True
            else:
                print comite_form.errors
        else:
            comite_form = ComiteForm()
            return render_to_response('adm/comite_create.html', {'comite_form': comite_form, 'registered': registered}, context)
    else:
        comite_form = ComiteForm()

    return render_to_response('adm/comite_create.html', {'comite_form': comite_form, 'registered': registered}, context)


def comite_list(request):

    context = RequestContext(request)
    comite_list = get_comite_list()
    context_dict = {}
    context_dict['object_list'] = comite_list

    return render_to_response('adm/comite_list.html', context_dict, context)


def comite_update(request, pk):
    context = RequestContext(request)
    comite = get_object_or_404(Comite, pk=pk)
    comite_form = ComiteForm(request.POST or None, instance=comite)
    usuario=request.POST.getlist('usuario')
    print usuario
    cantidad=len(usuario)
    if cantidad == 3:
        if comite_form.is_valid():
            comite_form.save()
            return redirect('comite_list')
    else:
        return render_to_response('adm/comite_form.html', {'comite_form': comite_form}, context)
    return render_to_response('adm/comite_form.html', {'comite_form': comite_form}, context)


@login_required
@user_passes_test(not_in_admin_group, login_url='/login/')
def import_project(request, pk):
    """Funcion para Importar Proyecto.

    :param request: Parametro a ser procesado.
    :param pk: Parametro a ser procesado. Identificador del Proyecto
    :type request: HttpRequest.
    :returns: La pagina correspondiente.
    :rtype: El response correspondiente.
    """
    registered = False
    context = RequestContext(request)
    proyecto = get_object_or_404(Proyecto, pk=pk)
    proyecto.pk = None
    proyecto.nombre_proyecto = 'import_'+proyecto.nombre_proyecto
    id_proyecto = pk
    phases_list = get_phases_list(pk)
    project_form = ProjectForm(request.POST or None, instance=proyecto)

    if project_form.is_valid():
        project = project_form.save()
        for fase in phases_list:
            fase.pk = None
            fase.proyecto_id = project.id_proyecto
            fase.save()

        registered = True

    return render_to_response('adm/import_project.html',
                              {'project_form': project_form, 'id_proyecto': id_proyecto,
                               'phases_list': phases_list,
                               'registered': registered}, context)


@login_required
@user_passes_test(not_in_admin_group, login_url='/login/')
def project_profile(request, pk):

    context = RequestContext(request)
    project = get_object_or_404(Proyecto, pk=pk)
    context_dict = {'project': project}

    return render_to_response('adm/project_profile.html', context_dict, context)