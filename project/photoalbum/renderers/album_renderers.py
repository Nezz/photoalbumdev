from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, Http404
from django.core.context_processors import csrf
from django.core.exceptions import ObjectDoesNotExist
from django.template import RequestContext
from photoalbum.models import Album, Slide, Photo
from photoalbum.utils import get_slide_or_404

def album_list_view(request):
    albums = Album.objects.filter(owner=request.user)
    c = {"albums": albums}
    c.update(csrf(request))
    return render_to_response("album_list.html", RequestContext(request, c))

def album_view(request, album_id, slide_id=1):
    slide_id = int(slide_id)
    album = get_object_or_404(Album, guid=album_id)

    slide = get_slide_or_404(album, slide_id)

    curr = slide_id
    maxSlide = len(album.get_slide_order())
    paginators = range(max(1, curr - 3), min(maxSlide, curr + 3) + 1)

    if (slide_id > 1):
        prev = slide_id - 1
    else:
        prev = None

    if (slide_id < len(album.get_slide_order())):
        next = slide_id + 1
    else:
        next = None

    photos = Photo.objects.filter(slide=slide)
    editable = album.owner == request.user

    c = {"album" : album, "curr" : curr, "next" : next, "prev" : prev, "max" : maxSlide, "paginators" : paginators, "photos" : photos, "editable" : editable}
    c.update(csrf(request))

    return render_to_response("album.html", RequestContext(request, c))

def albumdelete_view(request, album):
    c = {"album" : album }
    c.update(csrf(request))
    return render_to_response("album_delete.html", RequestContext(request, c))

def albummodify_view(request, album):
    c = {"album" : album }
    c.update(csrf(request))
    return render_to_response("album_modify.html", RequestContext(request, c))

def slidedelete_view(request, album, slide_id):
    slide = get_slide_or_404(album, slide_id)
    c = {"album" : album, "slide" : slide, "slide_id" : slide_id}
    c.update(csrf(request))
    return render_to_response("slide_delete.html", RequestContext(request, c))

def slidemodify_view(request, album, slide_id):
    slide = get_slide_or_404(album, slide_id)
    c = {"album" : album, "slide" : slide, "slide_id" : slide_id}
    c.update(csrf(request))
    return render_to_response("slide_modify.html", RequestContext(request, c))

def photomodify_view(request, album, slide_id, photo_id):
    slide = get_slide_or_404(album, slide_id)
    photo = get_object_or_404(Photo, pk=photo_id, slide=slide)
    c = {"album" : album, "slide" : slide, "slide_id" : slide_id, "photo" : photo }
    c.update(csrf(request))
    return render_to_response("photo_modify.html", RequestContext(request, c))
