from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'treeview.views.tree_list', name='tree_list'),
    url(r'^(?P<tree_id>[^/]*)/download$', 'treeview.views.download', name='download'),
    url(r'^(?P<tree_id>[^/]*)/view$', 'treeview.views.svgview', name='svgview'),
    url(r'^(?P<tree_id>[^/]*)/$', 'treeview.views.view', name='view'),
)
