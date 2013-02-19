from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^query/$', 'treequery.views.query', name='query'),
)
