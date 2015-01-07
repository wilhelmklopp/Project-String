from django import forms
from pstring.models import Links

class LinksForm(forms.Form):
    long_url = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'URL', 'autofocus': 'True'}), max_length=10000, label="1", required=True)
