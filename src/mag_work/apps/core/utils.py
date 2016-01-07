# -*- coding:utf-8 -*-
import json
import random
from django.http.response import HttpResponse
from django.shortcuts import _get_queryset
import re
from django.contrib.admin import ModelAdmin
from django.core.urlresolvers import reverse
from functools import partial


class APIStatusMixin(object):
    class response_status(object):
        success = u'success'
        fail = u'fail'


class JSONResponseMixin(APIStatusMixin):
    """
    A mixin that can be used to render a JSON response.
    """

    def render_to_json_response(self, status, data=None, **response_kwargs):
        """
        Returns a JSON response, transforming 'context' to make the payload.
        """
        if not data:
            data = {}
        response = {
            u'status': status,
            u'data': data
        }
        return HttpResponse(
            self.convert_context_to_json(response),
            content_type='application/json',
            **response_kwargs
        )

    def convert_context_to_json(self, context):
        """Convert the context dictionary into a JSON object"""
        # Note: This is *EXTREMELY* naive; in reality, you'll need
        # to do much more complex handling to ensure that arbitrary
        # objects -- such as Django model instances or querysets
        # -- can be serialized as JSON.
        return json.dumps(context)


