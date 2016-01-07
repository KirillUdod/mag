from matplotlib import pylab
from pylab import *

import PIL
import PIL.Image
import StringIO
from django.http import HttpResponse
from django.template import RequestContext, loader

def graph(request):
    x = [1,2,3,4,5,6]
    y = [5,23,23,4,5]
    plot(x,y, linewidth=2)

    xlabel('x axis')
    ylabel('y axis')
    title('graph')
    grid(True)

    buffer = StringIO.StringIO()
    canvas = pylab.get_current_fig_manager().canvas
    canvas.draw()
    graphIMG = PIL.Image.foromstring("RGB", canvas.gat.width_height(), canvas.tostring_rgd())
    graphIMG.sava(buffer, "PNG")
    pylab.close()

    return HttpResponse(buffer.getValue(), mimetype='image/png')