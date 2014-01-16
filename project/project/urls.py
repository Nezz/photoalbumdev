from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'project.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    # User
    url(r'^$', 'photoalbum.handlers.user_handlers.indexHandler'),
    url(r'^login/$', 'photoalbum.handlers.user_handlers.loginHandler'),
    url(r'^register/$', 'photoalbum.handlers.user_handlers.registerHandler'),
    url(r'^logout/$', 'photoalbum.handlers.user_handlers.logoutHandler'),
    url(r'^albums/$', 'photoalbum.handlers.user_handlers.indexHandler'),
    # Album
    url(r'^albums/(?P<album_id>([0-9a-zA-Z])+)/$', 'photoalbum.handlers.album_handlers.albumitemHandler'),
    url(r'^albums/(?P<album_id>([0-9a-zA-Z])+)/(?P<slide_id>([0-9])+)/$', 'photoalbum.handlers.album_handlers.slideitemHandler'),
    url(r'^albums/(?P<album_id>([0-9a-zA-Z])+)/(?P<slide_id>([0-9])+)/modify$', 'photoalbum.handlers.album_handlers.slidemodifyHandler'),
    url(r'^albums/(?P<album_id>([0-9a-zA-Z])+)/(?P<slide_id>([0-9])+)/(?P<photo_id>([0-9])+)$', 'photoalbum.handlers.album_handlers.slidephotoHandler'),
    url(r'^albums/(?P<album_id>([0-9a-zA-Z])+)/(?P<slide_id>([0-9])+)/(?P<photo_id>([0-9])+)$', 'photoalbum.handlers.album_handlers.slidephotomodifyHandler'),
    # Order
    url(r'^albums/(?P<album_id>([0-9a-zA-Z])+)/order$', 'photoalbum.handlers.order_handlers.neworderHandler'),
    url(r'^orders/$', 'photoalbum.handlers.order_handlers.orderlistHandler'),
    url(r'^orders/(?P<order_id>([0-9])+)/$', 'photoalbum.handlers.order_handlers.orderitemHandler'),
)
