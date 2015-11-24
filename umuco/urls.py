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
    url(r'^group/$', include(group_urls ) ),
    url(r'^group/(?P<colline>[0-9a-zA-Z_-]+)/reports$', NawenuzeGroupReportList.as_view(), name='groupreport-list'),
    url(r'^group/(?P<colline>[0-9a-zA-Z_-]+)$', NawenuzeGroupDetail.as_view(), name='group-detail'),
    url(r'^group/details/(?P<colline>[0-9a-zA-Z_-]+)$', views.by_group, name='group_detail'),
)
