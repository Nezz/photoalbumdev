import unittest
from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User
from photoalbum.models import Album, Slide, Photo

class album_tests(TestCase):
    def setUp(self):
        self.client = Client()

        user1 = User.objects.create_user(
            username="admin",
            password='admin',
            email="admin@admin.com")
        user2 = User.objects.create_user(
            username="admin2",
            password='admin2',
            email="admin2@admin.com")
        
        album1 = Album.objects.create(name="New album1", guid="albumone", owner=user1)
        album2 = Album.objects.create(name="New album2", guid="albumtwo", owner=user2)

        for i in range(0,1):
            slide1 = Slide.objects.create(template=0, album=album1)
            for j in range(0,3):
                Photo.objects.create(slide=slide1)

        for j in range(0,3):
            slide2 = Slide.objects.create(template=0, album=album2)
            for i in range(0,1):
                Photo.objects.create(slide=slide2)

    """
     /albums/
	    * GET:
		    * Logged in: List of albums
		    * No login: Login
	    * POST:
		    * New album (Owner only)
    """

    def test_albumsGetNoLogin(self):
        response = self.client.get('/albums/', follow=True)
        self.assertEquals(response.status_code, 200, "Testing request status code")
        self.assertTemplateUsed(response, "login.html", "Testing that the right template was rendered")

    def test_albumsGetLogin(self):
        self.assertTrue(self.client.login(username='admin', password='admin'))
        response = self.client.get('/albums/')
        self.assertEquals(response.status_code, 200, "Testing request status code")
        self.assertTemplateUsed(response, "album_list.html", "Testing that the right template was rendered")

    def test_albumsPostNoLogin(self):
        response = self.client.post('/albums/', follow=True)
        self.assertEquals(response.status_code, 403, "Testing request status code")

    def test_albumsPostLogin(self):
        self.assertTrue(self.client.login(username='admin', password='admin'))
        response = self.client.post('/albums/', follow=True)
        self.assertEquals(response.status_code, 200, "Testing request status code")
        self.assertTemplateUsed(response, "album.html", "Testing that the right template was rendered")

    """
     /albums/<Album ID>/
	    * GET:
		    * Owner login: Album editor
		    * No login: Album viewer
	    * POST: New slide (Owner only)
    """
    def test_albumGetNoLogin(self):
        response = self.client.get('/albums/albumone', follow=True)
        self.assertEquals(response.status_code, 200, "Testing request status code")
        self.assertTemplateUsed(response, "album.html", "Testing that the right template was rendered")
        self.assertNotContains(response, 'id="newslide"')

    def test_albumGetOwner(self):
        self.client.login(username='admin', password='admin')
        response = self.client.get('/albums/albumone', follow=True)
        self.assertEquals(response.status_code, 200, "Testing request status code")
        self.assertTemplateUsed(response, "album.html", "Testing that the right template was rendered")
        self.assertContains(response, 'id="newslide"')

    def test_albumGetNonowner(self):
        self.client.login(username='admin2', password='admin2')
        response = self.client.get('/albums/albumone', follow=True)
        self.assertEquals(response.status_code, 200, "Testing request status code")
        self.assertTemplateUsed(response, "album.html", "Testing that the right template was rendered")
        self.assertNotContains(response, 'id="newslide"')

    def test_albumGetFirstbuttons(self):
        response = self.client.get('/albums/albumtwo/1', follow=True)
        self.assertEquals(response.status_code, 200, "Testing request status code")
        self.assertTemplateUsed(response, "album.html", "Testing that the right template was rendered")
        self.assertNotContains(response, 'moveleft')
        self.assertContains(response, 'moveright')

    def test_albumGetMidbuttons(self):
        response = self.client.get('/albums/albumtwo/2', follow=True)
        self.assertEquals(response.status_code, 200, "Testing request status code")
        self.assertTemplateUsed(response, "album.html", "Testing that the right template was rendered")
        self.assertContains(response, 'moveleft')
        self.assertContains(response, 'moveright')

    def test_albumGetLastbuttons(self):
        response = self.client.get('/albums/albumtwo/3', follow=True)
        self.assertEquals(response.status_code, 200, "Testing request status code")
        self.assertTemplateUsed(response, "album.html", "Testing that the right template was rendered")
        self.assertContains(response, 'moveleft')
        self.assertNotContains(response, 'moveright')

    def test_albumGetDeletebutton(self):
        response = self.client.get('/albums/albumone/1', follow=True)
        self.assertNotContains(response, 'id="deletebutton"')

        response = self.client.get('/albums/albumtwo/1', follow=True)
        self.assertNotContains(response, 'id="deletebutton"')

        self.client.login(username='admin', password='admin')
        response = self.client.get('/albums/albumone/1', follow=True)
        self.assertNotContains(response, 'id="deletebutton"')

        self.client.login(username='admin2', password='admin2')
        response = self.client.get('/albums/albumtwo/1', follow=True)
        self.assertContains(response, 'id="deletebutton"')

    def test_albumPostNoLogin(self):
        response = self.client.post('/albums/albumone/', follow=True)
        self.assertEquals(response.status_code, 403, "Testing request status code")

    def test_albumPostOwner(self):
        self.client.login(username='admin', password='admin')
        response = self.client.post('/albums/albumone/', follow=True)
        self.assertEquals(response.status_code, 200, "Testing request status code")
        self.assertTemplateUsed(response, "album.html", "Testing that the right template was rendered")
        self.assertContains(response, 'id="newslide"')

    def test_albumPostNonowner(self):
        self.client.login(username='admin2', password='admin2')
        response = self.client.post('/albums/albumone/', follow=True)
        self.assertEquals(response.status_code, 403, "Testing request status code")

    """
     /albums/<Album ID>/delete
	    * GET:
		    * Owner login: Are you sure you want to delete?
		    * No login: Login page 
	    * POST: Delete album (Owner only)
    """
    def test_albumDeleteGetNoLogin(self):
        response = self.client.get('/albums/albumone/delete', follow=True)
        self.assertEquals(response.status_code, 200, "Testing request status code")
        self.assertTemplateUsed(response, "login.html", "Testing that the right template was rendered")

    def test_albumDeleteGetOwner(self):
        self.client.login(username='admin', password='admin')
        response = self.client.get('/albums/albumone/delete', follow=True)
        self.assertEquals(response.status_code, 200, "Testing request status code")
        self.assertTemplateUsed(response, "album_delete.html", "Testing that the right template was rendered")

    def test_albumDeleteGetNonowner(self):
        self.client.login(username='admin2', password='admin2')
        response = self.client.get('/albums/albumone/delete', follow=True)
        self.assertEquals(response.status_code, 403, "Testing request status code")

    def test_albumDeletePostNoLogin(self):
        response = self.client.post('/albums/albumone/delete', follow=True)
        self.assertEquals(response.status_code, 403, "Testing request status code")

    def test_albumDeletePostOwner(self):
        self.client.login(username='admin', password='admin')
        response = self.client.post('/albums/albumone/delete', follow=True)
        self.assertEquals(response.status_code, 200, "Testing request status code")
        self.assertTemplateUsed(response, "album_list.html", "Testing that the right template was rendered")

        response = self.client.get('/albums/albumone', follow=True)
        self.assertTemplateUsed(response, "404.html", "Testing that the item was not found")

    def test_albumDeletePostNonowner(self):
        self.client.login(username='admin2', password='admin2')
        response = self.client.post('/albums/albumone/delete', follow=True)
        self.assertEquals(response.status_code, 403, "Testing request status code")

    """
     /albums/<Album ID>/modify
	    * GET:
		    * Owner login: Edit album name
		    * No login: Login page
	    * POST: Modify album name (Owner only)
    """
    def test_albumModifyGetNoLogin(self):
        response = self.client.get('/albums/albumone/modify', follow=True)
        self.assertEquals(response.status_code, 200, "Testing request status code")
        self.assertTemplateUsed(response, "login.html", "Testing that the right template was rendered")

    def test_albumModifyGetOwner(self):
        self.client.login(username='admin', password='admin')
        response = self.client.get('/albums/albumone/modify', follow=True)
        self.assertEquals(response.status_code, 200, "Testing request status code")
        self.assertTemplateUsed(response, "album_modify.html", "Testing that the right template was rendered")

    def test_albumModifyGetNonowner(self):
        self.client.login(username='admin2', password='admin2')
        response = self.client.get('/albums/albumone/modify', follow=True)
        self.assertEquals(response.status_code, 403, "Testing request status code")

    def test_albumModifyPostNoname(self):
        response = self.client.post('/albums/albumone/modify', follow=True)
        self.assertEquals(response.status_code, 400, "Testing request status code")

    def test_albumModifyPostNologin(self):
        response = self.client.post('/albums/albumone/modify', { "name" : "Test album" }, follow=True)
        self.assertEquals(response.status_code, 403, "Testing request status code")

    def test_albumModifyPostOwner(self):
        self.client.login(username='admin', password='admin')
        response = self.client.post('/albums/albumone/modify', { "name" : "Test album" }, follow=True)
        self.assertEquals(response.status_code, 200, "Testing request status code")
        self.assertTemplateUsed(response, "album.html", "Testing that the right template was rendered")
        self.assertContains(response, "Test album")

    def test_albumModifyPostNonowner(self):
        self.client.login(username='admin2', password='admin2')
        response = self.client.post('/albums/albumone/modify', { "name" : "Test album" }, follow=True)
        self.assertEquals(response.status_code, 403, "Testing request status code")

    """
     /albums/<Album ID>/<Slide ID>/delete
	    * GET:
		    * Owner login: Are you sure you want to delete?
		    * No login: Login page 
	    * POST: Delete slide (Owner only)
    """
    def test_slideDeleteGetNoLogin(self):
        response = self.client.get('/albums/albumone/1/delete', follow=True)
        self.assertEquals(response.status_code, 200, "Testing request status code")
        self.assertTemplateUsed(response, "login.html", "Testing that the right template was rendered")

    def test_slideDeleteGetOwner(self):
        self.client.login(username='admin', password='admin')
        response = self.client.get('/albums/albumone/1/delete', follow=True)
        self.assertEquals(response.status_code, 200, "Testing request status code")
        self.assertTemplateUsed(response, "slide_delete.html", "Testing that the right template was rendered")

    def test_slideDeleteGetNonowner(self):
        self.client.login(username='admin2', password='admin2')
        response = self.client.get('/albums/albumone/1/delete', follow=True)
        self.assertEquals(response.status_code, 403, "Testing request status code")

    def test_slideDeletePostNoLogin(self):
        response = self.client.post('/albums/albumone/1/delete', follow=True)
        self.assertEquals(response.status_code, 403, "Testing request status code")

    def test_slideDeletePostOwner(self):
        self.client.login(username='admin2', password='admin2')
        response = self.client.post('/albums/albumtwo/1/delete', follow=True)
        self.assertEquals(response.status_code, 200, "Testing request status code")
        self.assertTemplateUsed(response, "album.html", "Testing that the right template was rendered")

        response = self.client.get('/albums/albumtwo/1', follow=True)
        self.assertEquals(response.status_code, 200, "Testing request status code")
        response = self.client.get('/albums/albumtwo/3', follow=True)
        self.assertTemplateUsed(response, "404.html", "Testing that the item was not found")

    def test_slideDeletePostNonowner(self):
        self.client.login(username='admin2', password='admin2')
        response = self.client.post('/albums/albumone/1/delete', follow=True)
        self.assertEquals(response.status_code, 403, "Testing request status code")

    def test_slideDeletePostSingleslide(self):
        self.client.login(username='admin', password='admin')
        response = self.client.post('/albums/albumone/1/delete', follow=True)
        self.assertEquals(response.status_code, 403, "Testing request status code")

    """
     /albums/<Album ID>/<Slide ID>/modify
	    * GET:
		    * Owner login: Template editor
		    * No login: Login page
	    * POST: Modify order and/or template (Owner only)
    """
    def test_slideModifyGetNoLogin(self):
        response = self.client.get('/albums/albumtwo/1/modify', follow=True)
        self.assertEquals(response.status_code, 200, "Testing request status code")
        self.assertTemplateUsed(response, "login.html", "Testing that the right template was rendered")

    def test_slideModifyGetOwner(self):
        self.client.login(username='admin2', password='admin2')
        response = self.client.get('/albums/albumtwo/1/modify', follow=True)
        self.assertEquals(response.status_code, 200, "Testing request status code")
        self.assertTemplateUsed(response, "slide_modify.html", "Testing that the right template was rendered")

    def test_slideModifyGetNonowner(self):
        self.client.login(username='admin', password='admin')
        response = self.client.get('/albums/albumtwo/1/modify', follow=True)
        self.assertEquals(response.status_code, 403, "Testing request status code")

    def test_slideModifyPostNoparams(self):
        response = self.client.post('/albums/albumtwo/1/modify', follow=True)
        self.assertEquals(response.status_code, 400, "Testing request status code")

    def test_slideModifyPostBadparams(self):
        self.client.login(username='admin2', password='admin2')
        response = self.client.post('/albums/albumtwo/1/modify', { "order" : "4", "template" : "3" }, follow=True)
        self.assertEquals(response.status_code, 400, "Testing request status code")

    def test_slideModifyPostNologin(self):
        response = self.client.post('/albums/albumtwo/1/modify', { "order" : "2", "template" : "3" }, follow=True)
        self.assertEquals(response.status_code, 403, "Testing request status code")

    def test_slideModifyPostOwner(self):
        self.client.login(username='admin2', password='admin2')
        response = self.client.post('/albums/albumtwo/1/modify', { "order" : "2", "template" : "3" }, follow=True)
        self.assertEquals(response.status_code, 200, "Testing request status code")
        self.assertTemplateUsed(response, "album.html", "Testing that the right template was rendered")

        response = self.client.post('/albums/albumtwo/1/modify', { "order" : "2"}, follow=True)
        self.assertEquals(response.status_code, 200, "Testing request status code")
        self.assertTemplateUsed(response, "album.html", "Testing that the right template was rendered")

        response = self.client.post('/albums/albumtwo/1/modify', { "template" : "3" }, follow=True)
        self.assertEquals(response.status_code, 200, "Testing request status code")
        self.assertTemplateUsed(response, "album.html", "Testing that the right template was rendered")
        # TODO: Test if worked

    def test_slideModifyPostNonowner(self):
        self.client.login(username='admin', password='admin')
        response = self.client.post('/albums/albumtwo/1/modify', { "order" : "2", "template" : "3" }, follow=True)
        self.assertEquals(response.status_code, 403, "Testing request status code")

    """
     /albums/<Album ID>/<Slide ID>/<Photo ID>
	    * GET: Url of photo
	    * POST: N/A
    """
    def test_photoGet(self):
        response = self.client.get('/albums/albumone/1/1/')
        self.assertEquals(response.status_code, 302, "Testing request status code")

        response = self.client.get('/albums/albumtwo/2/1/')
        self.assertTemplateUsed(response, "404.html", "Testing that the item was not found")

    """
         /albums/<Album ID>/<Slide ID>/<Photo ID>/delete
        * GET:
            * Owner login: Are you sure you want to delete?
            * No login: Login page 
        * POST: Delete photo (Owner only)
    """
    def test_photoDeleteGetNoLogin(self):
        response = self.client.get('/albums/albumone/1/1/delete', follow=True)
        self.assertEquals(response.status_code, 200, "Testing request status code")
        self.assertTemplateUsed(response, "login.html", "Testing that the right template was rendered")

    def test_photoDeleteGetOwner(self):
        self.client.login(username='admin', password='admin')
        response = self.client.get('/albums/albumone/1/1/delete', follow=True)
        self.assertEquals(response.status_code, 200, "Testing request status code")
        self.assertTemplateUsed(response, "photo_delete.html", "Testing that the right template was rendered")

    def test_photoDeleteGetNonowner(self):
        self.client.login(username='admin2', password='admin2')
        response = self.client.get('/albums/albumone/1/1/delete', follow=True)
        self.assertEquals(response.status_code, 403, "Testing request status code")

    def test_photoDeletePostNoLogin(self):
        response = self.client.post('/albums/albumone/1/1/delete', follow=True)
        self.assertEquals(response.status_code, 403, "Testing request status code")

    def test_photoDeletePostOwner(self):
        self.client.login(username='admin', password='admin')
        response = self.client.post('/albums/albumone/1/1/delete', follow=True)
        self.assertEquals(response.status_code, 200, "Testing request status code")
        self.assertTemplateUsed(response, "album.html", "Testing that the right template was rendered")

        response = self.client.get('/albums/albumone/1/1/', follow=True)
        self.assertTemplateUsed(response, "404.html", "Testing that the item was not found")
        response = self.client.get('/albums/albumone/1/2/')
        self.assertEquals(response.status_code, 302, "Testing request status code")

    def test_photoDeletePostNonowner(self):
        self.client.login(username='admin2', password='admin2')
        response = self.client.post('/albums/albumone/1/1/delete', follow=True)
        self.assertEquals(response.status_code, 403, "Testing request status code")

    """
     /albums/<Album ID>/<Slide ID>/<Photo ID>/modify
	    * GET:
		    * Owner login: URL editor (and future flickr stuff)
		    * No login: Login page 
	    * POST: Modify the url and the description of the photo (Owner only)
    """
    def test_photoModifyGetNoLogin(self):
        response = self.client.get('/albums/albumone/1/1/modify', follow=True)
        self.assertEquals(response.status_code, 200, "Testing request status code")
        self.assertTemplateUsed(response, "login.html", "Testing that the right template was rendered")

    def test_photoModifyGetOwner(self):
        self.client.login(username='admin', password='admin')
        response = self.client.get('/albums/albumone/1/1/modify', follow=True)
        self.assertEquals(response.status_code, 200, "Testing request status code")
        self.assertTemplateUsed(response, "photo_modify.html", "Testing that the right template was rendered")

    def test_photoModifyGetNonowner(self):
        self.client.login(username='admin2', password='admin2')
        response = self.client.get('/albums/albumone/1/1/modify', follow=True)
        self.assertEquals(response.status_code, 403, "Testing request status code")

    def test_photoModifyPostNoparams(self):
        response = self.client.post('/albums/albumone/1/1/modify', follow=True)
        self.assertEquals(response.status_code, 400, "Testing request status code")

    def test_photoModifyPostEmptyparams(self):
        self.client.login(username='admin', password='admin')
        self.client.login(username='admin', password='admin')
        response = self.client.post('/albums/albumone/1/1/modify', { "link" : "", "description" : "" }, follow=True)
        self.assertEquals(response.status_code, 200, "Testing request status code")

    def test_photoModifyPostNologin(self):
        response = self.client.post('/albums/albumone/1/1/modify', { "link" : "http://www.songarc.net", "description" : "test" }, follow=True)
        self.assertEquals(response.status_code, 403, "Testing request status code")

    def test_photoModifyPostOwner(self):
        self.client.login(username='admin', password='admin')
        response = self.client.post('/albums/albumone/1/1/modify', { "link" : "http://www.songarc.net", "description" : "test" }, follow=True)
        self.assertEquals(response.status_code, 200, "Testing request status code")
        self.assertTemplateUsed(response, "album.html", "Testing that the right template was rendered")

        response = self.client.post('/albums/albumone/1/1/modify', { "description" : "test" }, follow=True)
        self.assertEquals(response.status_code, 200, "Testing request status code")
        self.assertTemplateUsed(response, "album.html", "Testing that the right template was rendered")

        response = self.client.post('/albums/albumone/1/1/modify', { "link" : "http://www.songarc.net"}, follow=True)
        self.assertEquals(response.status_code, 200, "Testing request status code")
        self.assertTemplateUsed(response, "album.html", "Testing that the right template was rendered")
        # TODO: Test if worked
   
    def test_photoModifyPostNonowner(self):
        self.client.login(username='admin2', password='admin2')
        response = self.client.post('/albums/albumone/1/1/modify', { "link" : "http://www.songarc.net", "description" : "test"  }, follow=True)
        self.assertEquals(response.status_code, 403, "Testing request status code")
