# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='IndexBlock',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('title', models.CharField(verbose_name='Название', max_length=255)),
                ('text', models.TextField(verbose_name='Текст', blank=True, max_length=255)),
            ],
            options={
                'verbose_name': 'Блок главной страницы',
                'verbose_name_plural': 'Блоки главной страницы',
                'ordering': ('id',),
            },
        ),
    ]
