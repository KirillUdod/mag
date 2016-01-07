from matplotlib import pylab
from pylab import *

import PIL
import PIL.Image
from io import StringIO
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.views.generic import FormView, View, TemplateView

from simulation.models import SimModel
from simulation.forms import GraphByPointsForm

# def graph(request):
#     x = [1,2,3,4,5,6]
#     y = [5,23,23,4,5]
#     plot(x,y, linewidth=2)
#
#     xlabel('x axis')
#     ylabel('y axis')
#     title('graph')
#     grid(True)
#
#     buffer = StringIO.StringIO()
#     canvas = pylab.get_current_fig_manager().canvas
#     canvas.draw()
#     graphIMG = PIL.Image.foromstring("RGB", canvas.gat.width_height(), canvas.tostring_rgd())
#     graphIMG.save(buffer, "PNG")
#     pylab.close()
#
#     return HttpResponse(buffer.getValue(), mimetype='image/png')


class GraphByPointsView(FormView):
    template_name = u'simulation/graph_by_points.html'
    form_class = GraphByPointsForm

    def form_valid(self, form):
        x = form.cleaned_data[u'axis_x']
        y = form.cleaned_data[u'axis_y']
        x = x.split(', ')
        y = x.split(', ')
        plot(x, y, linewidth=2)

        xlabel('x axis')
        ylabel('y axis')
        title('graph')
        grid(True)

        buffer = StringIO.StringIO()
        canvas = pylab.get_current_fig_manager().canvas
        canvas.draw()
        graphIMG = PIL.Image.foromstring("RGB", canvas.gat.width_height(), canvas.tostring_rgd())
        graphIMG.save(buffer, "PNG")

        SimModel.objects.create(account=request.user.id,
                                type_id=u'GraphByPoints',
                                result_img=buffer)
        Sim_Model.save()

    def get_context_data(self, **kwargs):
        context = super(GraphByPointsView, self).get_context_data(**kwargs)
        context[u'next'] = self.request.GET.get(u'next', u'')
        return context