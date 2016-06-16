# -*- coding: utf-8 -*-

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
from django.db.models import F
from django.contrib.auth.decorators import login_required
from django.contrib import messages

User = get_user_model()


def landing(request):
    form = AuthenticationForm()
    return render(request, "landing_page.html", {'form': form})

@login_required
@csrf_exempt
def home(request):
    form = AuthenticationForm()
    return render(request, "muco_layout.html", {'form': form})


def analytics(request):
    groups = Report.objects.annotate(colline=F('group__colline')).annotate(commune=F('group__colline__commune')).values('colline','commune').distinct()
    statistics = []
    for i in groups:
        reports = Report.objects.filter(group__colline=i['colline'], group__colline__commune=i['commune'])
        group = i
        group.update(reports.aggregate(sold_lamps=Sum('sold_lamps')))
        group.update(reports.aggregate(recharged_lamps=Sum('recharged_lamps')))
        group.update(reports.aggregate(total_amount=Sum('total_amount')))
        group.update(reports.aggregate(pl_amount=Sum('pl_amount')))
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
        return {'Ok': "Pas", 'info_to_contact': "Ntimwanditse. Banza mwiyandikishe."}
    if response_data['text']:
        if response_data['text'] != "":
            message = response_data['text'].split("#")
            if len(message)  < 5:
                return {'Ok': "False", 'info_to_contact' : 'Mwatanze ibiharuro bike. Subira murungike mesaje yanditse neza.', 'raba': message }
            if len(message)  > 5 :
                return {'Ok': "False", 'info_to_contact' : 'Mwatanze ibitigiri vyinshi. Subirurungike ibiharuro.', 'raba': message }

            if len(message) == 5:
                group = PhoneModel.objects.get(number=response_data['phone']).group
                date_updated = validate_date(message[0])

                if date_updated.date() > datetime.datetime.today().date():
                    return {'Ok': "False", 'info_to_contact' : 'Itariki ntishobora kuba muri kazoza. SUbira urungike mesaje.', 'raba': date_updated}
                if (date_updated.weekday() +1 ) != group.day_of_meeting:
                    return {'Ok': "False", 'info_to_contact' : 'Itariki itegerezwa kuba umusi muhurirako. Subira urungike mesaje yanditse neza.', 'raba': date_updated}
                if (datetime.datetime.today() - date_updated).days > 7 :
                    return {'Ok': "Pas", 'info_to_contact' : 'Ntibigishoboka ko murungika raporo. Vugana na C.P.E.S.', 'error': (datetime.datetime.today() - date_updated).days }

                try:
                    message_1 = int(message[1])
                except Exception:
                    return {'Ok': "False", 'info_to_contact' : 'Amatara yagurishijwe ntiyanditse neza. Subira urungike raporo neza.', 'error': message[1]}
                else:
                    if not isinstance(message_1, (int)) or  message_1 < 0 :
                        return {'Ok': "False", 'info_to_contact' : 'Amatara yagurishijwe ntiyanditse neza. Subira urungike raporo neza.', 'error': message_1}
                try:
                    message_2= int(message[2])
                except Exception:
                    return {'Ok': "False", 'info_to_contact' : 'Amatara yasharijwe ntiyanditse neza. Subira urungike raporo neza.', 'error': message[2]}
                else:
                    if not isinstance(message_2, (int)) or  message_2 < 0 :
                        return {'Ok': "False", 'info_to_contact' : 'Amatara yasharijwe ntiyanditse neza. Subira urungike raporo neza.', 'error': message_2}

                try:
                    message_3 = int(message[3])
                except Exception:
                    return {'Ok': "False", 'info_to_contact' : 'Amafaranga yaziganijwe ntiyanditse neza. Subira urungike raporo neza.', 'error': message[3]}
                else:
                    if not isinstance(message_3, (int)) or  message_3 < 0 :
                        return {'Ok': "False", 'info_to_contact' : 'Le montant total epargnee n est pas valide. Subira urungike raporo neza.', 'error': message_3}

                try:
                    message_4 = int(message[4])
                except Exception:
                    return {'Ok': "False", 'info_to_contact' : 'Amafaranga yaziganijwe ntiyanditse neza. Subira urungike raporo neza.', 'error': message[4]}
                else:
                    if not isinstance(message_4, (int)) or  message_4 < 0 :
                        return {'Ok': "False", 'info_to_contact' : 'Amafaranga yaziganijwe ntiyanditse neza. Subira urungike raporo neza.', 'error': message_4}

                repport,  created = Report.objects.get_or_create(group=group, date_updated=date_updated)
                if created:
                    repport.sold_lamps = message_1
                    repport.recharged_lamps = message_2
                    repport.total_amount = message_3
                    repport.pl_amount = message_4
                    repport.save()
                elif (datetime.datetime.today() - date_updated).days > 6 :
                    return {'Ok': "Pas", 'info_to_contact' : 'Ntaruhusha mugifise bwugutanga iyi raporo. Vugana na C.P.E.S.', 'error': (datetime.datetime.today() - date_updated).days }
                # sold
                solds = Report.objects.filter(group=group).aggregate(Sum('sold_lamps'))
                if message_1 != 0 and group.lamps_in_stock < solds['sold_lamps__sum']:
                    sent = email_report_flagged(Organization.objects.get(name='CPES').partner.user.email, 'Umugwi {0} (womuri komine {1}) wavuze kuwa {2} kowagurishije amatara {3} ariko hari hasigaye muri stoc amatara {4}'.format(group, group.colline.commune, date_updated.strftime("%d-%m-%Y"), message_1, (group.lamps_in_stock - solds['sold_lamps__sum'])))
                    print sent
                    return {'Ok': False, 'info_to_contact': "Nta matara mwari mugisigaranye. Vugana na C.P.E.S."}
                else:
                    repport.sold_lamps = message_1
                    repport.recharged_lamps = message_2
                    repport.total_amount = message_3
                    repport.pl_amount = message_4
                    repport.save()


            return JsonResponse({'Ok': "True", 'sold_lamps': message_1, 'recharged_lamps': message_2, 'total_amount': message_3, 'pl_amount': message_4, 'date': date_updated}, safe=False)


