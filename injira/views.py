from django.shortcuts import render
from injira.models import Contact
from injira.serializers import ContactSerializer, UserSerializer
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from django.contrib.auth.models import User
from rest_framework import viewsets, serializers
from django.http import HttpResponse,  HttpResponseBadRequest
from injira.forms import ContactForm
import json
from rest_framework.permissions import  AllowAny
from rest_framework.decorators import permission_classes
from django.views.decorators.csrf import csrf_exempt

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

    def pre_save(request):
        valeurs = ''
        if request.method == 'POST':
            valeurs = request.POST[0]
            print valeurs

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
@permission_classes((AllowAny, ))
def save_embed(request):
    # permission_classes = (AllowAny,)
    response_data = {}
    if request.method == "POST":
        # form = ContactForm(request.POST)
        # if form.is_valid():
        #     response_data['forme'] = 'irivalide'
        #     r = form.cleaned_data['values']
        #     jsons = r.json()
        #     serializer = ContactSerializer(data=jsons)
        #     if serializer.is_valid():
        #         response_data['serializer'] = 'yashoboye kuba serialized'
        #         embed = serializer.save()
        #         return HttpResponse(json.dumps(embed), content_type="application/json")
        # else:
        #     return HttpResponseBadRequest(json.dumps(form.errors),
        #         content_type="application/json")
        #     response_data['erreurs forms'] = 'oui'
        return HttpResponse("%s %s" % (request.method, request.body))
    else:
        # form = ContactEmbeded()
        response_data['siPost'] = 'oui'

    return HttpResponse(json.dumps(response_data), content_type="application/json")
