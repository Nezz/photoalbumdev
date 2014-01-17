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
     /<Album ID>/
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
        self.assertNotContains(response, 'id="prevbutton"')
        self.assertContains(response, 'id="nextbutton"')

    def test_albumGetMidbuttons(self):
        response = self.client.get('/albums/albumtwo/2', follow=True)
        self.assertEquals(response.status_code, 200, "Testing request status code")
        self.assertTemplateUsed(response, "album.html", "Testing that the right template was rendered")
        self.assertContains(response, 'id="prevbutton"')
        self.assertContains(response, 'id="nextbutton"')

    def test_albumGetLastbuttons(self):
        response = self.client.get('/albums/albumtwo/3', follow=True)
        self.assertEquals(response.status_code, 200, "Testing request status code")
        self.assertTemplateUsed(response, "album.html", "Testing that the right template was rendered")
        self.assertContains(response, 'id="prevbutton"')
        self.assertNotContains(response, 'id="nextbutton"')

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
     /<Album ID>/delete
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
        self.assertTemplateUsed(response, "template.html", "Testing that the right template was rendered") # TODO

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
        self.assertEquals(response.status_code, 404, "Testing request status code")

    def test_albumDeletePostNonowner(self):
        self.client.login(username='admin2', password='admin2')
        response = self.client.post('/albums/albumone/delete', follow=True)
        self.assertEquals(response.status_code, 403, "Testing request status code")

    """
     /<Album ID>/modify
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
        self.assertTemplateUsed(response, "template.html", "Testing that the right template was rendered") # TODO

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
     /<Album ID>/<Slide ID>/delete
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
        self.assertTemplateUsed(response, "template.html", "Testing that the right template was rendered") # TODO

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
        self.assertEquals(response.status_code, 404, "Testing request status code")

    def test_slideDeletePostNonowner(self):
        self.client.login(username='admin2', password='admin2')
        response = self.client.post('/albums/albumone/1/delete', follow=True)
        self.assertEquals(response.status_code, 403, "Testing request status code")

    def test_slideDeletePostSingleslide(self):
        self.client.login(username='admin', password='admin')
        response = self.client.post('/albums/albumone/1/delete', follow=True)
        self.assertEquals(response.status_code, 403, "Testing request status code")