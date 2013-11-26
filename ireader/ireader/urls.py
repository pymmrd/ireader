from django.conf.urls import patterns, include, url
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ireader.views.home', name='home'),
    # url(r'^ireader/', include('ireader.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^book/', include('book.urls')),
    url(r'^$', 'book.views.index',
        {'tmpl': 'index.html'}, 'index'),
    url(r'^(?P<page>\d+)/$', 'book.views.index',
        {'tmpl':'index.html'}, 'index'),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
)

if settings.DEBUG:
    urlpatterns += patterns('django.contrib.staticfiles.views',
        url(r'^static/(?P<path>.*)$', 'serve'),
    )

handler404 = 'book.views.page_not_found'
handler500 = 'book.views.server_error'


