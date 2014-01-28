from django.http import HttpResponse, Http404, HttpResponseForbidden, HttpResponseRedirect, HttpResponseBadRequest
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.template import Context
from photoalbum.utils import rest_helper
from photoalbum.renderers.user_renderers import *
from photoalbum.models import Album
from django import forms
from django.core.validators import validate_email
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context

"""
 /
	* GET:
		* Logged in: List of albums
		* No login: Welcome page
	* POST: N/A
"""
def indexHandler(request):
    return rest_helper(indexGet, None, request)

def indexGet(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('albumlist'))
    else:
        return welcome_view(request)

"""
 /login/
	* GET: Login page
	* POST: Login user
"""
def loginHandler(request):
    return rest_helper(loginGet, loginPost, request)

def loginGet(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('index'))
    else:
        return login_view(request);

def loginPost(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            return HttpResponseRedirect(reverse('index'))
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
        return HttpResponseRedirect(reverse('index'))
    else:
        return register_view(request);

def registerPost(request):
    username = request.POST['username']
    password = request.POST['password']
    email = request.POST['email']
    
    if User.objects.filter(username=username).exists():
    	return HttpResponseBadRequest()
    	     
    user = User.objects.create_user(username, email, password)
    plaintext = get_template('email.txt')
    htmly     = get_template('email.html')
    d = Context({ 'username': username })
    subject, from_email, to = 'hello', 'petyalovei@gmail.com', email
    text_content = plaintext.render(d)
    html_content = htmly.render(d)
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()
    return HttpResponseRedirect(reverse('login'))

"""
 /logout/
 	* GET: Logout user
	* POST: N/A
"""
def logoutHandler(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))
