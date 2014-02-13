from django.shortcuts import render_to_response
from photoalbum.models import Order, Album
from django.core.context_processors import csrf
from django.template import RequestContext
from photoalbum.utils import get_payment_checksum
import datetime

def ordernew_view(request, album):
    c = {"album" : album }
    c.update(csrf(request))
    return render_to_response("order_new.html", RequestContext(request, c))

def order_list_view(request):
    orders = Order.objects.filter(owner=request.user)
    c = {"orders" : orders}
    c.update(csrf(request))
    return render_to_response("order_list.html", RequestContext(request, c))

def orderitem_view(request, order, paymentStatus):
    if paymentStatus == "success":
        message = "Thank you for paying for your order. It will be shipped to you soon."
    elif paymentStatus == "cancel":
        message = "The payment for the album has been cancelled."
    elif paymentStatus == "error":
        message = "There was an error during the payment. Please try again in a few minutes."
    elif paymentStatus == "fail":
        message = "Your payment could not be vertified. Please contact the payment provider if the problem persists."
    else:
        message = None

    c = {"order" : order, "message" : message}
    c.update(csrf(request))

    #checksum - for the payment
    if (order.payment_ref is None):
        checksum = get_payment_checksum(order.pk)
        c.update({"checksum" : checksum})

    return render_to_response("order.html", RequestContext(request, c))

def orderdelete_view(request, order):
    c = {"order" : order}
    c.update(csrf(request))
    return render_to_response("order_delete.html", RequestContext(request, c))
