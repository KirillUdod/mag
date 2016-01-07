from django.db import models
from django.conf import settings
from django.core.mail import send_mail


class AccountManager(models.Manager):
    def create_account(self, user, first_name, last_name):
        account = self.model(user=user, first_name=first_name, last_name=last_name)
        account.save(using=self._db)
        return account


class Account(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, verbose_name=u'Пользователь', related_name=u'account')

    first_name = models.CharField(u'Имя', max_length=255)
    last_name = models.CharField(u'Фамилия', max_length=255)
    ext_id = models.CharField(u'Внешний ID', max_length=255, null=True, blank=True)

    objects = AccountManager()

    class Meta:
        verbose_name = u'Аккаунт'
        verbose_name_plural = u'Аккаунты'

    def get_full_name(self):
        full_name = u'%s %s' % (self.last_name, self.first_name)
        return full_name.strip()

    def get_email(self):
        return self.user.email

    def notify_on_registration(self, template_name=u'accounts/email/thanks_for_registration.html'):
        # body = render_to_string(
        #     template_name,
        #     {
        #         u'email': self.get_email(),
        #         u'token': signing.dumps(self.get_email(), salt=settings.SIGNUP_SALT),
        #         u'site': Site.objects.get_current()
        #     }
        # )
        # title = u'Регистрация на сайте'
        # message = EmailMessage(
        #     title,
        #     body,
        #     settings.EMAIL_SENDER,
        #     [self.get_email().encode(u'utf-8'), ])
        # message.content_subtype = u'html'
        # message.send()
        return

    def save(self, *args, **kwargs):
        super(Account, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.get_full_name()