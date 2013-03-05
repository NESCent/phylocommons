from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    # Examples:
    url(r'^add/$', 'treeupload.views.add', name='add'),
    url(r'^uploads/$', 'treeupload.views.uploads', name='uploads'),
    url(r'^uploads/view/(?P<tree_id>[^/]*)/$', 'treeupload.views.upload_view', name='upload_view'),
)
