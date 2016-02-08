import django_tables2 as tables
from django.utils.safestring import SafeString
from umuco.models import  NawenuzeGroup, Report

class ReportTable(tables.Table):
    group__colline = tables.Column(verbose_name='Colline', attrs={'th':{'data-footer-formatter':"totalTextFormatter"}})
    sold_lamps = tables.Column(verbose_name='Sold lamps', attrs={'th':{'data-footer-formatter':"sumFormatter"}})
    recharged_lamps = tables.Column(verbose_name='Recharged lamps', attrs={'th':{'data-footer-formatter':"sumFormatter"}})
    amount = tables.Column(verbose_name='Set aside ', attrs={'th':{'data-footer-formatter':"sumFormatter"}})
    group__commune = tables.Column(verbose_name='Commune')
    date_updated = tables.Column(verbose_name='Date ')
    edit = tables.TemplateColumn('<a href="#" class="btn btn-xs btn-info">Edit</a>', verbose_name='Edit')
    delete = tables.TemplateColumn('<a href="#" class="btn btn-xs btn-danger">Delete</a>', verbose_name='Delete')

    class Meta:
        attrs = {"class": "table ", "data-toggle":"table", "data-search":"true" ,"data-show-columns":"true" ,  "data-show-export":"true", 'data-export-types': "['csv','excel']", "data-show-footer":"true"}

    def render_group__colline(self, value):
        ID = NawenuzeGroup.objects.get(colline=value).id
        return SafeString('''<a href="/report/reports/%s">%s</a>''' % (ID, value))

    def render_edit(self, record):
        report = Report.objects.get(group__colline=record['group__colline'], date_updated=record['date_updated']).id
        return SafeString('''<a href="/report/edit/%s" class="btn btn-xs btn-info">Edit</a>''' % (report))


class ReportTable2(tables.Table):
    group__colline = tables.Column(verbose_name='Colline', attrs={'th':{'data-footer-formatter':"totalTextFormatter"}})
    sold_lamps = tables.Column(verbose_name='Sold lamps', attrs={'th':{'data-footer-formatter':"sumFormatter"}})
    recharged_lamps = tables.Column(verbose_name='Recharged lamps', attrs={'th':{'data-footer-formatter':"sumFormatter"}})
    amount = tables.Column(verbose_name='Set aside ', attrs={'th':{'data-footer-formatter':"sumFormatter"}})
    group__commune = tables.Column(verbose_name='Commune')
    date_updated = tables.Column(verbose_name='Date ')
    details = tables.TemplateColumn('<a href="#" >Details</a>')

    def render_date_updated(self, value, record):
        report = Report.objects.get(group__colline=record['group__colline'], date_updated=record['date_updated']).id
        return SafeString('''<a href="/report/edit/%s">%s</a>''' % (report, value))

    def render_details(self, record):
        ID = NawenuzeGroup.objects.get(colline=record['group__colline']).id
        return SafeString('''<a href="/report/reports/%s" class="btn btn-xs btn-default">Details</a>''' % (ID))

    class Meta:
        attrs = {"class": "table ", "data-toggle":"table", "data-search":"true" ,"data-show-columns":"true" ,  "data-show-export":"true", 'data-export-types': "['csv','excel']", "data-show-footer":"true"}