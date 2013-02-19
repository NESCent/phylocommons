from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'treequery.views.query', name='query'),
)
