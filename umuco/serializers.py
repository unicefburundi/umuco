from rest_framework import serializers
from umuco.models import Report, NawenuzeGroup

class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = ('recharged_lamps', 'sold_lamps', 'amount','group', 'telephone', 'date')

class NawenuzeGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = NawenuzeGroup
        fields = ('colline', 'commune', 'day_of_meeting')