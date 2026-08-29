from django.db import models
from django.utils import timezone

from gyms.models import Gym
from members.models import Member


class Reminder(models.Model):
    """Stores each reminder attempt for a member."""

    REMINDER_TYPES = [
        ('MEMBERSHIP_EXPIRING', 'Membership Expiring'),
        ('MEMBERSHIP_EXPIRED', 'Membership Expired'),
    ]

    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('SENT', 'Sent'),
        ('FAILED', 'Failed'),
    ]

    gym = models.ForeignKey(Gym, on_delete=models.CASCADE, related_name='reminders')
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='reminders')
    reminder_type = models.CharField(max_length=30, choices=REMINDER_TYPES)
    message = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    scheduled_at = models.DateTimeField(default=timezone.now)
    sent_at = models.DateTimeField(null=True, blank=True)
    provider_message_id = models.CharField(max_length=255, blank=True, null=True)
    error_message = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-scheduled_at']

    def __str__(self):
        return f"{self.member.name} - {self.reminder_type} - {self.status}"
