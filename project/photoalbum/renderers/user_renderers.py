from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from django.template import RequestContext

def welcome_view(request):
    c = {}
    return render_to_response("welcome.html", RequestContext(request, c))

def login_view(request):
    c = {}
    c.update(csrf(request))
    return render_to_response("login.html", RequestContext(request, c))

def register_view(request):
    c = {}
    c.update(csrf(request))
    return render_to_response('register.html', RequestContext(request, c))