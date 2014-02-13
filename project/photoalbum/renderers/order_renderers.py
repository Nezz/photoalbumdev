from django.shortcuts import render_to_response
from photoalbum.models import Order, Album
from django.core.context_processors import csrf
from django.template import RequestContext
import datetime
import random
import string

now = datetime.datetime.now()

def order_list_view(request):
    orders = Order.objects.filter(owner=request.user)
    c = {"orders": orders}
    c.update(csrf(request))
    return render_to_response("order_list.html", RequestContext(request, c))


#def order_view(request):
#    order = Order.objects.filter(pk=request.order_id)
#    c = {"order": order}
#    c.update(csrf(request))
#    return render_to_response("order.html", RequestContext(request, c))

def order_create_view(request, album_id):


    album_original = Album.objects.get(guid=album_id)

    #how to generate a new pk which is proven to be non existant?
    pk_new = album_original.pk 
    exists = True
    while exists:
        try:
            a = Album.objects.get(pk=pk_new)
        except Album.DoesNotExist:
            a = None
        if a is None:
            exists = False
        else:
            pk_new += 1

    album_original.pk = pk_new
    album_original.name += " order copy"
    album_original.owner = None

    guid = ''.join(random.choice(string.ascii_lowercase + string.digits) for x in range(8))
    album_original.guid = guid
    album_original.save()

    Order.objects.create(owner=request.user, album=Album.objects.get(guid=guid), time_placed=datetime.datetime.now())

    orders = Order.objects.filter(owner=request.user)
    c = {"orders": orders}
    c.update(csrf(request))
    return render_to_response("order_list.html", RequestContext(request, c))