from django.shortcuts import render_to_response
from photoalbum.models import Order, Album
from django.core.context_processors import csrf
from django.template import RequestContext
import datetime
import md5

def ordernew_view(request, album):
    c = {"album" : album }
    c.update(csrf(request))
    return render_to_response("order_new.html", RequestContext(request, c))

def order_list_view(request):
    orders = Order.objects.filter(owner=request.user)
    c = {"orders": orders}
    c.update(csrf(request))
    return render_to_response("order_list.html", RequestContext(request, c))

def orderitem_view(request, order):
    c = {"order": order}
    c.update(csrf(request))

    #checksum - for the payment
    if (order.statusCode < 2):
        checksum_str = "pid=%s&sid=%s&amount=%s&token=%s"%(order.pk, "vladimirorekhov", 10, "1fff5d006fb58357dfac5f24c8c6e2b7")
        m = md5.new(checksum_str)
        checksum = m.hexdigest()
        c.update({"checksum" : checksum})

    return render_to_response("order.html", RequestContext(request, c))

def orderdelete_view(request, order):
    c = {"order": order}
    c.update(csrf(request))
    return render_to_response("order_delete.html", RequestContext(request, c))
