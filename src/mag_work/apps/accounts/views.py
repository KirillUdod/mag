from django.conf import settings
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib.auth.tokens import default_token_generator
from django.core import signing
from django.core.mail import EmailMessage
from django.core.urlresolvers import reverse
from django.db import transaction
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import redirect, resolve_url, render_to_response
from django.template import RequestContext
from django.template.response import TemplateResponse
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth import login
from django.views.generic import FormView, View, TemplateView


from accounts.forms import RegistrationForm, LoginForm, ProfileAccessForm, ProfileSettingsForm
from accounts.models import Account
from simulation.models import SimModel, ModelType

User = get_user_model()

MESSAGES = {
    'need_auth': u'Пожалуйста, зарегистрируйтесь или авторизуйтесь!',
    'unknown_error': u'Возникла непредвиденая ошибка. Попробуйте повторить, либо обратитесь к службе поддержки.',
    'token_expired': u'Ссылка недействительна, пожалуйста обратитесь в службу поддержки.',
    'registration_success': u'Почтовый ящик успешно активирован!',
    'need_address': u'Для комфортной работы с магазином, пожалуйста добавьте адрес.',
    'email_notification': u'Поздравляем, Вы успешно зарегистрировались! Для подтверждения, пожалуйста перейдите по ссылке, отправленной на вашу почту.',
    'email_confirm': u'Пожалуйста, перейдите по ссылке, отправленной в письме для подтверждения.',
    'wrong_creds': u'Неправильный почтовый адрес/пароль. Попробуйте зайти еще раз. Если ошибка повторится – свяжитесь с нашей службой поддержки.',
    'password_reset': u'Пожалуйста, перейдите по ссылке, отправленной в письме для сброса пароля.',
    'notifications_updated': u'Настройки оповещений сохранены.',
    'settings_updated': u'Настройки сохранены.',
}


class RegistrationView(FormView):
    form_class = RegistrationForm
    template_name = u'accounts/registration.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            user = User.objects.get(id=request.user.id)
            if user.is_active:
                return HttpResponseRedirect(reverse(u'profile'))
            else:
                messages.error(request, MESSAGES['email_confirm'])
            return HttpResponseRedirect(self.get_redirect_url())
        return super(RegistrationView, self).dispatch(request, *args, **kwargs)

    def try_to_create_user(self, email, password, first_name, last_name):
        user = User.objects.create_user(username=email, email=email, first_name=first_name,
                                        last_name=last_name, password=password)
        user.is_active = True
        user.save()
        Account.objects.create_account(
            user=user,
            first_name=first_name,
            last_name=last_name,
        )
        if user:
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(self.request, user)
            return HttpResponseRedirect(reverse(u'profile'))
        else:
            messages.warning(self.request, MESSAGES['unknown_error'])
            return HttpResponseRedirect(self.get_redirect_url())

    def form_valid(self, form):
        email, password, first_name, last_name = (
            form.cleaned_data[u'email'],
            form.cleaned_data[u'password'],
            form.cleaned_data[u'first_name'],
            form.cleaned_data[u'last_name']
        )
        self.try_to_create_user(email, password, first_name, last_name)
        return HttpResponseRedirect(self.get_redirect_url())

    def form_invalid(self, form):
        data = u'%s' % [error for i, error in form.errors.items()][0]

        return HttpResponseRedirect(self.get_redirect_url())

    def get_redirect_url(self):
        if self.request.GET.get(u'next'):
            return self.request.GET.get(u'next')
        return reverse(u'core_index')



class LoginView(FormView):
    template_name = u'accounts/login.html'
    form_class = LoginForm

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return HttpResponseRedirect(reverse(u'profile'))
        return super(LoginView, self).get(request, *args, **kwargs)

    def form_valid(self, form):
        if not form.cleaned_data[u'remember_me']:
            self.request.session.set_expiry(0)
        user = authenticate(username=form.cleaned_data[u'email'],
                            password=form.cleaned_data[u'password'])
        if user:
            login(self.request, user)
            return HttpResponseRedirect(self.get_redirect_url())

        else:
            messages.error(self.request, MESSAGES['wrong_creds'], fail_silently=True)
            return HttpResponseRedirect(self.get_redirect_url())

    def get_context_data(self, **kwargs):
        context = super(LoginView, self).get_context_data(**kwargs)
        context[u'next'] = self.request.GET.get(u'next', u'')
        return context

    def get_redirect_url(self):
        if self.request.GET.get(u'next'):
            return self.request.GET.get(u'next')
        return reverse(u'core_index')



