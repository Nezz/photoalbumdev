from django.shortcuts import render_to_response
from photoalbum.models import Order, Album
from django.core.context_processors import csrf
from django.template import RequestContext
import datetime

now = datetime.datetime.now()

def order_list_view(request):
    orders = Order.objects.filter(owner=request.user)
    c = {"orders": orders}
    c.update(csrf(request))
    return render_to_response("order_list.html", RequestContext(request, c))

def order_create_view(request, album_id):
    Order.objects.create(owner=request.user, album=Album.objects.get(guid=album_id), time_placed=datetime.datetime.now())

    orders = Order.objects.filter(owner=request.user)
    c = {"orders": orders}
    c.update(csrf(request))
    return render_to_response("order_list.html", RequestContext(request, c))