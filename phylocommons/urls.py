from django.conf.urls import patterns, include, url
from phylocommons.forms import ProfileForm

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'phylocommons.views.home', name='home'),
    
    url(r'^contributors/$', 'phylocommons.views.contributors', name='contributors'),
    url(r'^contact/$', 'phylocommons.views.contact', name='contact'),
    url(r'^help/$', 'phylocommons.views.help', name='help'),
    
    # accounts
    url(r'^accounts/', include('registration.urls')),
    
    # profiles
    url(r'^user/edit', 'profiles.views.edit_profile', 
        {
         'form_class': ProfileForm,
         }),
    url(r'^user/', include('profiles.urls')),
    
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
