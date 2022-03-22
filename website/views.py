from django.shortcuts import render, get_object_or_404
from django.http import Http404, HttpResponse
from django.template import loader

from .models import Datapoint

from django.views.decorators.cache import never_cache



# Create your views here.
@never_cache
def index(request):
    return render(request, 'website/index.html', {})
    
@never_cache
def data(request):
    datapoints = Datapoint.objects.order_by('created_at')
    context = {
        'datapoints': datapoints
    }
    #template = loader.get_template('website/data.html')
    #return HttpResponse(template.render(context, request))
    return render(request, 'website/data.html', context)

@never_cache
def sample(request, datapoint_id):
    # try:
    #     sample = Datapoint.objects.get(pk=datapoint_id)
    # except Datapoint.DoesNotExist:
    #     raise Http404(f"id {datapoint_id} does not exist!")
    sample = get_object_or_404(Datapoint, pk=datapoint_id)
    context = {
        'sample': sample
    }
    return render(request, 'website/sample.html', context)

@never_cache
def page1(request):
    return render(request, 'website/page1.html', {})
@never_cache
def page2(request):
    return render(request, 'website/page2.html', {})

@never_cache
def map(request):
    return render(request, 'website/map.html', {'marker_coord': [47.375, 8.545]})
