from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'role', 'discipline', 'is_verified', 'created_at']
    list_filter = ['role', 'gender', 'discipline', 'is_verified', 'created_at']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    ordering = ['-created_at']
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Additional Info', {
            'fields': ('role', 'gender', 'discipline', 'institution', 'country', 'phone', 
                      'profile_picture', 'bio', 'date_of_birth', 'enrollment_year', 'is_verified')
        }),
    )
