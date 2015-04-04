from django.conf.urls import patterns, url
from umuco import views

urlpatterns = patterns('',
    url(r'^$', views.home, name='report_home'),
    url(r'^add/$', views.save_report, name='add_report'),
    url(r'^overview/$', views.get_reports, name='get_reports'),
    url(r'^export/$', views.download_reports, name='download_reports'),
    url(r'^groups/$', views.by_group, name='by_group'),
)