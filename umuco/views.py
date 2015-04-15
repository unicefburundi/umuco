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
    liste_data = request.body.split("&")
    for i in liste_data:
        response_data[i.split("=")[0]] = urllib.unquote_plus(i.split("=")[1])
    if response_data['text']  :
        if response_data['text'] != "":
            message = response_data['text'].split("#")
            if len(message) >= 3:
                phone_mobile = PhoneModel.objects.get_or_create(phone_number=response_data["phone"])
                nawenuze_group = NawenuzeGroup.objects.get_or_create(name=message[0].title().replace(" ", "_"))
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
    jsonresponses= get_cumulative(request=request, name=name)
    return jsonresponses



def download_reports(request):
    queryset = Report.objects.all()
    columns = (
        'group_id',
        'date',
        'recharged_lamps',
        'sold_lamps',
        'amount',
        'telephone_id')

    response = ExcelResponse(queryset, headers=columns)
    return response

def by_group(request, name=None):

    response = get_cumulative(request=request, name=name)
    return render(request, "umuco/group_details.html", {"data" : response.content, "nawenuze_group": name.title()})

def all_groups(request):
    return render(request, "umuco/group_list.html")

# @json_view
def get_cumulative(request, name=None):
    reports = None
    if name==None:
        reports = Report.objects.values('amount', 'sold_lamps', 'recharged_lamps', 'date').order_by('date')
    else:
        reports = Report.objects.filter(group=name).values('amount', 'sold_lamps', 'recharged_lamps', 'date').order_by('date')
    first_date = int(reports[0]["date"].strftime('%s'))*1000
    cumulative_amount =[[first_date, int(reports[0]['amount'])]]
    cumulative_recharged = [[first_date, int(reports[0]['recharged_lamps'])]]
    cumulative_sold = [[first_date, int(reports[0]['sold_lamps'])]]
    max_length= len(reports)
    for k in range(max_length)[1:]:
        date = int(reports[k]["date"].strftime('%s'))*1000
        cumulative_amount.append([date, int(reports[k]['amount'] + cumulative_amount[k-1][1])])
        cumulative_recharged.append([date, int(reports[k]['recharged_lamps'] + cumulative_recharged[k-1][1])])
        cumulative_sold.append([date, int(reports[k]['sold_lamps'] + cumulative_sold[k-1][1])])

    return JsonResponse([{"name":"Amount", "data": cumulative_amount}, {"name":"Recharged Lamps", "data": cumulative_recharged}, {"name":"Sold Lamps", "data": cumulative_sold}, {"Disposable" : cumulative_amount[max_length-1], "Charged": cumulative_recharged[max_length
        -1], "Selling": cumulative_sold[max_length-1]}], safe=False)