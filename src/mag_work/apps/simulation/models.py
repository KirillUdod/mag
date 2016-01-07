# coding: utf-8
from django.conf import settings
from django.contrib.sites.models import Site
from django.db import models
from django.template.loader import render_to_string

from accounts.models import Account


def upload_photo(instance, filename):
    from core.utils import translify_upload_name

    filename = translify_upload_name(filename)
    return u'catalog/%s/%s' % (instance.product.id, filename)


class Sim_Model(models.Model):

    id = models.AutoField(primary_key=True, verbose_name=u'№ моделирования')
    account = models.ForeignKey(Account, related_name=u'account', verbose_name=u'Пользователь')
    type_id = models.ForeignKey(ModelType, related_name=u'type_id', verbose_name=u'Тип моделирования')
    created = models.DateTimeField(auto_now_add=True, verbose_name=u'Дата создания')
    result_img = models.ImageField(u'Фото (оригинал)', max_length=255, upload_to=upload_photo)

    class Meta:
        verbose_name = u'Заказ'
        verbose_name_plural = u'Заказы'
        ordering = (u'-id',)


class ModelType(models.Model):
    type_id = models.AutoField(primary_key=True, verbose_name=u'№ типа моделирования')
    name = models.TextField(max_length=50, verbose_name=u'Название модели')
    description = models.TextField(max_length=255, verbose_name=u'Описание модели')

    class Meta:
        verbose_name = u'Тип модели'
        verbose_name_plural = u'Типы моделей'
