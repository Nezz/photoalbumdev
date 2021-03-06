from django.http import HttpResponse, Http404, HttpResponseForbidden, HttpResponseRedirect, HttpResponseBadRequest
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.template import Context
from photoalbum.utils import rest_helper, validate_payment
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

        order = Order.objects.create(owner=request.user,
                                     album=album,
                                     time_placed=datetime.datetime.now(),
                                     details_name=request.POST['name'],
                                     details_zip=request.POST['zip'],
                                     details_city=request.POST['city'],
                                     details_address=request.POST['address'],
                                     details_country=request.POST['country'],
                                     details_phone=request.POST['phone'])

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
	* POST: N/A
"""
def orderitemHandler(request, order_id):
    return rest_helper(orderitemGet, None, request, order_id)

def orderitemGet(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    if order.owner == request.user:
        if 'status' in request.GET:
            return orderitem_view(request, order, request.GET['status'])
        else:
            return orderitem_view(request, order, None)
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
        if validate_payment(request.GET['pid'], request.GET['ref'], request.GET['checksum']):
            order = get_object_or_404(Order, pk=request.GET['pid'])
            order.payment_ref = request.GET['ref']
            order.save()

            return HttpResponseRedirect(reverse('orderitem', kwargs={'order_id' : request.GET['pid']}) + '?status=success')
        else:
            return HttpResponseRedirect(reverse('orderitem', kwargs={'order_id' : request.GET['pid']}) + '?status=fail')
    else:
        return HttpResponseBadRequest()

def paymentcancelHandler(request):
    return rest_helper(paymenterrorGet, None, request)

def paymenterrorGet(request):
    if 'pid' in request.GET and 'ref' in request.GET and 'checksum' in request.GET:
        if validate_payment(request.GET['pid'], request.GET['ref'], request.GET['checksum']):
            return HttpResponseRedirect(reverse('orderitem', kwargs={'order_id' : request.GET['pid']}) + '?status=error')
        else:
            return HttpResponseRedirect(reverse('orderitem', kwargs={'order_id' : request.GET['pid']}) + '?status=fail')
    else:
        return HttpResponseBadRequest()

def paymenterrorHandler(request):
    return rest_helper(paymentcancelGet, None, request)

def paymentcancelGet(request):
    if 'pid' in request.GET and 'ref' in request.GET and 'checksum' in request.GET:
        if validate_payment(request.GET['pid'], request.GET['ref'], request.GET['checksum']):
            return HttpResponseRedirect(reverse('orderitem', kwargs={'order_id' : request.GET['pid']}) + '?status=cancel')
        else:
            return HttpResponseRedirect(reverse('orderitem', kwargs={'order_id' : request.GET['pid']}) + '?status=fail')
    else:
        return HttpResponseBadRequest()


