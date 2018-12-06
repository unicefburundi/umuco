from rest_framework import serializers
from umuco.models import NawenuzeGroup, Report


class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = (
            "recharged_lamps",
            "sold_lamps",
            "total_amount",
            "group",
            "telephone",
            "date",
            "pl_amount",
            "id",
        )


class NawenuzeGroupSerializer(serializers.ModelSerializer):
    colline = serializers.CharField(source="colline.name", read_only=True)
    commune = serializers.CharField(source="colline.commune.name", read_only=True)

    class Meta:
        model = NawenuzeGroup
        fields = ("colline", "day_of_meeting", "commune", "id")
