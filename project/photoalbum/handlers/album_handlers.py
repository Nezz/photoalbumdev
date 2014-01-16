from django.http import HttpResponse, Http404, HttpResponseForbidden, HttpResponseRedirect
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
    raise Http404(); # TODO

"""
 /<Album ID>/delete
	* GET:
		* Owner login: Are you sure you want to delete?
		* No login: Login page 
	* POST: Delete album (Owner only)
"""
def albumitemdeleteHandler(request, album_id):
    return rest_helper(albumitemdeleteGet, albumitemdeletePost, request, album_id)

def albumitemdeleteGet(request, album_id):
    raise Http404(); # TODO

def albumitemdeletePost(request, album_id):
    Album.objects.get(pk = album_id).delete()
    return HttpResponseRedirect('/albums/')

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
    raise Http404(); # TODO

"""
 /<Album ID>/<Slide ID>/delete
	* GET:
		* Owner login: Are you sure you want to delete?
		* No login: Login page 
	* POST: Delete slide (Owner only)
"""
def slidedeleteHandler(request, album_id, slide_id):
    return rest_helper(slidedeleteGet, None, slidedeletePost, None, request, album_id, slide_id)

def slidedeleteGet(request, album_id, slide_id):
    raise Http404(); # TODO

def slidedeletePost(request):
    Album.delete(pk = album_id)
    return HttpResponseRedirect('/albums/')

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

def slidemodifyPost(request):
    raise Http404(); # TODO

"""
 /<Album ID>/<Slide ID>/<Photo ID>
	* GET: Url of photo
	* POST: N/A
"""
def slidephotoHandler(request, album_id, slide_id, photo_id):
    return rest_helper(slidephotoGet, None, request, album_id, slide_id, photo_id)

def slidephotoGet(request, album_id, slide_id, photo_id):
    raise Http404(); # TODO

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
