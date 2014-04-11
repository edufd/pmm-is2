from django.http import HttpResponseRedirect
from django.shortcuts import redirect

__author__ = 'Eduardo'
def home(request):
    return HttpResponseRedirect('/adm/')