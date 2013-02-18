from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^query/(?P<query>\w*)$', 'treequery.views.query', name='query'),
)
