from django import forms
from .models import Search


class SearchForms(forms.ModelForm):
    search = forms.CharField(max_length=200)
    created = forms.DateTimeField(auto_now=True)

    class Meta:
        model = Search
        fields = ( se)

