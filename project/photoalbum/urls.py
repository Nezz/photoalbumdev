from django.conf.urls import patterns, include, url

urlpatterns = patterns('photoalbum.handlers',
    # User
    url(r'^$', 'user_handlers.indexHandler', name='index'),
    url(r'^login/$', 'user_handlers.loginHandler', name='login'),
    url(r'^register/$', 'user_handlers.registerHandler', name='register'),
    url(r'^logout/$', 'user_handlers.logoutHandler', name='logout'),
    url(r'^userexist/$', 'user_handlers.userExist', name='checkuser'),
    # Album
    url(r'^albums/$', 'album_handlers.albumlistHandler', name='albumlist'),
    url(r'^albums/(?P<album_id>([0-9a-zA-Z])+)/$', 'album_handlers.albumitemHandler', name='albumitem'),
    url(r'^albums/(?P<album_id>([0-9a-zA-Z])+)/delete$', 'album_handlers.albumdeleteHandler', name='albumitemdelete'),
    url(r'^albums/(?P<album_id>([0-9a-zA-Z])+)/modify', 'album_handlers.albummodifyHandler', name='albumitemmodify'),
    url(r'^albums/(?P<album_id>([0-9a-zA-Z])+)/(?P<slide_id>([0-9])+)/$', 'album_handlers.slideitemHandler', name='slideitem'),
    url(r'^albums/(?P<album_id>([0-9a-zA-Z])+)/(?P<slide_id>([0-9])+)/delete$', 'album_handlers.slidedeleteHandler', name='slideitemdelete'),
    url(r'^albums/(?P<album_id>([0-9a-zA-Z])+)/(?P<slide_id>([0-9])+)/modify$', 'album_handlers.slidemodifyHandler', name='slideitemmodify'),
    url(r'^albums/(?P<album_id>([0-9a-zA-Z])+)/(?P<slide_id>([0-9])+)/(?P<photo_id>([0-9])+)/$', 'album_handlers.slidephotoHandler', name='slideitemphoto'),
    url(r'^albums/(?P<album_id>([0-9a-zA-Z])+)/(?P<slide_id>([0-9])+)/(?P<photo_id>([0-9])+)/delete$', 'album_handlers.slidephotodeleteHandler', name='slideitemphotodelete'),
    url(r'^albums/(?P<album_id>([0-9a-zA-Z])+)/(?P<slide_id>([0-9])+)/(?P<photo_id>([0-9])+)/modify$', 'album_handlers.slidephotomodifyHandler', name='slideitemphotomodify'),
    # Order
    url(r'^albums/(?P<album_id>([0-9a-zA-Z])+)/order$', 'order_handlers.ordernewHandler', name='ordernew'),
    url(r'^orders/$', 'order_handlers.orderlistHandler', name='orderlist'),
    url(r'^orders/(?P<order_id>([0-9])+)/$', 'order_handlers.orderitemHandler', name='orderitem'),
    url(r'^orders/(?P<order_id>([0-9])+)/delete$', 'order_handlers.orderitemdeleteHandler', name='orderitemdelete'),
    url(r'^orders/paymentsuccess$', 'order_handlers.paymentsuccessHandler', name='paymentsuccess'),
    url(r'^orders/paymentcancel$', 'order_handlers.paymentcancelHandler', name='paymentcancel'),
    url(r'^orders/paymenterror$', 'order_handlers.paymenterrorHandler', name='paymenterror'),
    #Social authentication
    url(r'', include('social.apps.django_app.urls', namespace='social')),
)
