from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'project.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'photoalbum.views.index'),
    url(r'^login/$', 'photoalbum.views.login_view'),
    url(r'^register/$', 'photoalbum.views.register'),
    url(r'^regview/$', 'photoalbum.views.register_view'),
    url(r'^logout/$', 'photoalbum.views.logout_view'),
)
