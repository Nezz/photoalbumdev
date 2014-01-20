import unittest
from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User

class user_tests(TestCase):
    def setUp(self):
        self.client = Client()
        User.objects.create_user(
            username="admin",
            password='admin',
            email="admin@admin.com")
    
    """
     /
	    ? GET:
		    ? Logged in: List of albums
		    ? No login: Welcome page
	    ? PUT: N/A
	    ? POST: N/A
	    ? DELETE: N/A
    """
    def test_indexGetNoLogin(self):
        response = self.client.get('/')
        self.assertEquals(response.status_code, 200, "Testing request status code")
        self.assertTemplateUsed(response, "welcome.html", "Testing that the right template was rendered")

    def test_indexGetLogin(self):
        self.assertTrue(self.client.login(username='admin', password='admin'))
        response = self.client.get('/', follow=True)
        self.assertEquals(response.status_code, 200, "Testing request status code")
        self.assertTemplateUsed(response, "album_list.html", "Testing that the right template was rendered")

    """
     /login/
	    ? GET: Login page
	    ? PUT: N/A
	    ? POST: Login user
	    ? DELETE: N/A
    """
    def test_loginGetNoLogin(self):
        response = self.client.get('/login/')
        self.assertEquals(response.status_code, 200, "Testing request status code")
        self.assertTemplateUsed(response, "login.html", "Testing that the right template was rendered")

    def test_loginGetLogin(self):
        self.assertTrue(self.client.login(username='admin', password='admin'))
        response = self.client.get('/login/', follow=True)
        self.assertEquals(response.status_code, 200, "Testing request status code")
        self.assertTemplateUsed(response, "album_list.html", "Testing that the right template was rendered")

    def test_loginPostSuccess(self):
        response = self.client.post('/login/', {'username': 'admin', 'password': 'admin'}, follow=True)
        self.assertEquals(response.status_code, 200, "Testing request status code")
        self.assertTemplateUsed(response, "album_list.html", "Testing that the right template was rendered")

    def test_loginPostFail(self):
        response = self.client.post('/login/', {'username': 'test', 'password': 'test'})
        self.assertEquals(response.status_code, 200, "Testing request status code")
        response = self.client.post('/login/', {'username': 'admin', 'password': 'test'})
        self.assertEquals(response.status_code, 200, "Testing request status code")
        # TODO: Invalid password or username

    """
     /register/
	    ? GET: Register page
	    ? PUT: N/A
	    ? POST: Register user
	    ? DELETE: N/A
    """
    def test_registerGetNoLogin(self):
        response = self.client.get('/register/')
        self.assertEquals(response.status_code, 200, "Testing request status code")
        self.assertTemplateUsed(response, "register.html", "Testing that the right template was rendered")

    def test_registerGetLogin(self):
        self.assertTrue(self.client.login(username='admin', password='admin'))
        response = self.client.get('/register/', follow=True)
        self.assertEquals(response.status_code, 200, "Testing request status code")
        self.assertTemplateUsed(response, "album_list.html", "Testing that the right template was rendered")

    def test_registerPostSuccess(self):
        response = self.client.post('/register/', {'username': 'admin2', 'password': 'admin2', 'email' : 'admin2@admin.com' }, follow=True)
        self.assertEquals(response.status_code, 200, "Testing request status code")
        self.assertTemplateUsed(response, "login.html", "Testing that the right template was rendered")

    def test_registerPostFail(self):
        response = self.client.post('/register/', {'username': 'admin', 'password': 'admin', 'email' : 'admin@admin.com' })
        self.assertNotEquals(response.status_code, 200, "Testing request status code")
        # TODO: Username already exists

    """
     /logout/
 	    ? GET: Logout user
	    ? PUT: N/A
	    ? POST: N/A
	    ? DELETE: N/A
    """
    def test_logoutGetNoLogin(self):
        response = self.client.get('/logout/', follow=True)
        self.assertEquals(response.status_code, 200, "Testing request status code")
        self.assertTemplateUsed(response, "welcome.html", "Testing that the right template was rendered")

    def test_logoutGetLogin(self):
        self.assertTrue(self.client.login(username='admin', password='admin'))
        response = self.client.get('/logout/', follow=True)
        self.assertEquals(response.status_code, 200, "Testing request status code")
        self.assertTemplateUsed(response, "welcome.html", "Testing that the right template was rendered")

if __name__ == '__main__':
    unittest.main()