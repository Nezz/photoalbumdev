from django.db import models
from django.contrib.auth.models import User

#class User(models.Model):
#    mail = models.EmailField(unique=True)
#    name = models.CharField(max_length=255)
    #any additional things we want to know about users

class Album(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    owner = models.ForeignKey(User)

class Slide(models.Model):
    order_number = models.IntegerField(default=0)
    album = models.ForeignKey('Album')

class Photo(models.Model):
    link = models.URLField(max_length=255)
    slide = models.ForeignKey('Slide')

class Order(models.Model):
    time_placed = models.TimeField()
    album = models.ForeignKey('Album')
    owner = models.ForeignKey(User)