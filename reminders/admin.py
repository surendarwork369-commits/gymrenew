from django.contrib import admin

from .models import Reminder


@admin.register(Reminder)
class ReminderAdmin(admin.ModelAdmin):
    list_display = ('member', 'gym', 'reminder_type', 'status', 'scheduled_at', 'sent_at')
    search_fields = ('member__name', 'member__phone', 'message')
    list_filter = ('status', 'reminder_type', 'gym')
