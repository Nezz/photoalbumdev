from django.http import HttpResponse, Http404, HttpResponseForbidden, HttpResponseRedirect, HttpResponseBadRequest
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.template import Context
from photoalbum.utils import rest_helper
from photoalbum.renderers.order_renderers import *
import datetime

"""
 /albums/<Album ID>/order
	* GET: N/A
	* POST: New order of the album
"""
def ordernewHandler(request, album_id):
    return rest_helper(ordernewGet, ordernewPost, request, album_id)

def ordernewGet(request, album_id):
    album = get_object_or_404(Album, guid=album_id)
    if request.is_ajax() or request.user.is_authenticated():
        return ordernew_view(request, album)
    elif not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('login'))
    else:
        return HttpResponseForbidden()

def ordernewPost(request, album_id):
    album = get_object_or_404(Album, guid=album_id)
    if request.user.is_authenticated():
        album.pk = None
        album.owner = None
        album.guid = ""
        album.save() # Copy album

        order = Order.objects.create(owner=request.user, album=album, time_placed=datetime.datetime.now()) # TODO: Order params (name, address, etc)

        return HttpResponseRedirect(reverse('orderitem', kwargs={'order_id' : order.pk}))
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
    order = get_object_or_404(Order, pk=order_id)
    if order.owner == request.user:
        return orderitem_view(request, order)
    elif not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('login'))
    else:
        return HttpResponseForbidden()

def orderitemPost(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    if order.owner == request.user:
        # TODO
        raise Http404
    elif not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('login'))
    else:
        return HttpResponseForbidden()

"""
 /orders/<Order ID>/delete
	* GET:
		None
	* POST: Delete order (Owner only)
"""
def orderitemdeleteHandler(request, order_id):
    return rest_helper(orderitemdeleteGet, orderitemdeletePost, request, order_id)

def orderitemdeleteGet(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    if request.is_ajax() or album.owner == request.user:
        return orderdelete_view(request, order)
    elif not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('login'))
    else:
        return HttpResponseForbidden()

def orderitemdeletePost(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    if order.owner == request.user:
        order.album.delete()
        order.delete()
        return HttpResponseRedirect(reverse('orderlist'))
    elif not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('login'))
    else:
        return HttpResponseForbidden()

def paymentsuccessHandler(request):
    return rest_helper(paymentsuccessGet, None, request)

def paymentsuccessGet(request):
    if 'pid' in request.GET and 'ref' in request.GET and 'checksum' in request.GET:
        raise Http404 # TODO
    else:
        return HttpResponseBadRequest()

def paymentcancelHandler(request):
    return rest_helper(paymenterrorGet, None, request)

def paymenterrorGet(request):
    if 'pid' in request.GET and 'ref' in request.GET and 'checksum' in request.GET:
        raise Http404 # TODO
    else:
        return HttpResponseBadRequest()

def paymenterrorHandler(request):
    return rest_helper(paymentcancelGet, None, request)

def paymentcancelGet(request):
    if 'pid' in request.GET and 'ref' in request.GET and 'checksum' in request.GET:
        raise Http404 # TODO
    else:
        return HttpResponseBadRequest()

