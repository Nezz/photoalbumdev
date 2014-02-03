from django.db import models
from django.contrib.auth.models import User

#class User(models.Model):
#    mail = models.EmailField(unique=True)
#    name = models.CharField(max_length=255)
    #any additional things we want to know about users

class Album(models.Model):
    name = models.CharField(max_length=255)
    guid = models.CharField(max_length=8, db_index=True)
    owner = models.ForeignKey(User)

    def __str__(self):
        return 'Album "%s" by %s (GUID: %s, ID: %s)' % (self.name, self.owner, self.guid, self.pk)

class Slide(models.Model):
    template = models.IntegerField(default=1)
    maxphoto = models.IntegerField(default=2)
    album = models.ForeignKey('Album')

    def __str__(self):
        return 'Slide (ID: %s) for album %s' % (self.pk, str(self.album))

    class Meta:
        order_with_respect_to = 'album'

class Photo(models.Model):
    link = models.URLField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    height = models.IntegerField(blank=True)
    width = models.IntegerField(blank=True)
    left = models.IntegerField(blank=True)
    slide = models.ForeignKey('Slide')

    def __str__(self):
        return 'Photo "%s" (ID: %s) for %s' % (self.description, self.pk, str(self.slide))

    class Meta:
        order_with_respect_to = 'slide'

class Order(models.Model):
    time_placed = models.TimeField()
    album = models.ForeignKey('Album')
    owner = models.ForeignKey(User)

    def __str__(self):
        return 'Order #%s for %s' % (self.pk, str(self.album))