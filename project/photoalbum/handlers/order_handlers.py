from django.http import HttpResponse, Http404, HttpResponseForbidden, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.template import Context
from photoalbum.rest import rest_helper

"""
 /<Album ID>/order
	? GET: New order of the album
	? PUT: N/A
	? POST: N/A
	? DELETE: N/A
"""
def neworderHandler(request, album_id):
    return rest_helper(neworderGet, None, None, None, request, album_id)

def neworderGet(request, album_id):
    raise Http404(); # TODO

"""
 /orders/
	? GET:
		? Logged in: List of orders
		? No login: Login page
	? PUT: N/A
	? POST: N/A
	? DELETE: N/A
"""
def orderlistHandler(request):
    return rest_helper(orderlistGet, None, None, None, request)

def orderlistGet(request):
    raise Http404(); # TODO

"""
 /orders/<Order ID>
	? GET:
		? Logged in: Order details
		? No login: Login page
	? PUT: N/A
	? POST: N/A
	? DELETE:
		? Logged in: Cancel order
		? No login: Login page
"""
def orderitemHandler(request, order_id):
    return rest_helper(orderitemGet, None, None, orderitemDelete, request, order_id)

def orderitemGet(request, order_id):
    raise Http404(); # TODO

def orderitemDelete(request, order_id):
    raise Http404(); # TODO