class LogOut(View):
    def get(self, request):
        return self.post(request)

    def post(self, request):
        logout(request)
        return redirect(request.GET.get(u'next') or reverse(u'core_index'))


class ProfileView(TemplateView):
    template_name = u'accounts/profile/profile.html'

    def dispatch(self, request, *args, **kwargs):
        if not hasattr(self.request.user, u'account'):
            return HttpResponseRedirect(self.get_redirect_url())
        return super(ProfileView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        context[u'account'] = self.request.user.account
        # orders = Order.objects.filter(
        #     Q(cart__checked_out=True) &
        #     Q(account=self.request.user.account) & (
        #         Q(payment_date__isnull=False) | Q(payment_type=Order.PAYMENT_TYPE_CASH)))
        # context[u'orders'] = orders
        return context

    def get_redirect_url(self):
        if self.request.GET.get(u'next'):
            return self.request.GET.get(u'next')
        return reverse(u'core_index')


class ProfileSettingsView(FormView):
    template_name = u'accounts/profile/profile_settings.html'
    form_class = ProfileSettingsForm

    def dispatch(self, request, *args, **kwargs):
        if not hasattr(self.request.user, u'account'):
            return self.get_redirect_url()
        return super(ProfileSettingsView, self).dispatch(request, *args, **kwargs)

    def get_initial(self):
        self.user = self.request.user
        self.account = self.user.account
        return {
            u'first_name': self.account.first_name,
            u'last_name': self.account.last_name,
        }

    def get_form_kwargs(self):
        kwargs = super(ProfileSettingsView, self).get_form_kwargs()
        kwargs.update({u'user': self.user})
        return kwargs

    def form_valid(self, form):
        first_name, last_name = (
            form.cleaned_data.get(u'first_name'),
            form.cleaned_data.get(u'last_name')
        )
        self.account.first_name = first_name
        self.account.last_name = last_name
        self.account.save()
        messages.success(self.request, MESSAGES['settings_updated'])
        return redirect(reverse(u'profile_settings'))

    def get_redirect_url(self):
        if self.request.GET.get(u'next'):
            return self.request.GET.get(u'next')
        return reverse(u'core_index')


class ProfileAccessView(FormView):
    template_name = u'accounts/profile/profile_access.html'
    form_class = ProfileAccessForm

    def dispatch(self, request, *args, **kwargs):
        if not hasattr(self.request.user, u'account'):
            return get_redirect_url()
        return super(ProfileAccessView, self).dispatch(request, *args, **kwargs)

    def get_initial(self):
        self.user = self.request.user
        self.account = self.user.account
        return {
            u'email': self.account.get_email(),
        }

    def get_form_kwargs(self):
        kwargs = super(ProfileAccessView, self).get_form_kwargs()
        kwargs.update({u'user': self.user})
        return kwargs

    def form_valid(self, form):
        email, password = (
            form.cleaned_data.get(u'new_email2'),
            form.cleaned_data.get(u'new_password2'),
        )
        if email:
            self.user.is_active = False
            self.user.email = email
            self.user.username = email
            self.user.save()
        if password:
            self.user.set_password(password)
            self.user.save()
        self.account.save()
        if email:
            logout(self.request)
            messages.success(self.request, MESSAGES['email_confirm'])
            return get_redirect_url()
        else:
            messages.success(self.request, MESSAGES['settings_updated'])
        return redirect(reverse(u'profile_access'))

    def get_redirect_url(self):
        if self.request.GET.get(u'next'):
            return self.request.GET.get(u'next')
        return reverse(u'core_index')


class ProfileModelsListView(TemplateView):
    template_name = u'accounts/profile/profile_models_list.html'

    def dispatch(self, request, *args, **kwargs):
        if not hasattr(self.request.user, u'account'):
            return HttpResponseRedirect(reverse(u'core_index'))
        return super(ProfileModelsListView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ProfileModelsListView, self).get_context_data(**kwargs)
        models = SimModel.objects.filter(Q(account=self.request.user.account))
        for model in models:
            # id = model.type_id.
            # t = ModelType.objects.get(mod_id=id)
            model.name = model.type_id.name
        context[u'models'] = models
        return context


