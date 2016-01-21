from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_exempt
from jsonview.decorators import json_view
from umuco.utils import ExcelResponse, validate_date, split_message
from django.http import JsonResponse
from django.contrib.auth.forms import AuthenticationForm
from umuco.models import *
from django.conf import settings
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
    response_data = split_message(request)
    if PhoneModel.objects.filter(number=response_data['phone']).count() == 0:
        return {'Ok': "Pas", 'info_to_contact': "Vous n etes pas inscrit. Veuillez vous inscrire "}
    if response_data['text']:
        if response_data['text'] != "":
            message = response_data['text'].split("#")
            if len(message)  < 4:
                return {'Ok': "False", 'info_to_contact' : 'Vous avez donne peu de valeurs. Renvoyer le message corrige', 'raba': message }
            if len(message)  > 4 :
                return {'Ok': "False", 'info_to_contact' : 'Vous avez donne beaucoup de valeurs. Renvoyer le message corrige', 'raba': message }

            if len(message) == 4:
                group = PhoneModel.objects.get(number=response_data['phone']).group

                date_updated = validate_date(message[0])
                if date_updated.date() > datetime.datetime.today().date():
                    return {'Ok': "False", 'info_to_contact' : 'La date ne peut etre dans le futur. Renvoyer le message corrige', 'raba': date_updated}
                try:
                    message_3 = int(message[3])
                except Exception:
                    return {'Ok': "False", 'info_to_contact' : 'L argent epargnee n est pas valide. Renvoyer le message corrige ', 'error': message[3]}
                else:
                    if not isinstance(message_3, (int)) or  message_3 < 0 :
                        return {'Ok': "False", 'info_to_contact' : 'L argent epargnee n est pas valide. Renvoyer le message corrige', 'error': message_3}
                try:
                    message_2= int(message[2])
                except Exception:
                    return {'Ok': "False", 'info_to_contact' : 'Les lampes rechargees ne sont pas valides. Renvoyer le message corrige.', 'error': message[2]}
                else:
                    if not isinstance(message_2, (int)) or  message_2 < 0 :
                        return {'Ok': "False", 'info_to_contact' : 'Les lampes rechargees ne sont pas valides. Renvoyer le message corrige.', 'error': message_2}
                try:
                    message_1 = int(message[1])
                except Exception:
                    return {'Ok': "False", 'info_to_contact' : 'Les lampes vendues ne sont pas valides. Renvoyer le message corrige.', 'error': message[1]}
                else:
                    if not isinstance(message_1, (int)) or  message_1 < 0 :
                        return {'Ok': "False", 'info_to_contact' : 'Les lampes vendues ne sont pas valides. Renvoyer le message corrige.', 'error': message_1}
                repport,  created = Report.objects.get_or_create(group=group, date_updated=date_updated)
                if created:
                    repport.amount = message_3
                    repport.sold_lamps = message_1
                    repport.recharged_lamps = message_2
                    repport.save()
                elif (datetime.datetime.today() - date_updated).days > 6 :
                    return {'Ok': "Pas", 'info_to_contact' : 'Vous ne pouvez plus mettre a jours le rapport. Contacter le partenaire.', 'error': (datetime.datetime.today() - date_updated).days }
                else:
                    repport.amount = message_3
                    repport.sold_lamps = message_1
                    repport.recharged_lamps = message_2
                    repport.save()

                return JsonResponse({'Ok': "True", 'sold_lamps': message_1, 'recharged_lamps': message_2, 'amount': message_3, 'date': date_updated}, safe=False)


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
    print response
    return render(request, "umuco/group_details.html", {"data": response.content, "nawenuze_group": colline.title()})


def all_groups(request):
    return render(request, "umuco/group_list.html")


def get_cumulative(request, colline=None):
    reports = None
    if not colline:
        reports = Report.objects.values('amount', 'sold_lamps', 'recharged_lamps', 'date_updated').order_by('date_updated')
    else:
        reports = Report.objects.filter(group__colline=colline).values('amount','sold_lamps', 'recharged_lamps', 'date_updated').order_by('date_updated')
    if not reports:
        return JsonResponse(None, safe=False)

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


@csrf_exempt
@json_view
def add_lamps(request):
    response_data = split_message(request)
    if response_data['text'] != "":
            message = response_data['text'].split("#")

            response_data['message'] =  message
            if message[0] not in settings.PASSWORD:
                return {'Ok': "False", 'info_to_contact' : 'Le message est faux. Contacter le partenaire. ',  'error' : message[0]}
            if NawenuzeGroup.objects.filter(colline=message[1].upper()).count() == 0:
                return {'Ok': "False", 'info_to_contact' : "Le groupe n'existe pas. Contacter le partenaire." ,  'error' : message[1]}
            try:
                lampes= int(message[2])
            except Exception:
                return {'Ok': "False", 'info_to_contact' : 'Les lampes recues ne sont pas valides. Renvoyer le message corrige.', 'error': message[2]}
            else:
                if not isinstance(lampes, (int)) or  lampes < 0 :
                    return {'Ok': "False", 'info_to_contact' : 'Les lampes recues ne sont pas valides. Renvoyer le message corrige.', 'error': lampes}
    return response_data
