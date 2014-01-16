from django.http import HttpResponse, Http404, HttpResponseForbidden, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.template import Context
from photoalbum.rest import rest_helper
from photoalbum.renderers.user_renderers import *
from photoalbum.renderers.album_renderers import album_list_view

"""
 /
	? GET:
		? Logged in: List of albums
		? No login: Welcome page
	? PUT: N/A
	? POST:
		? Logged in: New album
		? No login: N/A
	? DELETE: N/A
"""
def indexHandler(request):
    return rest_helper(indexGet, None, indexPost, None, request)

def indexGet(request):
    if request.user.is_authenticated():
        return album_list_view(request);
    else:
        return welcome_view(request)

def indexPost(request):
    if request.user.is_authenticated():
        raise Http404(); # TODO: New album
    else:
        return HttpResponseForbidden();

"""
 /login/
	? GET: Login page
	? PUT: N/A
	? POST: Login user
	? DELETE: N/A
"""
def loginHandler(request):
    return rest_helper(loginGet, None, loginPost, None, request)

def loginGet(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/')
    else:
        return login_view(request);

def loginPost(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            return HttpResponseRedirect('/')
        else:
            return HttpResponse("Not active")
    else:
        return HttpResponse("Error")

"""
 /register/
	? GET: Register page
	? PUT: N/A
	? POST: Register user
	? DELETE: N/A
"""
def registerHandler(request):
    return rest_helper(registerGet, None, registerPost, None, request)

def registerGet(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/')
    else:
        return register_view(request);

def registerPost(request):
    username = request.POST['username']
    password = request.POST['password']
    email = request.POST['email']
    user = User.objects.create_user(username, email, password)
    return HttpResponseRedirect('/login/')

"""
 /logout/
 	? GET: Logout user
	? PUT: N/A
	? POST: N/A
	? DELETE: N/A

"""
def logoutHandler(request):
    logout(request)
    return HttpResponseRedirect('/')