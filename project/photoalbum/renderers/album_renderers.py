from django.shortcuts import render_to_response, get_object_or_404
from django.core.context_processors import csrf
from photoalbum.models import Album, Slide

def album_list_view(request):
    albums = Album.objects.filter(owner=request.user)
    c = {"albums": albums}
    c.update(csrf(request))
    return render_to_response("album_list.html", c)

def album_view(request, album_id):
    album = get_object_or_404(Album, id=album_id)
    if (album.owner == request.user):
        return render_to_response("album.html", {"album": album}) # TODO: Album editor
    else:
        return render_to_response("album.html", {"album": album}) # TODO: Album viewer