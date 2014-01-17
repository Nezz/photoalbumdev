from django.http import HttpResponse, Http404, HttpResponseForbidden, HttpResponseRedirect, HttpResponseBadRequest
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.template import Context
from photoalbum.rest import rest_helper
from photoalbum.renderers.album_renderers import *
from photoalbum.models import Album, Slide, Photo

"""
 /<Album ID>/
	* GET:
		* Owner login: Album editor
		* No login: Album viewer
	* POST: New slide (Owner only)
"""
def albumitemHandler(request, album_id):
    return rest_helper(albumitemGet, albumitemPost, request, album_id)

def albumitemGet(request, album_id):
    return album_view(request, album_id)

def albumitemPost(request, album_id):
    album = Album.objects.get(guid=album_id)
    if album.owner == request.user:
        newSlide = Slide.objects.create(template=0, album=album)
        for i in range(0,4):
            Photo.objects.create(slide=newSlide)

        return HttpResponseRedirect('/albums/' + str(album_id) + '/' + str(len(album.get_slide_order())))
    else:
        return HttpResponseForbidden();

"""
 /<Album ID>/delete
	* GET:
		* Owner login: Are you sure you want to delete?
		* No login: Login page 
	* POST: Delete album (Owner only)
"""
def albumdeleteHandler(request, album_id):
    return rest_helper(albumdeleteGet, albumdeletePost, request, album_id)

def albumdeleteGet(request, album_id):
    album = get_object_or_404(Album, guid=album_id)
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/')
    elif album.owner == request.user:
        raise Http404(); # TODO
    else:
        return HttpResponseForbidden()

def albumdeletePost(request, album_id):
    album = get_object_or_404(Album, guid=album_id)
    if album.owner == request.user:
        album.delete()
        return HttpResponseRedirect('/albums/')
    else:
        return HttpResponseForbidden()

"""
 /<Album ID>/modify
	* GET:
		* Owner login: Edit album name
		* No login: Login page
	* POST: Modify album name (Owner only)
"""
def albummodifyHandler(request, album_id):
    return rest_helper(albummodifyGet, albummodifyPost, request, album_id)

def albummodifyGet(request, album_id):
    album = get_object_or_404(Album, guid=album_id)
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/')
    elif album.owner == request.user:
        raise Http404(); # TODO
    else:
        return HttpResponseForbidden()

def albummodifyPost(request, album_id):
    if 'name' in request.POST and request.POST['name']:
        album = get_object_or_404(Album, guid=album_id)
        if album.owner == request.user:
            album.name = request.POST['name']
            album.save()
            return HttpResponseRedirect('/albums/' + str(album_id))
        else:
            return HttpResponseForbidden()
    else:
        return HttpResponseBadRequest()

"""
 /<Album ID>/<Slide ID>
	* GET:
		* Owner login: Album editor at specific slide
		* No login: Album viewer at specific slide
	* POST: N/A
"""
def slideitemHandler(request, album_id, slide_id):
    return rest_helper(slideitemGet, None, request, album_id, slide_id)

def slideitemGet(request, album_id, slide_id):
    return album_view(request, album_id, slide_id)

"""
 /<Album ID>/<Slide ID>/delete
	* GET:
		* Owner login: Are you sure you want to delete?
		* No login: Login page 
	* POST: Delete slide (Owner only)
"""
def slidedeleteHandler(request, album_id, slide_id):
    return rest_helper(slidedeleteGet, slidedeletePost, request, album_id, slide_id)

def slidedeleteGet(request, album_id, slide_id):
    album = Album.objects.get(guid = album_id)
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/')
    elif album.owner == request.user:
        raise Http404(); # TODO
    else:
        return HttpResponseForbidden()

def slidedeletePost(request, album_id, slide_id):
    album = get_object_or_404(Album, guid=album_id)
    if album.owner == request.user and len(album.get_slide_order()) > 1:
        if len(album.get_slide_order()) < int(slide_id):
            raise Http404();
        else:
            slide = get_object_or_404(Slide, pk=album.get_slide_order()[int(slide_id) - 1])
            slide.delete();
            return HttpResponseRedirect('/albums/' + str(album_id))
    else:
        return HttpResponseForbidden()

"""
 /<Album ID>/<Slide ID>/modify
	* GET:
		* Owner login: Template editor
		* No login: Login page
	* POST: Modify order and template (Owner only)
"""
def slidemodifyHandler(request, album_id, slide_id):
    return rest_helper(slidemodifyGet, slidemodifyPost, request, album_id, slide_id)

def slidemodifyGet(request, album_id, slide_id):
    raise Http404(); # TODO

def slidemodifyPost(request, album_id, slide_id):
    raise Http404(); # TODO

"""
 /<Album ID>/<Slide ID>/<Photo ID>
	* GET: Url of photo
	* POST: N/A
"""
def slidephotoHandler(request, album_id, slide_id, photo_id):
    return rest_helper(slidephotoGet, None, request, album_id, slide_id, photo_id)

def slidephotoGet(request, album_id, slide_id, photo_id):
    photo = Photo.objects.get(pk=photo_id)
    return HttpResponseRedirect(photo.link)

"""
 /<Album ID>/<Slide ID>/<Photo ID>/modify
	* GET:
		* Owner login: URL editor (and future flickr stuff)
		* No login: Login page 
	* POST: Modify the url of the photo (Owner only)
"""
def slidephotomodifyHandler(request, album_id, slide_id, photo_id):
    return rest_helper(slidemodifyGet, slidephotomodifyGet, request, album_id, slide_id, photo_id)

def slidephotomodifyGet(request, album_id, slide_id, photo_id):
    raise Http404(); # TODO

def slidephotomodifyPost(request, album_id, slide_id, photo_id):
    raise Http404(); # TODO
