from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from jsonview.decorators import json_view
from umuco.utils import ExcelResponse
from django.http import JsonResponse
from umuco.models import Report, NawenuzeGroup

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
                nawenuze_group = NawenuzeGroup(name=message[0])
                nawenuze_group.save()
                rapport = Report(amount=int(message[3]), sold_lamps=int(message[1]), recharged_lamps=int(message[2]), group=nawenuze_group)
                rapport.save()
                return {'Ok': True}
            else:
                return {'Text incorect': True}
        else:
            return {'Text empty': True}
    else:
        return {'Text incorect': True}

@json_view
def get_reports(request):
    raports = Report.objects.values('amount', 'sold_lamps', 'recharged_lamps')
    mon = []
    rech = []
    vend = []
    for k, v in enumerate(raports):
        mon.append(int(v["amount"]))
        rech.append(int(v["recharged_lamps"]))
        vend.append(int(v["sold_lamps"]))
    resp = [{"name":"Amount", "data": mon, }, {"name":"Recharged Lamps", "data": rech,"type": "column"}, {"name":"Sold Lamps", "data":vend, "type": "column"}]
    return JsonResponse(resp, safe=False)




def download_reports(request):
    # import ipdb; ipdb.set_trace()
    queryset = Report.objects.all()
    columns = (
        'group',
        'date_updated',
        'recharged_lamps',
        'sold_lamps',
        'amount')

    response = ExcelResponse(queryset, headers=columns)
    return response