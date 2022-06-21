from django import forms
from main.models import PhotoGraphy


class PhotoCreationForm(forms.ModelForm):
    class Meta:
        model = PhotoGraphy
        exclude = ['created', 'updated', 'user']
