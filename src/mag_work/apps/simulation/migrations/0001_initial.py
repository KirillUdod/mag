# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ModelType',
            fields=[
                ('mod_id', models.AutoField(verbose_name='№ типа моделирования', primary_key=True, serialize=False)),
                ('name', models.TextField(verbose_name='Название модели', max_length=50)),
                ('description', models.TextField(verbose_name='Описание модели', max_length=255)),
            ],
            options={
                'verbose_name': 'Тип модели',
                'verbose_name_plural': 'Типы моделей',
            },
        ),
        migrations.CreateModel(
            name='SimModel',
            fields=[
                ('id', models.AutoField(verbose_name='№ моделирования', primary_key=True, serialize=False)),
                ('created', models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)),
                ('result_img', models.ImageField(verbose_name='Фото (оригинал)', max_length=255, upload_to='uploads/')),
                ('account', models.ForeignKey(to='accounts.Account', verbose_name='Пользователь', related_name='account')),
                ('type_id', models.ForeignKey(to='simulation.ModelType', verbose_name='Тип моделирования', related_name='modid')),
            ],
            options={
                'verbose_name': 'Модель',
                'verbose_name_plural': 'Модели',
                'ordering': ('-id',),
            },
        ),
    ]
