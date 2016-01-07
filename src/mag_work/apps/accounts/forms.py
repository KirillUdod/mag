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

from accounts.models import Account

User = get_user_model()


class RegistrationForm(forms.Form):
    first_name = forms.CharField(label=u'Имя', required=True, widget=forms.TextInput(attrs={
        u'type': u'text',
        u'class': u'auth-form-input auth-form-input_text auth-form-input_full',
        u'required': u'',
        u'data-msg-required': u'Обязательное поле',
        u'data-rule-lettersonlyRU': u'true',
        u'data-msg-lettersonlyRU': u'Пожалуйста, вводите буквы',
    }))

    last_name = forms.CharField(label=u'Фамилия', required=True, widget=forms.TextInput(attrs={
        u'type': u'text',
        u'class': u'auth-form-input auth-form-input_text auth-form-input_full',
        u'required': u'',
        u'data-msg-required': u'Обязательное поле',

    }))

    email = forms.EmailField(label=u'Электронная почта', required=True, widget=forms.EmailInput(attrs={
        u'type': u'email',
        u'class': u'auth-form-input auth-form-input_text auth-form-input_full',
        u'required': u'',
        u'data-msg-required': u'Обязательное поле',
        u'data-msg-email': u'Пожалуйста, введите корректный электронный адрес',
    }))

    password = forms.CharField(label=u'Пароль', required=True, widget=forms.PasswordInput(attrs={
        u'type': u'password',
        u'class': u'auth-form-input auth-form-input_text auth-form-input_full',
        u'required': u'',
        u'data-msg-required': u'Обязательное поле',
        u'data-rule-minlength': u'6',
        u'data-msg-minlength': u'Не менее 6 символов',
    }))

    def clean_email(self):
        if User.objects.filter(email__iexact=self.cleaned_data[u'email']).exists():
            raise forms.ValidationError(u'Данный почтовый ящик уже используется')
        return self.cleaned_data[u'email']

    def clean_password(self):
        password = self.cleaned_data.get(u'password', u'')
        if not len(password) >= 6:
            raise forms.ValidationError(u'Пароль должен быть не менее 6 символов')
        if password.isspace() or len(password.strip()) != len(password):
            raise forms.ValidationError(u'Пароль не может состоять из пробелов')
        return password


class LoginForm(forms.Form):
    email = forms.EmailField(label=u'Электронная почта', widget=forms.TextInput(attrs={
        u'type': u'email',
        u'class': u'auth-form-input auth-form-input_text auth-form-input_full',
        u'required': u'',
        u'data-msg-required': u'Обязательное поле',
        u'data-msg-email': u'Пожалуйста, введите корректный электронный адрес',
    }))
    password = forms.CharField(label=u'Пароль', widget=forms.PasswordInput(attrs={
        u'type': u'password',
        u'class': u'auth-form-input auth-form-input_text auth-form-input_full',
        u'required': u'',
        u'data-msg-required': u'Обязательное поле',
    }))
    remember_me = forms.BooleanField(label=u'Запомнить меня', required=False, widget=forms.CheckboxInput)


class ProfileSettingsForm(forms.ModelForm):
    first_name = forms.CharField(label=u'Имя', required=True, widget=forms.TextInput(attrs={
        u'type': u'text',
        u'class': u'profile-data-textbox',
        u'required': u'',
        u'data-msg-required': u'Обязательное поле',
        u'data-rule-lettersonlyRU': u'true',
        u'data-msg-lettersonlyRU': u'Пожалуйста, вводите буквы',
    }))

    last_name = forms.CharField(label=u'Фамилия', required=True, widget=forms.TextInput(attrs={
        u'type': u'text',
        u'class': u'profile-data-textbox',
        u'required': u'',
        u'data-msg-required': u'Обязательное поле',
        u'data-rule-lettersonlyRU': u'true',
        u'data-msg-lettersonlyRU': u'Пожалуйста, вводите буквы',
    }))

    class Meta:
        model = Account
        fields = (u'first_name', u'last_name')

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(ProfileSettingsForm, self).__init__(*args, **kwargs)


class ProfileAccessForm(forms.ModelForm):
    email = forms.EmailField(label=u'Текущий адрес электронной почты', required=False, widget=forms.TextInput(attrs={
        u'type': u'email',
        u'class': u'profile-data-textbox',
        u'data-msg-email': u'Пожалуйста, введите корректный электронный адрес',
    }))

    new_email1 = forms.EmailField(label=u'Новый адрес электронной почты', required=False, widget=forms.TextInput(attrs={
        u'type': u'email',
        u'class': u'profile-data-textbox',
        u'data-msg-email': u'Пожалуйста, введите корректный электронный адрес',
    }))

    new_email2 = forms.EmailField(label=u'Повторите новый адрес', required=False, widget=forms.TextInput(attrs={
        u'type': u'email',
        u'class': u'profile-data-textbox',
        u'data-msg-email': u'Пожалуйста, введите корректный электронный адрес',
    }))

    old_password = forms.CharField(label=u'Текущий пароль', required=False, widget=forms.PasswordInput(attrs={
        u'type': u'password',
        u'class': u'profile-data-textbox',
    }))

    new_password1 = forms.CharField(label=u'Новый пароль', required=False, widget=forms.PasswordInput(attrs={
        u'type': u'password',
        u'class': u'profile-data-textbox',
    }))

    new_password2 = forms.CharField(label=u'Повторите новый пароль', required=False, widget=forms.PasswordInput(attrs={
        u'type': u'password',
        u'class': u'profile-data-textbox',
    }))

    class Meta:
        model = Account
        fields = (u'email', u'new_email1', u'new_email2', u'old_password', u'new_password1', u'new_password2' )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(ProfileAccessForm, self).__init__(*args, **kwargs)

    def clean_new_email2(self):
        email1 = self.cleaned_data[u'new_email1']
        email2 = self.cleaned_data[u'new_email2']
        if email1 != email2:
            raise forms.ValidationError(u'Введенные адреса электронной почты не совпадают')
        if User.objects.filter(email__iexact=email2).exists():
            raise forms.ValidationError(u'Данный почтовый ящик уже используется')
        return email2

    def clean_old_password(self):
        """
        Validates that the old_password field is correct.
        """
        old_password = self.cleaned_data.get(u'old_password', None)
        # FIXME подумай еще раз
        if old_password:
            if not self.user.check_password(old_password):
                raise forms.ValidationError(u'Введен неправильный пароль')
        return old_password

    def clean_new_password2(self):
        new_password1 = self.cleaned_data.get(u'new_password1', u'')
        new_password2 = self.cleaned_data.get(u'new_password2', u'')
        old_password = self.cleaned_data.get(u'old_password', u'')
        if old_password:
            if not self.user.check_password(old_password):
                raise forms.ValidationError(u'Введен неправильный пароль')
        else:
            if new_password1 or new_password2:
                raise forms.ValidationError(u'Для сохранения нового пароля, необходимо ввести старый пароль')
        if new_password1 and new_password2:
            if new_password1 != new_password2:
                raise forms.ValidationError(u'Введенные пароли не совпадают')
            if not len(new_password2) >= 6:
                raise forms.ValidationError(u'Пароль должен быть не менее 6 символов')
            if new_password2.isspace() or len(new_password2.strip()) != len(new_password2):
                raise forms.ValidationError(u'Пароль не может состоять из пробелов')

        return new_password2