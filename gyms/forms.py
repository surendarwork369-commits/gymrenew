from django import forms
from .models import Gym
from django.core.exceptions import ValidationError



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
    def clean_gym_name(self):
       gym_name = self.cleaned_data.get('gym_name')

       if gym_name and not gym_name.replace(' ', '').isalpha():
           raise ValidationError('Name should contain only letters.')

       return gym_name
    def clean_phone(self):
       phone = self.cleaned_data.get('phone')
       if phone and not phone.isdigit():
           raise ValidationError('Phone number should be digit')
       if len(phone) < 10:
           raise ValidationError('phone number must contains 10 digits')
       if not phone.startswith(('6' , '7' , '8' , '9')):
           raise ValidationError('invalid! number')
       return phone