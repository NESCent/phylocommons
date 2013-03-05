from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    # Examples:
    url(r'^add/$', 'treeupload.views.add', name='add'),
    url(r'^uploads/$', 'treeupload.views.uploads', name='uploads'),
    url(r'^uploads/view/(?P<tree_id>[^/]*)/$', 'treeupload.views.upload_view', name='upload_view'),
    url(r'^uploads/test/(?P<tree_id>[^/]*)/$', 'treeupload.views.upload_test', name='upload_test'),
    url(r'^uploads/approve/(?P<tree_id>[^/]*)/$', 'treeupload.views.upload_approve', name='upload_approve'),
    url(r'^uploads/reject/(?P<tree_id>[^/]*)/$', 'treeupload.views.upload_reject', name='upload_reject'),
    url(r'^uploads/(?P<tree_id>[^/]*)/$', 'treeupload.views.upload_action', name='upload_action'),
)
