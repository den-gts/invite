from django.conf.urls import patterns, include, url
from appInvite.views import writeInvite, sendInvite, activateInvite, newPswd, showDebugInfo
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', writeInvite, name='home'),
    url(r'^sendInvite', sendInvite),
    url(r'^activate/(.{40})$', activateInvite),
    url(r'^newpswd$', newPswd),
    url(r'^debug$', showDebugInfo),
    # url(r'^invite/', include('invite.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
