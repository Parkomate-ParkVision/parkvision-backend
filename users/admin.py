from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models import ParkomateUser

admin.site.site_header = 'ParkVision Admin'

class ParkomateUserAdmin(UserAdmin):
    model = ParkomateUser
    list_display = (
        'name',
        'email',
        'phone',
        'organization',
        'privilege'
    )
    list_filter = (
        'organization',
        'privilege',
        'is_active',
        'is_staff',
        'is_superuser',
    )
    search_fields = ('name', 'email')
    ordering = ('email',)

    fieldsets = (
        (None, {'fields': ('email', 'name', 'password')}),
        ('Organization Info', {'fields': ('organization',)}),
        ('Privilege Info', {'fields': ('privilege',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'password1', 'password2', 'organization', 'privilege'),
        }),
    )

admin.site.register(ParkomateUser, ParkomateUserAdmin)