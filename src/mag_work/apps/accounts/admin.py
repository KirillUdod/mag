# coding: utf-8
from django.contrib import admin
from django.core.urlresolvers import reverse
from django.http import HttpResponse

from accounts.models import Account


def export_as_text(self, request, queryset):
    result = u''
    for account in queryset:
        result += u'{id};{full_name};{phone};{email}\r\n'.format(
            id=account.id,
            full_name=account.get_full_name(),
            phone=account.phone,
            email=account.get_email()
        )
    response = HttpResponse(result, content_type='application/octet-stream')
    response['Content-Disposition'] = 'attachment; filename="users.txt"'
    return response


export_as_text.short_description = "Экспортировать в файл"


class AccountAdmin(admin.ModelAdmin):
    list_display = (u'id', u'get_full_name', u'get_email', u'is_active')
    list_display_links = (u'id', u'get_full_name', u'get_email')
    ordering = (u'id',)

    def is_active(self, instance):
        return instance.user.is_active


admin.site.register(Account, AccountAdmin)



