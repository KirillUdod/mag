# coding: utf-8
from django.conf.urls import patterns, url

from simulation.views import GraphByPointsView


urlpatterns = patterns(
    u'accounts.views',

    url(r'^simmod/$', GraphByPointsView.as_view(), name=u'sim'),

    # url(r'^login/$', LoginView.as_view(), name=u'login'),
    # url(r'^logout/$', LogOut.as_view(), name=u'logout'),
    # url(r'^profile/$', login_required(ProfileView.as_view()), name=u'profile'),
    # url(r'^profile/settings/$', login_required(ProfileSettingsView.as_view()), name=u'profile_settings'),
    # url(r'^profile/access/$', login_required(ProfileAccessView.as_view()), name=u'profile_access'),

)