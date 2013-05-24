from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'treeview.views.list', name='trees'),
    url(r'^(?P<tree_id>[^/]*)/download$', 'treeview.views.download', name='download'),
    url(r'^(?P<tree_id>[^/]*)/$', 'treeview.views.view', name='view'),
)
