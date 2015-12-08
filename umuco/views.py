from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_exempt
from jsonview.decorators import json_view
from umuco.utils import ExcelResponse
from django.http import JsonResponse
from django.contrib.auth.forms import AuthenticationForm
from umuco.models import *
import urllib
from umuco.forms import *
import datetime
from django.views.generic import CreateView, DetailView
from django.contrib.auth import get_user_model
from django_tables2 import RequestConfig
from umuco.tables import ReportTable
from django.db.models import Sum


User = get_user_model()


@csrf_exempt
def home(request):
    form = AuthenticationForm()
    return render(request, "muco_layout.html", {'form': form})


def analytics(request):
    groups = Report.objects.values('group__colline','group__commune').distinct()
    statistics = []
    for i in groups:
        reports = Report.objects.filter(group__colline=i['group__colline'], group__commune=i['group__commune'])
        group = i
        group.update(reports.aggregate(sold_lamps=Sum('sold_lamps')))
        group.update(reports.aggregate(recharged_lamps=Sum('recharged_lamps')))
        group.update(reports.aggregate(amount=Sum('amount')))
        statistics.append(group)
    statistics = ReportTable(statistics)
    statistics.exclude = ('date_updated', )
    RequestConfig(request).configure(statistics)
    return render(request, 'umuco/analytics.html', {'statistics': statistics})


@csrf_exempt
@json_view
def save_report(request):
    response_data = {}
    liste_data = request.body.split("&")
    for i in liste_data:
        response_data[i.split("=")[0]] = urllib.unquote_plus(i.split("=")[1])
    if PhoneModel.objects.filter(number=response_data['phone']).count() == 0:
        return {'Ok': "Ntiwanditswe."}
    if response_data['text']:
        if response_data['text'] != "":
            message = response_data['text'].split("#")
            if len(message) >= 3:
                group = PhoneModel.objects.get(number=response_data['phone']).group
                date_updated = '20{0}-{1}-{2}'.format(message[0][-2:], message[0][2:4], message[0][:2])
                rapport = Report(amount=int(message[3]), sold_lamps=int(message[1]), recharged_lamps=int(message[2]), group=group, date_updated=datetime.datetime.strptime(date_updated, '%Y-%m-%d'))
                rapport.save()

                return JsonResponse({'Ok': "True", 'sold_lamps': int(message[1]), 'recharged_lamps': int(message[2]), 'amount': int(message[3]), 'date': date_updated}, safe=False)
            else:
                return {'Ok': "Ntibikwiye."}
        else:
            return {'Ok': "Mesage irera."}
    else:
        return {'Ok': "No Text"}


@json_view
def get_reports(request, colline=None):
    jsonresponses = get_cumulative(request=request, colline=colline)
    return jsonresponses


def download_reports(request):
    queryset = Report.objects.all()
    columns = (
        'group_id',
        'date_updated',
        'recharged_lamps',
        'sold_lamps',
        'amount',)

    response = ExcelResponse(queryset, headers=columns)
    return response


def by_group(request, colline=None):

    response = get_cumulative(request=request, colline=colline)
    return render(request, "umuco/group_details.html", {"data": response.content, "nawenuze_group": colline.title()})


def all_groups(request):
    return render(request, "umuco/group_list.html")


def get_cumulative(request, colline=None):
    reports = None
    if not colline:
        reports = Report.objects.values('amount', 'sold_lamps', 'recharged_lamps', 'date_updated').order_by('date_updated')
    else:
        reports = Report.objects.filter(group__colline=colline).values('amount','sold_lamps', 'recharged_lamps', 'date_updated').order_by('date_updated')
    first_date = int(reports[0]["date_updated"].strftime('%s'))*1000
    cumulative_amount = [[first_date, int(reports[0]['amount'])]]
    cumulative_recharged = [[first_date, int(reports[0]['recharged_lamps'])]]
    cumulative_sold = [[first_date, int(reports[0]['sold_lamps'])]]
    max_length = len(reports)
    for k in range(max_length)[1:]:
        date = int(reports[k]["date_updated"].strftime('%s'))*1000
        cumulative_amount.append([date, int(reports[k]['amount'] + cumulative_amount[k-1][1])])
        cumulative_recharged.append([date, int(reports[k]['recharged_lamps'] + cumulative_recharged[k-1][1])])
        cumulative_sold.append([date, int(reports[k]['sold_lamps'] + cumulative_sold[k-1][1])])

    return JsonResponse([{"name": "Amount", "data": cumulative_amount}, {"name":"Recharged Lamps", "data": cumulative_recharged}, {"name":"Sold Lamps", "data": cumulative_sold}, {"Disposable": cumulative_amount[max_length-1], "Charged": cumulative_recharged[max_length
        -1], "Selling": cumulative_sold[max_length-1]}], safe=False)


class UserCreate(CreateView):
    model = User
    form_class = UserCreationForm

    def get_success_url(self):
        return reverse('detail_user', kwargs={'pk': self.object.id})


class UserDetail(DetailView):
    model = User


class NaweNuzeDetail(DetailView):
    model = NawenuzeGroup

    def get_context_data(self, **kwargs):
        context = super(NaweNuzeDetail, self).get_context_data(**kwargs)
        nawenuzegroup = context['object']
        reports = Report.objects.filter(group__colline=nawenuzegroup).values('group__colline', 'group__commune', 'sold_lamps', 'recharged_lamps', 'amount', 'date_updated')
        reports = ReportTable(reports)
        RequestConfig(self.request).configure(reports)
        context['reports'] = reports
        return context
