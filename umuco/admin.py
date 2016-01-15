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
        model =Report
        fields = ('date_updated', 'recharged_lamps', 'sold_lamps', 'amount', 'group__colline', 'group__commune')

class ReportAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = ReportAdminResource
    date_hierarchy = 'date_updated'
    list_display = ('date_updated', 'group','recharged_lamps', 'sold_lamps', 'amount')
    search_fields = ('group__colline', 'group__commune', )

class NawenuzeGroupAdmin(admin.ModelAdmin):
    list_display = ('colline', 'commune', 'day_of_meeting', 'province')
    search_fields = ('colline', 'commune',  'province')
    list_filter = ( 'day_of_meeting',)

class PhoneModelAdminResource(resources.ModelResource):
    class Meta:
        model =PhoneModel
        fields = ('number',  'group__colline', 'group__commune')

class PhoneModelAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = PhoneModelAdminResource
    list_display = ('number', 'colline','commune')
    search_fields = ('number', 'group__colline', 'group__commune', )

    def colline(self, obj):
        return obj.group.colline

    def commune(self, obj):
        return obj.group.commune

class ReceptionAdminResource(resources.ModelResource):
    class Meta:
        model =Reception
        fields = ('lamps_received',  'group__colline', 'group__commune', 'date_received')

class ReceptionAdmin(ExportMixin, admin.ModelAdmin):
    resource_class =ReceptionAdminResource
    list_display = ('group', 'date_received', 'colline','commune')
    search_fields = ( 'group__colline', 'group__commune', )

    def colline(self, obj):
        return obj.group.colline

    def commune(self, obj):
        return obj.group.commune

admin.site.register(Report, ReportAdmin)
admin.site.register(NawenuzeGroup, NawenuzeGroupAdmin)
admin.site.register(PhoneModel, PhoneModelAdmin)
admin.site.register(Reception, ReceptionAdmin)