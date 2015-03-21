from rest_framework import serializers
from umuco.models import Report

class ReportSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Report
        fields = ('recharged_lamps', 'sold_lamps', 'amount','group')