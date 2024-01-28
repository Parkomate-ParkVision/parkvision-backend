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
        'privilege'
    )
    list_filter = (
        'privilege',
        'is_active',
        'is_staff',
        'is_superuser',
    )
    search_fields = ('name', 'email')
    ordering = ('email',)

    fieldsets = (
        (None, {'fields': ('email', 'name', 'password')}),
        ('Privilege Info', {'fields': ('privilege',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'password1', 'password2', 'privilege'),
        }),
    )

admin.site.register(ParkomateUser, ParkomateUserAdmin)