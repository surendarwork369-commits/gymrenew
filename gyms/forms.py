from django import forms
from .models import Gym


class GymForm(forms.ModelForm):
    """
    Form for creating and editing gym profile.
    
    Uses Django's ModelForm which automatically:
    - Creates form fields based on model fields
    - Handles validation
    - Saves to database
    """
    class Meta:
        model = Gym
        fields = ['gym_name', 'phone', 'email', 'address']
        widgets = {
            'gym_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Gym Name'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Phone Number',
                'type': 'tel'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email Address'
            }),
            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Address',
                'rows': 3
            }),
        }
