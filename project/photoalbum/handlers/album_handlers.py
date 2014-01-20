from django.http import HttpResponse, Http404, HttpResponseForbidden, HttpResponseRedirect, HttpResponseBadRequest
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.template import Context
from photoalbum.rest import rest_helper
from photoalbum.renderers.album_renderers import *
from photoalbum.models import Album, Slide, Photo
import random
import string

"""
 /albums/
	* GET:
		* Logged in: List of albums
		* No login: Login
	* POST:
		* New album (Owner only)
"""
def albumlistHandler(request):
    return rest_helper(albumlistGet, albumlistPost, request)

def albumlistGet(request):
    if request.user.is_authenticated():
        return album_list_view(request)
    else:
        return HttpResponseRedirect('/login/')

def albumlistPost(request):
    if request.user.is_authenticated():
        guid = ''.join(random.choice(string.ascii_lowercase + string.digits) for x in range(8))
        newAlbum = Album.objects.create(name="My album", guid=guid, owner=request.user)
        return albumitemPost(request, newAlbum.guid)
    else:
        return HttpResponseForbidden();

"""
 /albums/<Album ID>/
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
    album = get_object_or_404(Album, guid=album_id)
    if album.owner == request.user:
        newSlide = Slide.objects.create(template=0, album=album)
        for i in range(0,4):
            Photo.objects.create(slide=newSlide)

        return HttpResponseRedirect('/albums/' + str(album_id) + '/' + str(len(album.get_slide_order())))
    else:
        return HttpResponseForbidden();

"""
 /albums/<Album ID>/delete
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
 /albums/<Album ID>/modify
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
 /albums/<Album ID>/<Slide ID>
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
 /albums/<Album ID>/<Slide ID>/delete
	* GET:
		* Owner login: Are you sure you want to delete?
		* No login: Login page 
	* POST: Delete slide (Owner only)
"""
def slidedeleteHandler(request, album_id, slide_id):
    return rest_helper(slidedeleteGet, slidedeletePost, request, album_id, slide_id)

def slidedeleteGet(request, album_id, slide_id):
    album = get_object_or_404(Album, guid=album_id)
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
 /albums/<Album ID>/<Slide ID>/modify
	* GET:
		* Owner login: Template editor
		* No login: Login page
	* POST: Modify order and template (Owner only)
"""
def slidemodifyHandler(request, album_id, slide_id):
    return rest_helper(slidemodifyGet, slidemodifyPost, request, album_id, slide_id)

def slidemodifyGet(request, album_id, slide_id):
    album = get_object_or_404(Album, guid=album_id)
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/')
    elif album.owner == request.user:
        raise Http404(); # TODO
    else:
        return HttpResponseForbidden()

def slidemodifyPost(request, album_id, slide_id):
    if 'order' in request.POST and request.POST['order'] and 'template' in request.POST and request.POST['template']:
        album = get_object_or_404(Album, guid=album_id)
        if album.owner == request.user and len(album.get_slide_order()) > 1:
            if len(album.get_slide_order()) < int(slide_id):
                raise Http404();
            elif int(request.POST['order']) > len(album.get_slide_order()):
                return HttpResponseBadRequest()
            else:
                slide = get_object_or_404(Slide, pk=album.get_slide_order()[int(slide_id) - 1])

                slide.template = int(request.POST['template'])
                slide.save()

                order = album.get_slide_order()
                order.insert(int(request.POST['order']) - 1, order.pop(int(slide_id) - 1))
                album.set_slide_order(order)
                return HttpResponseRedirect('/albums/' + str(album_id) +  '/' + request.POST['order'])
        else:
            return HttpResponseForbidden()
    else:
        return HttpResponseBadRequest()

"""
 /albums/<Album ID>/<Slide ID>/<Photo ID>
	* GET: Url of photo
	* POST: N/A
"""
def slidephotoHandler(request, album_id, slide_id, photo_id):
    return rest_helper(slidephotoGet, None, request, album_id, slide_id, photo_id)

def slidephotoGet(request, album_id, slide_id, photo_id):
    slide_id = int(slide_id)
    album = get_object_or_404(Album, guid=album_id)

    if len(album.get_slide_order()) < int(slide_id):
        raise Http404();

    slide = get_object_or_404(Slide, pk=album.get_slide_order()[slide_id - 1])
    photo = get_object_or_404(Photo, pk=photo_id, slide=slide)
    return HttpResponseRedirect(photo.link)

"""
 /albums/<Album ID>/<Slide ID>/<Photo ID>/modify
	* GET:
		* Owner login: URL editor (and future flickr stuff)
		* No login: Login page 
	* POST: Modify the url and the description of the photo (Owner only)
"""
def slidephotomodifyHandler(request, album_id, slide_id, photo_id):
    return rest_helper(slidephotomodifyGet, slidephotomodifyPost, request, album_id, slide_id, photo_id)

def slidephotomodifyGet(request, album_id, slide_id, photo_id):
    album = get_object_or_404(Album, guid=album_id)
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/')
    elif album.owner == request.user:
        raise Http404(); # TODO
    else:
        return HttpResponseForbidden()

def slidephotomodifyPost(request, album_id, slide_id, photo_id):
    if 'description' in request.POST or 'link' in request.POST: # May be empty, no need to check
        album = get_object_or_404(Album, guid=album_id)
        if album.owner == request.user:
            slide_id = int(slide_id)
            if len(album.get_slide_order()) < slide_id:
                raise Http404();

            slide = get_object_or_404(Slide, pk=album.get_slide_order()[slide_id - 1])

            photo = get_object_or_404(Photo, pk=photo_id, slide=slide)

            photo.description = str(request.POST['description'])
            photo.link = str(request.POST['link']) # TODO: Verify if valid link to an image
            photo.save()
            return HttpResponseRedirect('/albums/' + str(album_id) + '/' + str(slide_id))
        else:
            return HttpResponseForbidden()
    else:
        return HttpResponseBadRequest()
