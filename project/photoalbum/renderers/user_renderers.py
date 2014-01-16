from django.shortcuts import render_to_response
from django.core.context_processors import csrf

def welcome_view(request):
    return render_to_response("welcome.html")

def login_view(request):
    c = {}
    c.update(csrf(request))
    return render_to_response("login.html", c)

def register_view(request):
    c = {}
    c.update(csrf(request))
    return render_to_response('register.html', c)