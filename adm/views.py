from django.template import RequestContext
from django.shortcuts import render_to_response

# Create your views here.
def index(request):

    context = RequestContext(request)

    context_dict = {'boldmessage': "Soy un mensaje en negrita del contexto"}

    return render_to_response('adm/index.html', context_dict, context)