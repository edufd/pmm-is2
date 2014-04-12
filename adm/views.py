from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404, redirect
from adm.forms import UserForm, UserProfileForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse

# Create your views here.
from adm.models import UserProfile

def index(request):

    context = RequestContext(request)
    return render_to_response('adm/index.html', context)


def about(request):
    context = RequestContext(request)
    return render_to_response('adm/about.html', context)


def contact(request):
    context = RequestContext(request)
    return render_to_response('adm/contact.html', context)


@login_required
def home(request):
    context = RequestContext(request)
    return render_to_response('adm/home.html', context)

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

def user_login(request):
    # Like before, obtain the context for the user's request.
    context = RequestContext(request)
    context_dict = {}

    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/adm/home')
            else:
                context_dict['disabled_account'] = True
                return render_to_response('adm/user_login.html', context_dict, context)
        else:
            print "Invalid login details: {0}, {1}".format(username, password)
            context_dict['bad_details'] = True
            return render_to_response('adm/user_login.html', context_dict, context)

    else:
        return render_to_response('adm/user_login.html', context_dict, context)

@login_required
def restricted(request):
    return HttpResponse("Como estas logeado, puedes ver este texto!")

@login_required
def user_logout(request):
    logout(request)

    return HttpResponseRedirect('/adm/')

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

def get_user_list():

    user_list = User.objects.all()

    # We loop through each category returned, and create a URL attribute.
    # This attribute stores an encoded URL (e.g. spaces replaced with underscores).
    for user in user_list:
        user.url = encode_url(user.username)
    return user_list

@login_required
def user_list(request):
    context = RequestContext(request)
    user_list = get_user_list()

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
    if request.method=='POST':
        user.is_active = False
        user.save()
        return redirect('user_list')

    return render_to_response('adm/user_confirm_delete.html', {'object':user}, context)