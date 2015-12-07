import django_tables2 as tables
from django.utils.safestring import SafeString
from umuco.models import  NawenuzeGroup

class ReportTable(tables.Table):
    group__colline = tables.Column(verbose_name='Colline', attrs={'th':{'data-footer-formatter':"totalTextFormatter"}})
    sold_lamps = tables.Column(verbose_name='Sold lamps', attrs={'th':{'data-footer-formatter':"sumFormatter"}})
    recharged_lamps = tables.Column(verbose_name='Recharged lamps', attrs={'th':{'data-footer-formatter':"sumFormatter"}})
    amount = tables.Column(verbose_name='Amount', attrs={'th':{'data-footer-formatter':"sumFormatter"}})
    group__commune = tables.Column(verbose_name='Commune')
    date_updated = tables.Column(verbose_name='Date')

    class Meta:
        attrs = {"class": "table ", "data-toggle":"table", "data-search":"true" ,"data-show-columns":"true" ,  "data-show-export":"true", 'data-export-types': "['csv','excel']", "data-show-footer":"true"}

    def render_group__colline(self, value):
        ID = NawenuzeGroup.objects.get(colline=value).id
        return SafeString('''<a href="/report/reports/%s">%s</a>''' % (ID, value))