# coding: utf-8
import datetime
from django import forms
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordResetForm as DjangoPasswordResetForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.models import get_current_site
from django.core.mail import EmailMessage
from django.template import loader
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.forms import AuthenticationForm
from django.forms import ModelChoiceField

from simulation.models import ModelType


class UserModelChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
         return obj.get_name()


class ModelTypeForm(forms.Form):
    type = UserModelChoiceField(queryset=ModelType.objects.all().order_by('name'), required = False)


class GraphByPointsForm(forms.Form):
    axis_x = forms.CharField(label=u'Точки по оси Х', required=True, widget=forms.TextInput(attrs={
        u'type': u'axis_x',
        u'class': u'profile-data-textbox',
        u'required': u'',
        u'data-msg-required': u'Обязательное поле'
    }))
    axis_y = forms.CharField(label=u'Точки по оси Х', required=True, widget=forms.TextInput(attrs={
        u'type': u'axis_y',
        u'class': u'profile-data-textbox',
        u'required': u'',
        u'data-msg-required': u'Обязательное поле'
    }))