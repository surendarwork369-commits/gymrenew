from django import forms
from django.core.exceptions import ValidationError
from .models import Member


class MemberForm(forms.ModelForm):
    """
    Form for creating and editing members.
    
    Custom validation ensures:
    - End date is not before start date
    - Amount is not negative
    """
    class Meta:
        model = Member
        fields = ['name', 'phone', 'email', 'membership_start_date', 
                  'membership_end_date', 'membership_amount', 'notes']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Member Name'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Phone Number',
                'type': 'tel'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email (optional)',
                'required': False
            }),
            'membership_start_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'membership_end_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'membership_amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Amount (e.g., 500.00)',
                'step': '0.01'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Additional notes (optional)',
                'rows': 3
            }),
        }

    def clean(self):
        """Validate that end date is not before start date and amount is not negative."""
        cleaned_data = super().clean()
        start_date = cleaned_data.get('membership_start_date')
        end_date = cleaned_data.get('membership_end_date')
        amount = cleaned_data.get('membership_amount')

        if start_date and end_date:
            if end_date < start_date:
                raise ValidationError(
                    'Membership end date cannot be before start date.'
                )

        if amount is not None:
            if amount < 0:
                raise ValidationError(
                    'Membership amount cannot be negative.'
                )

        return cleaned_data
