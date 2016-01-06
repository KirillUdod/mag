from django.db import models
from django.core.mail import EmailMessage


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
        body = render_to_string(
            template_name,
            {
                u'email': self.get_email(),
                u'token': signing.dumps(self.get_email(), salt=settings.SIGNUP_SALT),
                u'site': Site.objects.get_current()
            }
        )
        title = u'Регистрация на '
        message = EmailMessage(
            title,
            body,
            settings.EMAIL_SENDER,
            [self.get_email().encode(u'utf-8'), ])
        message.content_subtype = u'html'
        message.send()

    def notify_on_express_registration_via_email(self, password,
                                                 template_name=u'accounts/email/registration_on_express_order.html'):
        body = render_to_string(
            template_name,
            {
                u'email': self.get_email(),
                u'password': password,
                u'site': Site.objects.get_current()
            }
        )
        title = u'Регистрация на MadyArt.ru'
        message = EmailMessage(
            title,
            body,
            settings.EMAIL_SENDER,
            [self.get_email().encode(u'utf-8'), ])
        message.content_subtype = u'html'
        message.send()

    def notify_on_express_registration_via_sms(self, password,
                                               template_name=u'accounts/sms/registration_on_express_order.html'):
        content = render_to_string(
            template_name,
            {
                u'password': password
            }
        )
        sms_message = SMSMessage.objects.create(
            content=content,
            recipient=self.phone,
            queue_type=SMSMessage.QUEUE_TYPE_REGULAR
        )
        send_message(sms_message)

    def notify_on_email_change_request(self, template_name=u'accounts/email/change_email_request.html'):
        body = render_to_string(
            template_name,
            {
                u'email': self.get_email(),
                u'token': signing.dumps(self.get_email(), salt=settings.SIGNUP_SALT),
                u'site': Site.objects.get_current()
            }
        )
        title = u'Изменение почтового адреса на MadyArt.ru'
        message = EmailMessage(
            title,
            body,
            settings.EMAIL_SENDER,
            [self.get_email().encode(u'utf-8'), ])
        message.content_subtype = u'html'
        message.send()

    def save(self, *args, **kwargs):
        if self.phone:
            self.phone = clean_phone(self.phone)
        super(Account, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.get_full_name()