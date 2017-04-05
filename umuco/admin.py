from django.contrib import admin
from import_export import resources
from import_export.admin import ExportMixin
from umuco.models import *
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordResetForm
from django.utils.crypto import get_random_string
from umuco.forms import UserCreationForm
from authtools.admin import NamedUserAdmin

User = get_user_model()


class UserAdmin(NamedUserAdmin):
    """
    A UserAdmin that sends a password-reset email when creating a new user,
    unless a password was entered.
    """
    add_form = UserCreationForm
    add_fieldsets = (
        (None, {
            'description': (
                "Enter the new user's name and email address and click save."
                " The user will be emailed a link allowing them to login to"
                " the site and set their password."
            ),
            'fields': ('email', 'name',),
        }),
        ('Password', {
            'description': "Optionally, you may set the user's password here.",
            'fields': ('password1', 'password2'),
            'classes': ('collapse', 'collapse-closed'),
        }),
    )

    def save_model(self, request, obj, form, change):
        if not change and not obj.has_usable_password():
            # Django's PasswordResetForm won't let us reset an unusable
            # password. We set it above super() so we don't have to save twice.
            obj.set_password(get_random_string())
            reset_password = True
        else:
            reset_password = False

        super(UserAdmin, self).save_model(request, obj, form, change)

        if reset_password:
            reset_form = PasswordResetForm({'email': obj.email})
            assert reset_form.is_valid()
            reset_form.save(
                subject_template_name='registration/account_creation_subject.txt',
                email_template_name='registration/account_creation_email.html',
                )

admin.site.unregister(User)
admin.site.register(User, UserAdmin)


class ReportAdminResource(resources.ModelResource):
    class Meta:
        model = Report
        fields = ('date_updated', 'recharged_lamps', 'sold_lamps', 'total_amount', 'pl_amount', 'group__colline__name', 'group__colline__commune__name', 'group__colline__commune__province__name')


class ReportAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = ReportAdminResource
    date_hierarchy = 'date_updated'
    list_display = ('date_updated', 'group', 'recharged_lamps', 'sold_lamps', 'total_amount', 'pl_amount',)
    search_fields = ('group__colline__name', 'group__colline__commune__name', )


class NawenuzeGroupAdminResource(resources.ModelResource):
    class Meta:
        model = NawenuzeGroup
        fields = ('colline__name', 'colline__commune__name', 'colline__commune__province__name', 'day_of_meeting', 'lamps_in_stock', 'cost_lamp', 'cost_recharge')


class NawenuzeGroupAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = NawenuzeGroupAdminResource
    list_display = ('colline', 'commune', 'day_of_meeting', 'lamps_in_stock', 'province', 'cost_lamp', 'cost_recharge')
    search_fields = ('colline__name', 'colline__commune__name',  'colline__commune__province__name')
    list_filter = ('day_of_meeting',)

    def commune(self, obj):
        return obj.colline.commune

    def province(self, obj):
        return obj.colline.commune.province


class PhoneModelAdminResource(resources.ModelResource):
    class Meta:
        model = PhoneModel
        fields = ('number',  'group__colline__name', 'group__colline__commune__name', 'group__colline__commune__province__name')


class PhoneModelAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = PhoneModelAdminResource
    list_display = ('number', 'colline', 'commune')
    search_fields = ('number', 'group__colline__name', 'group__colline__commune__name', )

    def colline(self, obj):
        return obj.group.colline

    def commune(self, obj):
        return obj.group.colline.commune


class ReceptionAdminResource(resources.ModelResource):
    class Meta:
        model = Reception
        fields = ('lamps_received',  'group__colline__name', 'date_received', 'group__colline__commune__name', 'group__colline__commune__province__name')


class ReceptionAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = ReceptionAdminResource
    list_display = ('group', 'lamps_received', 'date_received', 'colline', 'commune')
    date_hierarchy = 'date_received'
    search_fields = ('group__colline__name', 'group__colline__commune__name', )

    def colline(self, obj):
        return obj.group.colline

    def commune(self, obj):
        return obj.group.colline.commune


class OrganizationAdminResource(resources.ModelResource):
    class Meta:
        model = Organization
        fields = ('name',   'partner')


class OrganizationAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = OrganizationAdminResource
    list_display = ('name',  'partner')
    search_fields = ('name',  'partner')


class CathegoryAdminResource(resources.ModelResource):
    class Meta:
        model = Cathegory
        fields = ('name',   'code')


class CathegoryAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = CathegoryAdminResource
    list_display = ('name',  'code')
    search_fields = ('name',  'code')


class ReportServicesAdminResource(resources.ModelResource):
    class Meta:
        model = ReportServices
        fields = ('service',   'date_updated', 'beneficiary')


class ReportServicesAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = ReportServicesAdminResource
    list_display = ('service',   'date_updated', 'beneficiary')
    search_fields = ('service',)


admin.site.register(Report, ReportAdmin)
admin.site.register(NawenuzeGroup, NawenuzeGroupAdmin)
admin.site.register(PhoneModel, PhoneModelAdmin)
admin.site.register(Reception, ReceptionAdmin)
admin.site.register(Organization, OrganizationAdmin)
admin.site.register(Temporaly)
admin.site.register(Cathegory, CathegoryAdmin)
admin.site.register(ReportServices, ReportServicesAdmin)
