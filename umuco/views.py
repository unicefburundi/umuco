from django.shortcuts import render
from django.core.urlresolvers import reverse, reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from jsonview.decorators import json_view
from umuco.utils import ExcelResponse, validate_date, split_message, email_report_flagged
from django.http import JsonResponse, HttpResponseRedirect
from django.contrib.auth.forms import AuthenticationForm
from umuco.models import *
from django.conf import settings
from umuco.forms import *
import datetime
from django.views.generic import CreateView, DetailView
from django.contrib.auth import get_user_model
from django_tables2 import RequestConfig
from umuco.tables import ReportTable, ReportTable2
from django.db.models import Sum
from django.views.generic.edit import UpdateView, DeleteView
from django.views.generic import ListView
from bdiadmin.forms import *


User = get_user_model()


@csrf_exempt
def home(request):
    form = AuthenticationForm()
    return render(request, "muco_layout.html", {'form': form})


def analytics(request):
    groups = Report.objects.values('group__colline','group__colline__commune').distinct()
    statistics = []
    for i in groups:
        reports = Report.objects.filter(group__colline=i['group__colline'], group__colline__commune=i['group__colline__commune'])
        group = i
        group.update(reports.aggregate(sold_lamps=Sum('sold_lamps')))
        group.update(reports.aggregate(recharged_lamps=Sum('recharged_lamps')))
        group.update(reports.aggregate(amount=Sum('amount')))
        statistics.append(group)
    statistics = ReportTable2(statistics)
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

                # cost
                cost_expected = (message_1 * group.cost_lamp + message_2*group.cost_recharge)
                if message_3 != 0 and message_3 != cost_expected :
                    sent = email_report_flagged(Organization.objects.get(name='CPS').user.email, 'le groupe {0} (de la commune {1}) a raporte le {2} avoir avoir epargne {3} fbu alors que cela valait juste {4}'.format(group, group.commune, date_updated.strftime("%d-%m-%Y"), message_3, cost_expected))
                    print sent
                # sold
                solds = Report.objects.filter(group=group).aggregate(Sum('sold_lamps'))
                if message_1 != 0 and group.lamps_in_stock != solds['sold_lamps__sum']:
                    sent = email_report_flagged(Organization.objects.get(name='CPS').user.email, 'le groupe {0} (de la commune {1}) a raporte le {2} avoir vendu plus de lampes ({3}) qu il n en restait en stock({4})'.format(group, group.commune, date_updated.strftime("%d-%m-%Y"), message_1, (group.lamps_in_stock - solds['sold_lamps__sum'])))
                    print sent


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
        reports = Report.objects.filter(group__colline=nawenuzegroup).values('group__colline', 'group__commune', 'sold_lamps', 'recharged_lamps', 'amount', 'date_updated', 'group__lamps_in_stock')
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
        if message[1] not in settings.PASSWORD:
            return {'Ok': "Pas", 'info_to_contact' : 'Le message est faux. Contacter le partenaire. ',  'error' : message[1]}
        if NawenuzeGroup.objects.filter(colline=message[2].upper()).count() == 0:
            return {'Ok': "False", 'info_to_contact' : "Le groupe n'existe pas. Contacter le partenaire." ,  'error' : message[2]}
        try:
            lamps= int(message[3])
        except Exception:
            return {'Ok': "False", 'info_to_contact' : 'Les lampes recues ne sont pas valides. Renvoyer le message corrige.', 'error': message[3]}
        else:
            if not isinstance(lamps, (int)) or  lamps < 0 :
                return {'Ok': "False", 'info_to_contact' : 'Les lampes recues ne sont pas valides. Renvoyer le message corrige.', 'error': lamps}
        date_received = validate_date(message[4])
        if date_received.date() > datetime.datetime.today().date():
            return {'Ok': "False", 'info_to_contact' : 'La date ne peut etre dans le futur. Renvoyer le message corrige.', 'raba': date_received}
        group = NawenuzeGroup.objects.get(colline=message[2].upper())
        reception , created = Reception.objects.get_or_create(group=group, lamps_received=lamps, date_received=date_received)
        if created:
            group.lamps_in_stock += lamps
            group.save()
    return {'Ok': "True", 'info_to_contact' : 'Le groupe de la colline {0}( commune {3}) a recu {1} lampes le {2}. Merci a bientot.'.format(group, lamps, date_received.strftime("%d-%m-%Y"), group.commune) , 'raba': date_received.strftime("%d-%m-%Y")}


class ReportList(ListView):
    model = Report

class ReportUpdate(UpdateView):
    model = Report
    fields = ['recharged_lamps','sold_lamps','amount','group']

    def get_success_url(self, **kwargs):
        return reverse('reports_by_groups2', kwargs={'pk': self.object.group.id})

class ReportDelete(DeleteView):
    model = Report
    success_url = reverse_lazy('report_list')


class PhoneModelCreate(CreateView):
    model = PhoneModel
    fields = '__all__'
    success_url = reverse_lazy('groups')

class NaweNuzeCreate(CreateView):
    model = NawenuzeGroup
    fields = ('province', 'commune', 'colline')
    exclude = ('lamps_in_stock','cost_lamp','cost_recharge')
    success_url = reverse_lazy('groups')

def submit_group(request):
    form = NaweNuzeForm()
    phonemodel_formset = GroupFormset(instance=NawenuzeGroup())
    province_form = ProvinceForm()
    commune_form = CommuneForm()
    colline_form = CollineForm()
    phone_form = PhoneModelForm()
    if request.POST:
        form = NaweNuzeForm(request.POST)
        if form.is_valid():
            group = form.save(commit=False)
            phonemodel_formset = GroupFormset(request.POST, instance=group)
            if phonemodel_formset.is_valid():
                group.save()
                phonemodel_formset.save()
                return HttpResponseRedirect(reverse('groups'))
    else:
        form = NaweNuzeForm()
        phonemodel_formset = GroupFormset(instance=NawenuzeGroup())
    return render(request, "umuco/group_submit.html", {
        "form": form,
        "phonemodel_formset": phonemodel_formset,
        "province_form" : province_form,
        "commune_form" : commune_form,
        "colline_form" : colline_form,
        "phone_form" : phone_form
    })