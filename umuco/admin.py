from django.contrib import admin

from umuco.models import Report, NawenuzeGroup, PhoneModel

class ReportAdmin(admin.ModelAdmin):
    date_hierarchy = 'date'
    list_display = ('date_updated', 'group','recharged_lamps', 'sold_lamps', 'amount')


class NawenuzeGroupAdmin(admin.ModelAdmin):
    list_display = ('colline', 'commune', 'day_of_meeting', 'province')
    search_fields = ('colline', 'commune',  'province')
    list_filter = ( 'day_of_meeting',)

admin.site.register(Report, ReportAdmin)
admin.site.register(NawenuzeGroup, NawenuzeGroupAdmin)
admin.site.register(PhoneModel)
