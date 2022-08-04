from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from django.contrib.auth.models import Permission

# Register your models here.
User = get_user_model()


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'is_staff', 'is_superuser', 'groups', 'user_permissions', 'password1', 'password2',)
        }),
    )
    # fieldsets = UserAdmin.fieldsets + (
    #     ('Profile', {'fields': ('profile_pic',)}),
    # )
    model = User
    list_display = ('email', 'username', 'first_name',
                    'last_name', 'is_staff', 'is_active')
    list_filter = ['is_staff', ]
    list_editable = ['is_active', 'is_staff']
    list_per_page = 20


@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    model = Permission
    fields = ['name']
