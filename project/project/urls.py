from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'project.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'photoalbum.views.index_view'),
    url(r'^login/$', 'photoalbum.views.login_view'),
    url(r'^albums/(?P<album_id>([0-9a-zA-Z])*)/$', 'photoalbum.views.album_view'),
    url(r'^albums/$', 'photoalbum.views.album_list_view'),
    url(r'^register/$', 'photoalbum.views.register_view'),
    url(r'^logout/$', 'photoalbum.views.logout_view'),
)
