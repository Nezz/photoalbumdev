from django.http import HttpResponse, Http404, HttpResponseForbidden, HttpResponseRedirect, HttpResponseBadRequest
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.template import Context
from photoalbum.utils import rest_helper, get_slide_or_404
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
        return HttpResponseRedirect(reverse('login'))

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
        newSlide = Slide.objects.create(template=1, album=album, maxphoto=10)
        if 'after' in request.POST:
            order = album.get_slide_order()
            order.insert(int(request.POST['after']), order.pop(len(order) - 1))
            album.set_slide_order(order)
            newId = int(request.POST['after']) + 1
        else:
            newId = len(album.get_slide_order())

        return HttpResponseRedirect(reverse('slideitem', kwargs={'album_id' : album_id, 'slide_id' : newId}))
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
    if request.is_ajax() or album.owner == request.user:
        return albumdelete_view(request, album)
    elif not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('login'))
    else:
        return HttpResponseForbidden()

def albumdeletePost(request, album_id):
    album = get_object_or_404(Album, guid=album_id)
    if album.owner == request.user:
        album.delete()
        return HttpResponseRedirect(reverse('albumlist'))
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
    if request.is_ajax() or album.owner == request.user:
        return albummodify_view(request, album)
    elif not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('login'))
    else:
        return HttpResponseForbidden()

def albummodifyPost(request, album_id):
    if 'name' in request.POST and request.POST['name']:
        album = get_object_or_404(Album, guid=album_id)
        if album.owner == request.user:
            album.name = request.POST['name']
            album.save()
            return HttpResponseRedirect(reverse('albumitem', kwargs={'album_id' : album_id}))
        else:
            return HttpResponseForbidden()
    else:
        return HttpResponseBadRequest()

"""
 /albums/<Album ID>/<Slide ID>
	* GET:
		* Owner login: Album editor at specific slide
		* No login: Album viewer at specific slide
	* POST: New photo (owner only)
"""
def slideitemHandler(request, album_id, slide_id):
    return rest_helper(slideitemGet, slideitemPost, request, album_id, slide_id)

def slideitemGet(request, album_id, slide_id):
    return album_view(request, album_id, slide_id)

def slideitemPost(request, album_id, slide_id):
    album = get_object_or_404(Album, guid=album_id)
    if album.owner == request.user:
        slide = get_slide_or_404(album, slide_id)
        Photo.objects.create(slide=slide, height=100, width=100, left=0, top=0)
        return HttpResponseRedirect(reverse('slideitem', kwargs={'album_id' : album_id, 'slide_id' : slide_id}))
    else:
        return HttpResponseForbidden();

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
    if request.is_ajax() or album.owner == request.user:
        return slidedelete_view(request, album, slide_id)
    elif not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('login'))
    else:
        return HttpResponseForbidden()

def slidedeletePost(request, album_id, slide_id):
    album = get_object_or_404(Album, guid=album_id)
    if album.owner == request.user and len(album.get_slide_order()) > 1: # Only allow delete if this isn't the only slide
        slide = get_slide_or_404(album, slide_id)
        slide.delete();
        return HttpResponseRedirect(reverse('albumitem', kwargs={'album_id' : album_id}))
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
    if request.is_ajax() or album.owner == request.user:
        return slidemodify_view(request, album, slide_id)
    elif not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('login'))
    else:
        return HttpResponseForbidden()

def slidemodifyPost(request, album_id, slide_id):
    hasOrder = 'order' in request.POST and request.POST['order'];
    hasTemplate = 'template' in request.POST and request.POST['template']
    if hasOrder or hasTemplate:
        album = get_object_or_404(Album, guid=album_id)
        if album.owner == request.user:
            if hasOrder and int(request.POST['order']) > len(album.get_slide_order()):
                return HttpResponseBadRequest()
            else:
                slide = get_slide_or_404(album, slide_id)

                if hasTemplate:                  
                    slide.template = int(request.POST['template'])
                    if slide.template == 1:
                    	slide.maxphoto = 2
                    elif slide.template == 2:
                    	slide.maxphoto = 3
                    else:
                    	slide.maxphoto = 4
                    slide.save()

                if hasOrder:
                    order = album.get_slide_order()
                    order.insert(int(request.POST['order']) - 1, order.pop(int(slide_id) - 1))
                    album.set_slide_order(order)
                    newId = request.POST['order']
                    
                else:
                    newId = slide_id

                return HttpResponseRedirect(reverse('slideitem', kwargs={'album_id' : album_id, 'slide_id' : newId}))
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
    album = get_object_or_404(Album, guid=album_id)
    slide = get_slide_or_404(album, slide_id)
    photo = get_object_or_404(Photo, pk=photo_id, slide=slide)
    return HttpResponseRedirect(photo.link)

"""
 /albums/<Album ID>/<Slide ID>/<Photo ID>/delete
	* GET:
		* Owner login: Are you sure you want to delete?
		* No login: Login page 
	* POST: Delete photo (Owner only)
"""
def slidephotodeleteHandler(request, album_id, slide_id, photo_id):
    return rest_helper(slidephotodeleteGet, slidephotodeletePost, request, album_id, slide_id, photo_id)

def slidephotodeleteGet(request, album_id, slide_id, photo_id):
    album = get_object_or_404(Album, guid=album_id)
    if request.is_ajax() or album.owner == request.user:
        return photodelete_view(request, album, slide_id, photo_id)
    elif not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('login'))
    else:
        return HttpResponseForbidden()

def slidephotodeletePost(request, album_id, slide_id, photo_id):
    album = get_object_or_404(Album, guid=album_id)
    if album.owner == request.user:
        slide = get_slide_or_404(album, slide_id)
        photo = get_object_or_404(Photo, pk=photo_id, slide=slide)
        photo.delete()
        return HttpResponseRedirect(reverse('albumitem', kwargs={'album_id' : album_id}))
    else:
        return HttpResponseForbidden()

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
    if request.is_ajax() or album.owner == request.user:
        return photomodify_view(request, album, slide_id, photo_id)
    elif not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('login'))
    else:
        return HttpResponseForbidden()

def slidephotomodifyPost(request, album_id, slide_id, photo_id):
    if 'description' in request.POST or 'link' in request.POST or 'height' in request.POST or 'width' in request.POST or 'left' in request.POST or 'top' in request.POST: # May be empty, no need to check
        album = get_object_or_404(Album, guid=album_id)
        if album.owner == request.user:
            slide = get_slide_or_404(album, slide_id)

            photo = get_object_or_404(Photo, pk=photo_id, slide=slide)

            if 'description' in request.POST:
                photo.description = str(request.POST['description'])
            if 'link' in request.POST:
                photo.link = str(request.POST['link'])
            if 'height' in request.POST:
            	photo.height = int(request.POST['height'])
            if 'width' in request.POST:
            	photo.width = int(request.POST['width'])
            if 'left' in request.POST:
            	photo.left = int(request.POST['left'])
            if 'top' in request.POST:
            	photo.top = int(request.POST['top'])
            
            photo.save()
            return HttpResponseRedirect(reverse('slideitem', kwargs={'album_id' : album_id, 'slide_id' : slide_id}))
        else:
            return HttpResponseForbidden()
    else:
        return HttpResponseBadRequest()
