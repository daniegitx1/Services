from django import forms
from .models import Listing

class ListingForm(forms.ModelForm):
    duration = forms.IntegerField(
        min_value=1,
        label="Duration (Months)",
        widget=forms.NumberInput(attrs={'id': 'duration', 'onchange': 'calculateEndDate()'})
    )

    class Meta:
        model = Listing
        fields = ['type', 'category', 'post_title', 'summary', 'description', 'client_name',
                  'phone_number', 'email', 'website', 'picture', 'duration']

        widgets = {
            'start_date': forms.HiddenInput(),
            'end_date': forms.HiddenInput(),
        }
