from datetime import timedelta

from django.db import models
from django.utils import timezone
from gyms.models import Gym


class Member(models.Model):
    """
    Member model.

    Each member belongs to a gym (ForeignKey).
    membership_amount uses DecimalField for precise money handling.
    Status values are calculated from dates instead of being stored separately.
    """
    gym = models.ForeignKey(Gym, on_delete=models.CASCADE, related_name='members')
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True, null=True)
    membership_start_date = models.DateField()
    membership_end_date = models.DateField()
    membership_amount = models.DecimalField(max_digits=10, decimal_places=2)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    @property
    def membership_status(self):
        """Return ACTIVE, EXPIRING_SOON, or EXPIRED based on membership end date."""
        today = timezone.now().date()

        if self.membership_end_date < today:
            return 'EXPIRED'
        if self.membership_end_date <= today + timedelta(days=7):
            return 'EXPIRING_SOON'
        return 'ACTIVE'

    @property
    def days_until_expiry(self):
        """Number of days remaining until membership expires."""
        today = timezone.now().date()
        return (self.membership_end_date - today).days

    def __str__(self):
        return f"{self.name} ({self.gym.gym_name})"

