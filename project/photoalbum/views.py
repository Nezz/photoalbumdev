from django.shortcuts import render
from django.http import HttpResponse
from django.http import Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.core.context_processors import csrf
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context


# Create your views here.

def index_view(request):
	if request.user.is_authenticated():
		return render_to_response("index.html")
	else:
		c = {}
		c.update(csrf(request))
		return render_to_response("welcome.html", c)
		
def logout_view(request):
	logout(request)
	c = {}
	c.update(csrf(request))
	return render_to_response("welcome.html", c)

def login_view(request):
    if 'username' in request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return render_to_response("index.html")
            else:
                return HttpResponse("Not active")
        else:
            return HttpResponse("Error")
    else:
        if request.user.is_authenticated():
            return render_to_response("index.html")
        else:
            c = {}
            c.update(csrf(request))
            return render_to_response("login.html", c)
        
def register_view(request):
    if 'username' in request.POST:
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        user = User.objects.create_user(username, email, password)
        c = {}
        c.update(csrf(request))
        # plaintext = get_template('email.txt')
        # 	htmly     = get_template('email.html')
        # 
        # 	d = Context({ 'username': username })
        # 
        # 	subject, from_email, to = 'hello', 'petyalovei@gmail.com', email
        # 	text_content = plaintext.render(d)
        # 	html_content = htmly.render(d)
        # 	msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        # 	msg.attach_alternative(html_content, "text/html")
        # 	msg.send()
        return render_to_response("login.html", c)
    else:
        c = {}
        c.update(csrf(request))
        return render_to_response('register.html', c)
