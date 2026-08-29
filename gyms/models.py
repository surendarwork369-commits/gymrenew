from django.db import models
from django.contrib.auth.models import User


class Gym(models.Model):
    """
    Gym profile model.
    
    Each user owns one gym. Use OneToOneField to enforce one-to-one relationship.
    When a user deletes their account, their gym is deleted too (CASCADE).
    """
    owner = models.OneToOneField(User, on_delete=models.CASCADE, related_name='gym')
    gym_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Gyms'

    def __str__(self):
        return f"{self.gym_name} (Owner: {self.owner.username})"

