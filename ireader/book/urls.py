from django.conf.urls import patterns, url

urlpatterns = patterns('book.views',
	(r'^0(?P<pk>\d?)/$', 'show_category', {'tmpl': 'book/category.html'}, 'show-category'),
	(r'^content/(?P<pk>\d+)/$', 'show_content', {'tmpl': 'book/content.html'}, 'show-content'),
	(r'^detail/(?P<partition>\d+)/(?P<pk>\d+)/$', 'show_detail', {'tmpl': 'book/detail.html'}, 'show-detail'),
)
