from rest_framework import serializers
from injira.models import Contact, Raport
from django.contrib.auth.models import User

class ContactSerializer( serializers.ModelSerializer):
    """
    Serializer to parse Contact data
    """
    class Meta:
        model = Contact
        fields = ('nom', 'mail', 'staff')


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'is_staff')

class RaportSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Raport
        fields = ('lampes_rechargees', 'lampes_vendues', 'montant')