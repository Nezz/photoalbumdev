from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'project.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    # User
    url(r'^$', 'photoalbum.handlers.user_handlers.indexHandler', name='index'),
    url(r'^login/$', 'photoalbum.handlers.user_handlers.loginHandler', name='login'),
    url(r'^register/$', 'photoalbum.handlers.user_handlers.registerHandler', name='register'),
    url(r'^logout/$', 'photoalbum.handlers.user_handlers.logoutHandler', name='logout'),
    # Album
    url(r'^albums/$', 'photoalbum.handlers.album_handlers.albumlistHandler', name='albumlist'),
    url(r'^albums/(?P<album_id>([0-9a-zA-Z])+)/$', 'photoalbum.handlers.album_handlers.albumitemHandler', name='albumitem'),
    url(r'^albums/(?P<album_id>([0-9a-zA-Z])+)/delete$', 'photoalbum.handlers.album_handlers.albumdeleteHandler', name='albumitemdelete'),
    url(r'^albums/(?P<album_id>([0-9a-zA-Z])+)/modify', 'photoalbum.handlers.album_handlers.albummodifyHandler', name='albumitemmodify'),
    url(r'^albums/(?P<album_id>([0-9a-zA-Z])+)/(?P<slide_id>([0-9])+)/$', 'photoalbum.handlers.album_handlers.slideitemHandler', name='slideitem'),
    url(r'^albums/(?P<album_id>([0-9a-zA-Z])+)/(?P<slide_id>([0-9])+)/delete$', 'photoalbum.handlers.album_handlers.slidedeleteHandler', name='slideitemdelete'),
    url(r'^albums/(?P<album_id>([0-9a-zA-Z])+)/(?P<slide_id>([0-9])+)/modify$', 'photoalbum.handlers.album_handlers.slidemodifyHandler', name='slideitemmodify'),
    url(r'^albums/(?P<album_id>([0-9a-zA-Z])+)/(?P<slide_id>([0-9])+)/(?P<photo_id>([0-9])+)$', 'photoalbum.handlers.album_handlers.slidephotoHandler', name='slideitemphoto'),
    url(r'^albums/(?P<album_id>([0-9a-zA-Z])+)/(?P<slide_id>([0-9])+)/(?P<photo_id>([0-9])+)/modify$', 'photoalbum.handlers.album_handlers.slidephotomodifyHandler', name='slideitemphotomodify'),
    # Order
    url(r'^albums/(?P<album_id>([0-9a-zA-Z])+)/order$', 'photoalbum.handlers.order_handlers.neworderHandler', name='neworder'),
    url(r'^orders/$', 'photoalbum.handlers.order_handlers.orderlistHandler', name='orderlist'),
    url(r'^orders/(?P<order_id>([0-9])+)/$', 'photoalbum.handlers.order_handlers.orderitemHandler', name='orderitem'),
    url(r'^orders/(?P<order_id>([0-9])+)/delete$', 'photoalbum.handlers.order_handlers.orderitemdeleteHandler', name='orderitemdelete'),
)
