from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from jsonview.decorators import json_view
from injira.utils import ExcelResponse
from django.http import JsonResponse
from injira.models import Raport

@csrf_exempt
def home(request):
    return render(request, "muco_layout.html")

@csrf_exempt
@json_view
def save_report(request):
    response_data = {}
    # import ipdb; ipdb.set_trace()
    liste_data = request.body.split("&")
    for i in liste_data:
        response_data[i.split("=")[0]] = i.split("=")[1]
    if response_data['text']  :
        if response_data['text'] != "":
            message = response_data['text'].split("%2A")
            if len(message) >= 3:
                rapport = Raport(montant=int(message[3]), lampes_vendues=int(message[1]), lampes_rechargees=int(message[2]), groupe=message[0])
                rapport.save()
                return {'Ok': True}
            else:
                return {'Text incorect': True}
        else:
            return {'Text empty': True}
    else:
        return {'Text incorect': True}

def montant_pertime(request):
    data = Raport.objects.values('montant', 'date')
    timess = []
    for i in data:
        timess.append(i['montant'])
        timess.append(str(i['date']))
        i['date'] = str(i['date'])
    return render(request, 'turabe.html', {'data' : data, 'timess':timess})


@json_view
def get_reports(request):
    raports = Raport.objects.values('montant', 'lampes_vendues', 'lampes_rechargees')
    mon = []
    rech = []
    vend = []
    for k, v in enumerate(raports):
        mon.append(int(v["montant"]))
        rech.append(int(v["lampes_rechargees"]))
        vend.append(int(v["lampes_vendues"]))
    resp = [{"name":"Montant", "data": mon, }, {"name":"Lampes rechargees", "data": rech,"type": "column"}, {"name":"lampes vendues", "data":vend, "type": "column"}]
    return JsonResponse(resp, safe=False)




def download_reports(request):
    # import ipdb; ipdb.set_trace()
    queryset = Raport.objects.all()
    columns = (
        'groupe',
        'date_updated',
        'lampes_rechargees',
        'lampes_vendues',
        'montant')

    response = ExcelResponse(queryset, headers=columns)
    return response