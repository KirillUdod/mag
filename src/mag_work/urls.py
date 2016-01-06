from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    # Examples:
    # url(r'^$', 'mag_work.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^', include(u'core.urls')),
    url(r'^admin/', include(admin.site.urls)),
]
