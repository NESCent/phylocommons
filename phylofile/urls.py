from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'phylofile.views.home', name='home'),
    
    url(r'^contributors/$', 'phylofile.views.contributors', name='contributors'),
    url(r'^contact/$', 'phylofile.views.contact', name='contact'),
    url(r'^profile/(?P<user_id>[^/]*)/$', 'phylofile.views.user_profile', name='user_profile'),
    
    # accounts
    url(r'^accounts/', include('registration.urls')),
    
    # profiles
    url(r'^profiles/', include('profiles.urls')),
    
    # treeupload application
    url(r'^trees/', include('treeupload.urls')),
    
    # treeview application
    url(r'^trees/', include('treeview.urls')),

    # treequery application
    url(r'^query/', include('treequery.urls')),
    
    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
