# -*- coding:utf-8 -*-
from datetime import datetime
from django.conf import settings

from accounts.forms import LoginForm, RegistrationForm


def auth_forms(request):
    """
    Всплывающие окна регистрации, авторизации и восстановления пароля + подписки
    """
    return {
        u'login_form': LoginForm(),
        u'registration_form': RegistrationForm(),
    }
