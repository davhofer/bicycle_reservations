from django.shortcuts import render, get_object_or_404
from django.http import Http404, HttpResponse, JsonResponse
from django.template import loader


from .models import Datapoint
from .forms import InputForm

from django.views.decorators.cache import never_cache



# Create your views here.
@never_cache
def index(request):
    if request.method == 'GET':
        return render(request, 'website/index.html', {'get_results': False, 'autofocus': False})
    elif request.method == 'POST':
        form = InputForm(request.POST)
        
        start = form.data['start']
        end = form.data['dest']
        start_date = form.data['date']
        start_time = form.data['time']



        return render(request, 'website/index.html', {'get_results': True, 'autofocus': True})


