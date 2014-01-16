from django.shortcuts import render_to_response, get_object_or_404
from photoalbum.models import Album, Slide

def album_list_view(request):
    for i in range (0, 5):
        Album.objects.create(name=("Album " + str(i)), owner=request.user)

    albums = Album.objects.filter(owner=request.user)
    #for a in albums:
    #    slides = Slide.objects.filter(album=a)
    #    a.slides_num = len(slides)
    return render_to_response("album_list.html", {"albums": albums})

def album_view(request, album_id):
    album = get_object_or_404(Album, id=album_id)
    if (album.owner == request.user):
        return render_to_response("album.html", {"album": album}) # TODO: Album editor
    else:
        return render_to_response("album.html", {"album": album}) # TODO: Album viewer