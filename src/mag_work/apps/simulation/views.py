from matplotlib import pylab
from pylab import *

import PIL
import PIL.Image
import io
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.views.generic import FormView, View, TemplateView

from simulation.models import SimModel, ModelType
from simulation.forms import GraphByPointsForm, ModelTypeForm


class GraphByPointsView(FormView):
    template_name = u'simulation/graph_by_points.html'
    form_class = GraphByPointsForm

    def form_valid(self, form):
        x = form.cleaned_data[u'axis_x']
        y = form.cleaned_data[u'axis_y']

        x = x.split(', ')
        y = y.split(', ')
        plot(x, y, linewidth=2)

        xlabel('x axis')
        ylabel('y axis')
        title('graph')
        grid(True)

        buffer = str(io.StringIO())
        canvas = pylab.get_current_fig_manager().canvas
        canvas.draw()
        graphIMG = PIL.Image.fromstring("RGB", canvas.get_width_height(), canvas.tostring_rgb())
        graphIMG.save(buffer, "PNG")
        # return HttpResponse(buffer,  content_type="image/png")
        # SimModel.objects.create(account=request.user.id,
        #                         type_id=u'GraphByPoints',
        #                         result_img=buffer)
        # Sim_Model.save()


class ModelTypeView(FormView):
    template_name = u'simulation/chose_mod_type.html'
    form_class = ModelTypeForm

    def get_initial(self):
        print(ModelType.objects.all())
        return {u'models': ModelType.objects.all()}

    def form_valid(self, form):
        answer = form.cleaned_data[u'value']
        return redirect(reverse(u'profile_access'))

    def get_redirect_url(self):
        if self.request.GET.get(u'next'):
            return self.request.GET.get(u'next')
        return reverse(u'core_index')