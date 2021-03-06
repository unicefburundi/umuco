import django_tables2 as tables
from django.utils.safestring import SafeString
from umuco.models import  NawenuzeGroup, Report
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from bdiadmin.models import  Commune


class ReportTable(tables.Table):
    date_updated = tables.Column(verbose_name='Date ', attrs={'th':{'data-footer-formatter':"totalTextFormatter"}})
    sold_lamps = tables.Column(verbose_name=_('Sold lamps'), attrs={'th':{'data-footer-formatter':"sumFormatter"}})
    recharged_lamps = tables.Column(verbose_name=_('Recharged lamps'), attrs={'th':{'data-footer-formatter':"sumFormatter"}})
    total_amount = tables.Column(verbose_name=_('Total Set aside '), attrs={'th':{'data-footer-formatter':"sumFormatter"}})
    pl_amount = tables.Column(verbose_name=_('PL Set aside '), attrs={'th':{'data-formatter':"percentFormater"}})
    edit = tables.TemplateColumn('<a href="#" class="btn btn-xs btn-info">Edit</a>', verbose_name=_('Edit'))
    class Meta:
        attrs = {"class": "table ", "data-toggle":"table", "data-search":"true" ,"data-show-columns":"true" ,  "data-show-export":"true", 'data-export-types': "['csv','excel']", "data-show-footer":"true"}

    def render_group__colline(self, value):
        ID = NawenuzeGroup.objects.get(colline=value).id
        return SafeString('<a href='+reverse("report:reports_by_groups", args=[ID])+'>'+value+'</a>')

    def render_edit(self, record):
        report = Report.objects.get(group__colline=record['group__colline'], date_updated=record['date_updated']).id
        return SafeString('<a href='+reverse("report:report_edit", args=[report])+'>Edit</a>')

    def render_pl_amount(self, value, record):
        if record['total_amount'] == 0:
            return 0
        else :
            percent = 100*int(value)/record['total_amount']
            return percent


class ReportTable2(tables.Table):
    colline = tables.Column(verbose_name='Colline', attrs={'th':{'data-footer-formatter':"totalTextFormatter"}})
    commune = tables.Column(verbose_name='Commune')
    sold_lamps = tables.Column(verbose_name=_('Sold lamps'), attrs={'th':{'data-footer-formatter':"sumFormatter"}})
    recharged_lamps = tables.Column(verbose_name=_('Recharged lamps'), attrs={'th':{'data-footer-formatter':"sumFormatter"}})
    total_amount = tables.Column(verbose_name=_('Total Set aside '), attrs={'th':{'data-footer-formatter':"sumFormatter"}})
    pl_amount = tables.Column(verbose_name=_('PL Set aside '), attrs={'th':{'data-formatter':"percentFormater", 'data-footer-formatter':"sumpercentFormatter"}})
    date_updated = tables.Column(verbose_name='Date ')
    details = tables.TemplateColumn('<a href="#" >Details</a>')

    def render_date_updated(self, value, record):
        report = Report.objects.get(group__colline=record['colline'], date_updated=record['date_updated']).id
        return SafeString('''<a href="/fr/report/edit/%s">%s</a>''' % (report, value.name))

    def render_details(self, record):
        ID = NawenuzeGroup.objects.get(colline=record['colline']).id
        return SafeString('<a href='+reverse("report:reports_by_groups", args=[ID])+'>Details</a>')

    def render_colline(self, record):
        name = NawenuzeGroup.objects.get(colline=record['colline']).colline.name
        return name

    def render_commune(self, record):
        name = Commune.objects.get(pk=record['commune']).name
        return name

    def render_pl_amount(self, value, record):
        if record['total_amount'] == 0:
            return 0
        else :
            percent = 100*int(value)/record['total_amount']
            return percent

    class Meta:
        attrs = {"class": "table ", "data-toggle":"table", "data-search":"true" ,"data-show-columns":"true" ,  "data-show-export":"true", "data-side-pagination":"server", "data-pagination":"true", "data-page-list":[25, 50, 100] ,"data-export-types": "['csv','excel']", "data-show-footer":"true"}
