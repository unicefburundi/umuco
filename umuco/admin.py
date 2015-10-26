from django.contrib import admin

from umuco.models import Report, NawenuzeGroup, PhoneModel

class ReportAdmin(admin.ModelAdmin):
    date_hierarchy = 'date'
    list_display = ('date', 'group','recharged_lamps', 'sold_lamps', 'amount' , 'telephone')

class NawenuzeGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'person', 'phone', 'colline', 'day_of_gathering')

admin.site.register(Report, ReportAdmin)
admin.site.register(NawenuzeGroup, NawenuzeGroupAdmin)
admin.site.register(PhoneModel)