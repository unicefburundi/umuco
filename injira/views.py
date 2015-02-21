from django.shortcuts import render, render_to_response
from injira.models import Contact, Raport
from injira.serializers import ContactSerializer, UserSerializer
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from django.contrib.auth.models import User
from rest_framework import viewsets, serializers
from django.http import HttpResponse
from injira.forms import ContactForm
import json
import urllib
from django.views.decorators.csrf import csrf_exempt
from jsonview.decorators import json_view
from django.db.models import Count

class ContactMixin(object):
    """
    Mixin to inherit from
    Here we're setting the queryset and the serializer
    """
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer

class ContactList(ContactMixin, ListCreateAPIView):
    """
    Return a list of all the contacts, or
    create new ones
    """
    @json_view
    def pre_save(request):
        if request.method == 'POST':
            response_data = {}
            liste_data = request.body.split("&")
            for i in liste_data:
                response_data[i.split("=")[0]] = i.split("=")[1]
            return response_data

class ContactDetail(ContactMixin, RetrieveUpdateDestroyAPIView):
    """
    Return a specific contact, update it, or delete it.
    """
    pass


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'is_staff')

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


def save_contacts(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return HttpResponse("Form saved")
        else :
            print form.errors
    else:
        form = ContactForm()

    return render(request, 'injira/add_contact.html', {'form': form})


@csrf_exempt
@json_view
def save_embed(request):
    response_data = {}
    if request.method == "POST":
        response_data = {}
        liste_data = request.body.split("&")
        for i in liste_data:
            response_data[i.split("=")[0]] = i.split("=")[1]
        return response_data
    else:
        response_data['siPost'] = 'oui'

    return HttpResponse(json.dumps(response_data), content_type="application/json")

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

def overview(request):
    responses_pie =  Raport.objects.values('montant', 'lampes_vendues', 'lampes_rechargees', 'groupe').annotate(Count("id"))
    # import ipdb; ipdb.set_trace()
    for i,k in enumerate(responses_pie):
        responses_pie[i]['groupe'] = str(responses_pie[i]['groupe'])

    return render(request, 'pivotable.html', {'responses_pie_json': responses_pie})

def nvdchart(request):
    xdata = ["Apple", "Apricot", "Avocado", "Banana", "Boysenberries", "Blueberries", "Dates", "Grapefruit", "Kiwi", "Lemon"]
    ydata = [52, 48, 160, 94, 75, 71, 490, 82, 46, 17]
    chartdata = {'x': xdata, 'y': ydata}
    charttype = "pieChart"
    chartcontainer = 'piechart_container'
    data = {
        'charttype': charttype,
        'chartdata': chartdata,
        'chartcontainer': chartcontainer,
        'extra': {
            'x_is_date': False,
            'x_axis_format': '',
            'tag_script_js': True,
            'jquery_on_ready': False,
        }
    }
    return render_to_response('pivotable.html', data )
