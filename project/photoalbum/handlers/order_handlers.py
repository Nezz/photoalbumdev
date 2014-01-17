from django.http import HttpResponse, Http404, HttpResponseForbidden, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.template import Context
from photoalbum.rest import rest_helper

"""
 /<Album ID>/order
	* GET: New order of the album
	* POST: N/A
"""
def neworderHandler(request, album_id):
    return rest_helper(neworderGet, None, request, album_id)

def neworderGet(request, album_id):
    raise Http404(); # TODO

"""
 /orders/
	* GET:
		* Logged in: List of orders
		* No login: Login page
	* POST: N/A
"""
def orderlistHandler(request):
    return rest_helper(orderlistGet, None, request)

def orderlistGet(request):
    raise Http404(); # TODO

"""
 /orders/<Order ID>
	* GET:
		* Logged in: Order details
		* No login: Login page
	* POST:
		* Cancel order (owner only)
"""
def orderitemHandler(request, order_id):
    return rest_helper(orderitemGet, None, request, order_id)

def orderitemGet(request, order_id):
    raise Http404(); # TODO

"""
 /orders/<Order ID>/delete
	* GET:
		* Owner login: Are you sure you want to delete?
		* No login: Login page 
	* POST: Delete order (Owner only)
"""
def orderitemdeleteHandler(request, order_id):
    return rest_helper(orderlistGet, None, request, order_id)

def orderitemdeleteGet(request, order_id):
    raise Http404(); # TODO

def orderitemdeletePost(request, order_id):
    raise Http404(); # TODO