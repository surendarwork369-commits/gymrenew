from django.contrib import admin
from .models import Member


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    """Admin configuration for Member model."""
    list_display = ['name', 'gym', 'phone', 'membership_end_date', 'membership_amount', 'created_at']
    search_fields = ['name', 'phone', 'email', 'gym__gym_name']
    list_filter = ['gym', 'created_at', 'membership_end_date']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Member Information', {
            'fields': ('gym', 'name', 'phone', 'email', 'notes')
        }),
        ('Membership Details', {
            'fields': ('membership_start_date', 'membership_end_date', 'membership_amount')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

