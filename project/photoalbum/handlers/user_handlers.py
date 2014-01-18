from django.http import HttpResponse, Http404, HttpResponseForbidden, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.template import Context
from photoalbum.rest import rest_helper
from photoalbum.renderers.user_renderers import *
from photoalbum.renderers.album_renderers import album_list_view
from photoalbum.handlers.album_handlers import albumitemPost
from photoalbum.models import Album
from django import forms
from django.core.validators import validate_email
import string
import random

"""
 /
	* GET:
		* Logged in: List of albums
		* No login: Welcome page
	* POST:
		* New album (Owner only)
"""
def indexHandler(request):
    return rest_helper(indexGet, indexPost, request)

def indexGet(request):
    if request.user.is_authenticated():
        return album_list_view(request);
    else:
        return welcome_view(request)

def indexPost(request):
    if request.user.is_authenticated():
        guid = ''.join(random.choice(string.ascii_lowercase + string.digits) for x in range(8))
        newAlbum = Album.objects.create(name="New album", guid=guid, owner=request.user)
        return albumitemPost(request, newAlbum.guid)
    else:
        return HttpResponseForbidden();

"""
 /login/
	* GET: Login page
	* POST: Login user
"""
def loginHandler(request):
    return rest_helper(loginGet, loginPost, request)

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
	* GET: Register page
	* POST: Register user
"""
def registerHandler(request):
    return rest_helper(registerGet, registerPost, request)

def registerGet(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/')
    else:
        return register_view(request);

def registerPost(request):
    usernam = request.POST['username']
    password = request.POST['password']
    email = request.POST['email']
    
    if User.objects.filter(username=usernam).exists():
    	return HttpResponse("User already exists")
    	     
    user = User.objects.create_user(usernam, email, password)
    return HttpResponseRedirect('/login/')

"""
 /logout/
 	* GET: Logout user
	* POST: N/A
"""
def logoutHandler(request):
    logout(request)
    return HttpResponseRedirect('/')