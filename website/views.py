from django.shortcuts import render, get_object_or_404
from django.http import Http404, HttpResponse, JsonResponse
from django.template import loader

import pandas as pd

from .models import Datapoint
from .forms import InputForm


from django.views.decorators.cache import never_cache


from .sbb_api import send_request   

from .algorithm import *
from .preprocessing import *



# Create your views here.
@never_cache
def index(request):
    if request.method == 'GET':

        return render(request, 'website/index.html', {'get_results': False, 'autofocus': False})
    elif request.method == 'POST':
        try:
            form = InputForm(request.POST)
            model = load_model('website/model/xgb_model.pkl')

            
            # check for validity of locations!
            start = form.data['start']
            end = form.data['dest']


            start_date = form.data['date']
            start_time = form.data['time']


            start_time_iso = f"{start_date}T{start_time}:00"

            sections = send_request(start, end, start_time_iso)

            print(sections)


            data = []
            for s in sections:
                d = {}
                d['start_loc'] = s[0].replace('Ã¼', 'ü').replace('Ã¶','ö').replace('Ã¤','ä')
                d['start'] = s[1]
                d['end_loc'] = s[2].replace('Ã¼', 'ü').replace('Ã¶','ö').replace('Ã¤','ä')
                d['end'] = s[3]
                d['line'] = s[4]
                data.append(d)

            if not data:
                print("No data returned!")
                # return error message, e.g. no intercity on this route
                return render(request, 'website/index.html', {'get_results': False, 'autofocus': True, 'error': True, 'tech_error': False})


            data = pd.DataFrame(data)

            df = pre_process_data(data)

            pred, bottleneck = get_latest_reservation_ts(model, df)

            print(pred, bottleneck)

            s = pred*60
            d = datetime.timedelta(seconds=s)
            t = datetime.datetime.fromisoformat(start_time_iso) - d

            critical = data.iloc[bottleneck]
            print(critical)

            critical_start = critical['start_loc']
            critical_end = critical['end_loc']

      


            return render(request, 'website/index.html', {'get_results': True, 'tech_error': False, 'autofocus': True, 'date': start_date, 'time': start_time, 'start': start, 'end': end, 'prediction': t, 'critical_start': critical_start, 'critical_end': critical_end})
        except:
            return render(request, 'website/index.html', {'tech_error': True})

