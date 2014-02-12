from django.http import HttpResponse, Http404, HttpResponseForbidden, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.template import Context
from photoalbum.utils import rest_helper
from photoalbum.renderers.order_renderers import *

"""
 /albums/<Album ID>/order
	* GET: N/A
	* POST: New order of the album
"""
def neworderHandler(request, album_id):
    return rest_helper(None, neworderPost, request, album_id)

def neworderPost(request, album_id):
        if request.user.is_authenticated():
            return order_create_view(request, album_id)
        else:
            return HttpResponseRedirect(reverse('login'))
    

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
        if request.user.is_authenticated():
            return order_list_view(request)
        else:
            return HttpResponseRedirect(reverse('login'))
    

"""
 /orders/<Order ID>
	* GET:
		* Logged in: Order details
		* No login: Login page
	* POST:
		* Cancel order (owner only)
"""
def orderitemHandler(request, order_id):
    return rest_helper(orderitemGet, orderitemPost, request, order_id)

def orderitemGet(request, order_id):
    raise Http404(); # TODO

def orderitemPost(request, order_id):
    raise Http404(); # TODO

"""
 /orders/<Order ID>/delete
	* GET:
		None
	* POST: Delete order (Owner only)
"""
def orderitemdeleteHandler(request, order_id):
    return rest_helper(None, orderitemdeletePost, request, order_id)

def orderitemdeletePost(request, order_id):
    if request.user.is_authenticated:
        order = get_object_or_404(Order, pk=order_id)
        order.delete()
        return order_list_view(request)
    else:
        return HttpResponseRedirect(reverse('login'))
