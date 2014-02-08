from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('photoalbum.urls')),
)

handler404 = 'photoalbum.views.custom_404_view'
handler500 = 'photoalbum.views.custom_error_view'