@json_view
def get_reports(request, colline=None):
    jsonresponses = get_cumulative(request=request, colline=colline)
    return jsonresponses


@login_required
def download_reports(request):
    queryset = Report.objects.all()
    columns = (
        'group_id',
        'date_updated',
        'recharged_lamps',
        'sold_lamps',
        'total_amount',)

    response = ExcelResponse(queryset, headers=columns)
    return response


def by_group(request, colline=None):
    response = get_cumulative(request=request, colline=colline)
    groupe, created = NawenuzeGroup.objects.get_or_create(colline__name=colline)
    rapporteurs = PhoneModel.objects.filter(group__colline__name=colline)
    print response
    return render(request, "umuco/group_details.html", {"data": response.content, "nawenuze_group": colline.title(), 'groupe': groupe, 'rapporteurs': rapporteurs})

@login_required
def all_groups(request):
    return render(request, "umuco/group_list.html")


def get_cumulative(request, colline=None):
    reports = None
    if not colline:
        reports = Report.objects.values('total_amount', 'sold_lamps', 'recharged_lamps', 'date_updated', 'pl_amount').order_by('date_updated')
    else:
        reports = Report.objects.filter(group__colline__name=colline).values('total_amount','sold_lamps', 'recharged_lamps', 'date_updated', 'pl_amount').order_by('date_updated')
    if not reports:
        return JsonResponse(None, safe=False)

    first_date = int(reports[0]["date_updated"].strftime('%s'))*1000
    cumulative_total_amount = [[first_date, int(reports[0]['total_amount'])]]
    cumulative_recharged = [[first_date, int(reports[0]['recharged_lamps'])]]
    cumulative_sold = [[first_date, int(reports[0]['sold_lamps'])]]
    cumulative_pl_amount = [[first_date, int(reports[0]['pl_amount'])]]
    max_length = len(reports)
    for k in range(max_length)[1:]:
        date = int(reports[k]["date_updated"].strftime('%s'))*1000
        cumulative_total_amount.append([date, int(reports[k]['total_amount'] + cumulative_total_amount[k-1][1])])
        cumulative_recharged.append([date, int(reports[k]['recharged_lamps'] + cumulative_recharged[k-1][1])])
        cumulative_sold.append([date, int(reports[k]['sold_lamps'] + cumulative_sold[k-1][1])])
        cumulative_pl_amount.append([date, int(reports[k]['pl_amount'] + cumulative_pl_amount[k-1][1])])

    return JsonResponse([{"name": "Total épargné", "data": cumulative_total_amount}, {"name":"Lampes rechargées", "data": cumulative_recharged}, {"name":"Lampes vendues", "data": cumulative_sold}, {"name":"PL épargné", "data": cumulative_pl_amount},{"Disposable": cumulative_total_amount[max_length-1], "Charges": cumulative_recharged[max_length
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
        reports = Report.objects.filter(group=nawenuzegroup).values('group__colline', 'group__colline__commune', 'sold_lamps', 'recharged_lamps', 'total_amount', 'date_updated', 'group__lamps_in_stock', 'pl_amount')
        reports = ReportTable(reports)
        RequestConfig(self.request).configure(reports)
        context['reports'] = reports
        return context


@csrf_exempt
@json_view
def add_lamps(request):
    """Add reception of lamps"""
    response_data = split_message(request)
    if response_data['text'] != "":
        message = response_data['text'].split("#")
        response_data['message'] =  message
        if message[1] not in settings.PASSWORD:
            return {'Ok': "Pas", 'info_to_contact' : 'Mesaje siyo. Vugana na C.P.E.S.. ',  'error' : message[1]}
        if NawenuzeGroup.objects.filter(colline__name=message[2].title()).count() == 0:
            return {'Ok': "False", 'info_to_contact' : "Umugwi ntubaho. Vugana na C.P.E.S.." ,  'error' : message[2]}
        try:
            lamps= int(message[3])
        except Exception:
            return {'Ok': "False", 'info_to_contact' : 'Amatara mwaronse ntiyanditswe neza. Subira urungike raporo neza.', 'error': message[3]}
        else:
            if not isinstance(lamps, (int)) or  lamps < 0 :
                return {'Ok': "False", 'info_to_contact' : 'Amatara mwaronse ntiyanditswe neza. Subira urungike raporo neza.', 'error': lamps}
        date_received = validate_date(message[4])
        if date_received.date() > datetime.datetime.today().date():
            return {'Ok': "False", 'info_to_contact' : 'Itariki ntishobora kuba muri kazoza. Subira urungike raporo neza.', 'raba': date_received}
        group = NawenuzeGroup.objects.get(colline__name=message[2].title())
        reception , created = Reception.objects.get_or_create(group=group, lamps_received=lamps, date_received=date_received)
        if created:
            group.lamps_in_stock += lamps
            group.save()
    return {'Ok': "True", 'info_to_contact' : 'Umugwi ku mutumba {0} (komine {3}) waronse amatara {1} kuwa{2}. Murakoze.'.format(group, lamps, date_received.strftime("%d-%m-%Y"), group.colline.commune) , 'raba': date_received.strftime("%d-%m-%Y")}


class ReportList(ListView):
    model = Report

class ReportUpdate(UpdateView):
    model = Report
    fields = ['recharged_lamps','sold_lamps','total_amount','group', 'date_updated', 'pl_amount']
    # print(self)

    def get_success_url(self, **kwargs):
        return reverse('reports_by_groups2', kwargs={'pk': self.object.group.id})

    def get_initial(self):
        return {'group' : self.object.group}

class ReportDelete(DeleteView):
    model = Report
    success_url = reverse_lazy('report_list')

class ReportCreate(CreateView):
    template_name = 'umuco/report_create.html'
    model = Report
    fields = '__all__'

    def render_to_response(self, context, **response_kwargs):
        self.request.current_app = self.request.resolver_match.namespace
        return super(ReportCreate, self).render_to_response(context, **response_kwargs)

    def get_success_url(self):
        return reverse('report:report_list',  current_app=self.request.resolver_match.namespace)


class PhoneModelCreate(CreateView):
    model = PhoneModel
    fields = '__all__'
    success_url = reverse_lazy('groups')

class NaweNuzeCreate(CreateView):
    model = NawenuzeGroup
    fields = ('province', 'commune', 'colline')
    exclude = ('lamps_in_stock','cost_lamp','cost_recharge')
    success_url = reverse_lazy('groups')

@login_required
def submit_group(request):
    form = NaweNuzeForm()
    phonemodel_formset = GroupFormset(instance=NawenuzeGroup())
    province_form = ProvinceForm()
    commune_form = CommuneForm()
    colline_form = CollineForm()
    phone_form = PhoneModelForm()
    if request.POST:
        form = NaweNuzeForm({'province': request.POST.get('province'), 'day_of_meeting': request.POST.get('day_of_meeting'), 'colline' : request.POST.get('colline'), 'commune' : request.POST.get('commune')})
        try:
            colline = Colline.objects.get(id=int(request.POST.get('colline')))
        except:
            form._errors['colline'] = "Colline doesn't exist"
            return False
        else:
            form.colline = colline
        try:
            commune = Commune.objects.get(id=int(request.POST.get('commune')))
        except:
            form._errors['commune'] = "Commune doesn't exist"
            return False
        else:
            form.commune = commune

        if form.is_valid():
            group = form.save(commit=False)
            phonemodel_formset = GroupFormset(request.POST, instance=group)
            if phonemodel_formset.is_valid():
                group.save()
                phonemodel_formset.save()
                messages.add_message(request, messages.SUCCESS, 'Saved group and sent SMS')
                return HttpResponseRedirect(reverse('report:group_detail', kwargs={'colline':group.colline}))

        else:
            form = form
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