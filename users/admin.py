from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

# Register your models here.
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'role', 'is_active']
    list_filter = ['role', 'is_active', 'date_joined' ]
    search_fields = ['username', 'email', 'first_name', 'last_name']
    readonly_fields = ['date_joined']
    
    fieldsets = UserAdmin.fieldsets + (

        ('Additional Info', {'fields': ('role', 'phone')}),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Info', {'fields': ('role','email' , 'phone')}),
    )