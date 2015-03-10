from django.conf.urls import patterns, url
from injira import views

urlpatterns = patterns('',
    url(r'^contacts/$', views.ContactList.as_view(), name = 'contact_list'),
    url(r'^contacts/(?P<pk>[0-9]+)$', views.ContactDetail.as_view(), name = 'contact_detail'),
    url(r'^add_contact/$', views.save_contacts, name='add_contact'),
    url(r'^ngaha/$', views.save_report, name='add_raport'),
    url(r'^utore/$', views.get_raports, name='get_raports'),
    url(r'^export/$', views.download_reports, name='download_reports')
)