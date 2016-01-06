from django.views.generic import TemplateView

from core.models import IndexBlock


class IndexPage(TemplateView):
    template_name = u'index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexPage, self).get_context_data(**kwargs)
        context[u'blocks'] = IndexBlock.objects.get
        return context
