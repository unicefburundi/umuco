from django.contrib import admin
from import_export import resources
from import_export.admin import ExportMixin
from bdiadmin.models import *

class ProvinceResource(resources.ModelResource):
    class Meta:
        model = Province
        fields = ('name', 'code')

class ProvinceAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = ProvinceResource
    search_fields = ('name', 'code')
    list_display = ('name', 'code')


class CommuneResource(resources.ModelResource):
    class Meta:
        model = Commune
        fields = ('name', 'code')

class CommuneAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = CommuneResource
    search_fields = ('name', 'code')
    list_display = ('name', 'code')

class CollineResource(resources.ModelResource):
    class Meta:
        model = Colline
        fields = ('name', 'code')

class CollineAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = CollineResource
    search_fields = ('name', 'code')
    list_display = ('name', 'code')

admin.site.register(Province, ProvinceAdmin)
admin.site.register(Commune, CommuneAdmin)
admin.site.register(Colline, CollineAdmin)