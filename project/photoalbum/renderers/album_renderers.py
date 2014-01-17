from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, Http404
from django.core.context_processors import csrf
from django.core.exceptions import ObjectDoesNotExist
from photoalbum.models import Album, Slide, Photo

def album_list_view(request):
    albums = Album.objects.filter(owner=request.user)
    c = {"albums": albums}
    c.update(csrf(request))
    return render_to_response("album_list.html", c)

def album_view(request, album_id, slide_id=1):
    slide_id = int(slide_id)
    album = get_object_or_404(Album, guid=album_id)

    if len(album.get_slide_order()) < int(slide_id):
        raise Http404();

    slide = get_object_or_404(Slide, pk=album.get_slide_order()[slide_id - 1])

    curr = slide_id

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

    c = {"album": album, "curr" : curr, "next" : next, "prev" : prev, "photos" : photos, "editable" : editable}
    c.update(csrf(request))
    if (album.owner == request.user):
        return render_to_response("album.html", c) # TODO: Album editor
    else:
        return render_to_response("album.html", c) # TODO: Album viewer