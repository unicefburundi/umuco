from rest_framework import serializers
from umuco.models import Raport

class RaportSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Raport
        fields = ('lampes_rechargees', 'lampes_vendues', 'montant','groupe')