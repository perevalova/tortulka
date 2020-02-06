from django import forms
from django.core.validators import RegexValidator


class ContactForm(forms.Form):
    first_name = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-input'}))
    last_name = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-input'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-input'}))
    phone_number = forms.CharField(min_length=13, validators=[RegexValidator(r'^(\+380)?\d{9}$', message="Формат номеру: +380123456789")], required=False, widget=forms.TextInput(attrs={'class': 'form-input'}))
    message = forms.CharField(max_length=2560, widget=forms.Textarea(attrs={'class': 'form-input textarea-lg'}))
