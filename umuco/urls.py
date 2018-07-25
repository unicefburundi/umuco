from django.conf.urls import patterns, url, include
from umuco import views
from umuco.api import NawenuzeGroupList, NawenuzeGroupDetail, NawenuzeGroupReportList

group_urls = patterns('',
        url(r'^$', NawenuzeGroupList.as_view(), name='group-list')
)

urlpatterns = patterns('',
    url(r'^$', views.home, name='report_home'),
    url(r'^overview/$', views.get_reports, name='get_reports'),
    url(r'^overview/(?P<colline>[0-9a-zA-Z_-]+)$', views.get_reports, name='get_groups_reports'),
    url(r'^export/$', views.download_reports, name='download_reports'),
    url(r'^group/$', include(group_urls)),
    url(r'^add/group/$', views.submit_group, name='submit_group'),
    # for the api
    url(r'^group/(?P<colline>[0-9a-zA-Z_-]+)/reports$', NawenuzeGroupReportList.as_view(), name='groupreport-list'),
    url(r'^group/(?P<colline>[0-9a-zA-Z_-]+)$', NawenuzeGroupDetail.as_view(), name='group-detail'),
    url(r'^group/details/(?P<group>[0-9a-zA-Z_-]+)$', views.by_group, name='group_detail'),
    # for the simple class based view
    url(r'^reports/(?P<pk>\d+)$', views.NaweNuzeDetail.as_view(), name='reports_by_groups'),

    url(r'^user/add/$', views.UserCreate.as_view(), name='create_user'),
    url(r'^user/detail/(?P<pk>\d+)$', views.UserDetail.as_view(), name='detail_user'),
    #report
    url(r'^report_create/?$', views.ReportCreate.as_view(), name='report_create'),
    url(r'^list/$', views.ReportList.as_view(), name='report_list'),
    url(r'^edit/(?P<pk>\d+)$', views.ReportUpdate.as_view(), name='report_edit'),
    url(r'^delete/(?P<pk>\d+)$', views.ReportDelete.as_view(), name='report_delete'),
)
