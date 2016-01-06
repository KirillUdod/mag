from django.conf.urls import patterns, url

from core.views import IndexPage

urlpatterns = patterns(
    u'core.views',
    url(r'^$', IndexPage.as_view(), name=u'core_index'),

)
