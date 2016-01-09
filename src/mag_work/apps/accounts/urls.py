# coding: utf-8
from django.conf.urls import patterns, url
from django.contrib.auth import views
from django.contrib.auth.decorators import login_required, user_passes_test

from accounts.views import RegistrationView, LoginView, LogOut, ProfileView, ProfileSettingsView, ProfileAccessView,\
    ProfileModelsListView


urlpatterns = patterns(
    u'accounts.views',

    url(r'^register/$', RegistrationView.as_view(), name=u'registration'),

    url(r'^login/$', LoginView.as_view(), name=u'login'),
    url(r'^logout/$', LogOut.as_view(), name=u'logout'),
    url(r'^profile/$', login_required(ProfileView.as_view()), name=u'profile'),
    url(r'^profile/settings/$', login_required(ProfileSettingsView.as_view()), name=u'profile_settings'),
    url(r'^profile/access/$', login_required(ProfileAccessView.as_view()), name=u'profile_access'),
    url(r'^profile/models_list/$', login_required(ProfileModelsListView.as_view()), name=u'profile_models_list'),

)