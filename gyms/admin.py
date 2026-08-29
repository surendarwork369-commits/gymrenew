from django.contrib import admin
from .models import Gym


@admin.register(Gym)
class GymAdmin(admin.ModelAdmin):
    """Admin configuration for Gym model."""
    list_display = ['gym_name', 'owner', 'phone', 'email', 'created_at']
    search_fields = ['gym_name', 'owner__username', 'phone', 'email']
    list_filter = ['created_at']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Gym Information', {
            'fields': ('gym_name', 'owner', 'phone', 'email', 'address')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

