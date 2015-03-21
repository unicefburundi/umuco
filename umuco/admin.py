from django.contrib import admin

from umuco.models import Raport

class RaportAdmin(admin.ModelAdmin):
    date_hierarchy = 'date'
    list_display = ('date', 'groupe','lampes_vendues', 'lampes_rechargees', 'montant' )

admin.site.register(Raport, RaportAdmin)
