from django.shortcuts import render, get_object_or_404
from django.http import Http404, HttpResponse, JsonResponse
from django.template import loader

import pandas as pd

from .models import Datapoint
from .forms import InputForm


from django.views.decorators.cache import never_cache


from .sbb_api import send_request

# Create your views here.
@never_cache
def index(request):
    if request.method == 'GET':
        return render(request, 'website/index.html', {'get_results': False, 'autofocus': False})
    elif request.method == 'POST':
        form = InputForm(request.POST)
        

        # check for validity of locations!
        start = form.data['start']
        end = form.data['dest']


        start_date = form.data['date']
        start_time = form.data['time']


        start_time_iso = f"{start_date}T{start_time}:00"

        sections = send_request(start, end, start_time_iso)


        data = []
        for s in sections:
            d = {}
            d['start_loc'] = s[0]
            d['start'] = s[1]
            d['end_loc'] = s[2]
            d['end'] = s[3]
            d['line'] = s[4]
            data.append(d)

        df = pd.DataFrame(data)
      


        return render(request, 'website/index.html', {'get_results': True, 'autofocus': True})


