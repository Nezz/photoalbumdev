from django.http import HttpResponse, Http404, HttpResponseForbidden, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.template import Context
from photoalbum.rest import rest_helper
from photoalbum.renderers.album_renderers import *

"""
 /<Album ID>/
	? GET:
		? Owner login: Album editor
		? No login: Album viewer
	? PUT: N/A
	? POST: New slide (Owner only)
	? DELETE: Delete album (Owner only)
"""
def albumitemHandler(request, album_id):
    return rest_helper(albumitemGet, None, albumitemPost, albumitemDelete, request, album_id)

def albumitemGet(request, album_id):
    return album_view(request, album_id)

def albumitemPost(request):
    raise Http404(); # TODO

def albumitemDelete(request):
    raise Http404(); # TODO

"""
 /<Album ID>/<Slide ID>
	? GET:
		? Owner login: Album editor at specific slide
		? No login: Album viewer at specific slide
	? PUT: Modify order and template (Owner only)
	? POST: N/A
	? DELETE: Delete slide (owner only)
"""
def slideitemHandler(request, album_id, slide_id):
    return rest_helper(slideitemGet, None, slideitemPost, slideitemDelete, request, album_id, slide_id)

def slideitemGet(request, album_id, slide_id):
    raise Http404(); # TODO

def slideitemPost(request):
    raise Http404(); # TODO

def slideitemDelete(request):
    raise Http404(); # TODO

"""
 /<Album ID>/<Slide ID>/modify
	? GET:
		? Owner login: Template editor
		? No login: Login page
	? PUT: N/A
	? POST: N/A
	? DELETE: N/A
"""
def slidemodifyHandler(request, album_id, slide_id):
    return rest_helper(slidemodifyGet, None, None, None, request, album_id, slide_id)

def slidemodifyGet(request, album_id, slide_id):
    raise Http404(); # TODO

"""
 /<Album ID>/<Slide ID>/<Photo ID>
	? GET: Url of photo
	? PUT: N/A
	? POST: N/A
	? DELETE: N/A
"""
def slidephotoHandler(request, album_id, slide_id, photo_id):
    return rest_helper(slidephotoGet, None, None, None, request, album_id, slide_id, photo_id)

def slidephotoGet(request, album_id, slide_id, photo_id):
    raise Http404(); # TODO

"""
 /<Album ID>/<Slide ID>/<Photo ID>/modify
	? GET:
		? Owner login: URL editor (and future flickr stuff)
		? No login: Login page 
	? PUT: N/A
	? POST: N/A
	? DELETE: N/A
"""
def slidephotomodifyHandler(request, album_id, slide_id, photo_id):
    return rest_helper(slidemodifyGet, None, None, None, request, album_id, slide_id, photo_id)

def slidephotomodifyGet(request, album_id, slide_id, photo_id):
    raise Http404(); # TODO
