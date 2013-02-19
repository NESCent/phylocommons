from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'trees.views.list', name='list'),
    url(r'^add/$', 'trees.views.add', name='add'),
    url(r'^(?P<tree_uri>\w*)/download$', 'trees.views.download', name='download'),
    url(r'^(?P<tree_uri>\w*)/$', 'trees.views.view', name='view'),
)
