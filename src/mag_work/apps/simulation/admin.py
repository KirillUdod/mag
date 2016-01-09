# coding: utf-8
from django.contrib import admin
from django.core.urlresolvers import reverse
from django.http import HttpResponse

from simulation.models import SimModel, ModelType


class SimModelAdmin(admin.ModelAdmin):
    list_display = (u'id', u'account', u'type_id', u'created', u'result_img',)

admin.site.register(SimModel, SimModelAdmin)

class ModelTypeAdmin(admin.ModelAdmin):
    list_display = (u'mod_id', u'name', u'description',)

admin.site.register(ModelType, ModelTypeAdmin)