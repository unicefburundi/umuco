from rest_framework import generics, permissions
from umuco.models import NawenuzeGroup, Report
from umuco.serializers import NawenuzeGroupSerializer, ReportSerializer


class NawenuzeGroupList(generics.ListCreateAPIView):
    model = NawenuzeGroup
    queryset = NawenuzeGroup.objects.all()
    serializer_class = NawenuzeGroupSerializer
    permission_classes = [permissions.AllowAny]


class NawenuzeGroupDetail(generics.RetrieveAPIView):
    model = NawenuzeGroup
    queryset = NawenuzeGroup.objects.all()
    serializer_class = NawenuzeGroupSerializer
    lookup_field = "colline"


class ReportList(generics.ListCreateAPIView):
    model = Report
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    permission_classes = [permissions.AllowAny]


class ReportDetail(generics.RetrieveUpdateDestroyAPIView):
    model = Report
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    permission_classes = [permissions.AllowAny]


class NawenuzeGroupReportList(generics.ListAPIView):
    model = Report
    queryset = Report.objects.all()
    serializer_class = ReportSerializer

    def get_queryset(self):
        queryset = super(NawenuzeGroupReportList, self).get_queryset()
        return queryset.filter(group__name=self.kwargs.get("name"))
