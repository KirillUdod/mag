# coding: utf-8
from django.conf.urls import include, url, patterns
from django.contrib import admin



urlpatterns = patterns(
    u'',
    url(r'^admin/', include(admin.site.urls))
)

urlpatterns += patterns(
    u'',
    url(r'^', include(u'core.urls')),
    url(r'^', include(u'accounts.urls')),
    url(r'^', include(u'simulation.urls')),
)
