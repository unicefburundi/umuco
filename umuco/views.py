from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from jsonview.decorators import json_view
from umuco.utils import ExcelResponse
from django.http import JsonResponse
from umuco.models import Report, NawenuzeGroup, PhoneModel
import urllib

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
                phone_mobile = PhoneModel.objects.get_or_create(phone_number=urllib.unquote_plus(response_data["phone"]))
                nawenuze_group = NawenuzeGroup.objects.get_or_create(name=message[0].title())
                rapport = Report(amount=int(message[3]), sold_lamps=int(message[1]), recharged_lamps=int(message[2]), group=nawenuze_group[0], telephone=phone_mobile[0])
                rapport.save()
                return {'Ok': "True"}
            else:
                return {'Ok': "Ntibikwiye."}
        else:
            return {'Ok': "Mesage irera."}
    else:
        return {'Ok': "No Text"}

@json_view
def get_reports(request, name=None):
    raports = None
    if name==None:
        raports = Report.objects.values('amount', 'sold_lamps', 'recharged_lamps', 'date')
    else :
        raports = Report.objects.filter(group=name).values('amount', 'sold_lamps', 'recharged_lamps', 'date')
    mon = []
    rech = []
    vend = []
    for k, v in enumerate(raports):
        date = int(v["date"].strftime('%s'))*1000
        mon.append([date, int(v["amount"])])
        rech.append([date, int(v["recharged_lamps"])])
        vend.append([date, int(v["sold_lamps"])])

    resp = [{"name":"Amount", "data": mon}, {"name":"Recharged Lamps", "data": rech}, {"name":"Sold Lamps", "data":vend}]
    return JsonResponse(resp, safe=False)




def download_reports(request):
    queryset = Report.objects.all()
    columns = (
        'group_id',
        'date_updated',
        'recharged_lamps',
        'sold_lamps',
        'amount',
        'telephone_id')

    response = ExcelResponse(queryset, headers=columns)
    return response

def by_group(request, name=None):
    # import ipdb; ipdb.set_trace()
    response = get_reports(request=request, name=name)
    return render(request, "umuco/group_details.html", {"data" : response.content})

def all_groups(request):
    return render(request, "umuco/group_list.html")
