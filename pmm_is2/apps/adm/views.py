from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.http import HttpResponse
from pmm_is2.apps.adm.forms import UserForm, UserProfileForm
from pmm_is2.apps.adm.models import UserProfile


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
    return render_to_response('adm/usuario.html', context)


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
    user_list = User.objects.all().order_by('id')

    for user in user_list:
        user.url = encode_url(user.username)
    return user_list


@login_required
def user_list(request):

    current_user = request.user
    context = RequestContext(request)
    user_list = get_user_list(current_user.id)

    context_dict= {}
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
def user_delete(request, pk):
    context = RequestContext(request)
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        user.is_active = False
        user.save()
        return redirect('user_list')

    return render_to_response('adm/user_confirm_delete.html', {'object':user}, context)