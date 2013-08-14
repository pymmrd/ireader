from django.conf.urls import patterns, include, url
from django.conf import settings

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ireader.views.home', name='home'),
    # url(r'^ireader/', include('ireader.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
	url(r'^book/', include('book.urls')),
	(r'^$', 'book.views.index', {'tmpl': 'index.html'}, 'index'),
)

if settings.DEBUG:
	urlpatterns += patterns('django.contrib.staticfiles.views',
	    url(r'^static/(?P<path>.*)$', 'serve'),
	)

	
