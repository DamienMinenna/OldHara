from django import forms
from .models import Path_Biblio

class addfolderForm(forms.Form):
    nameFolder = forms.CharField(label='Name of the new folder ', max_length=100)


class addDOIForm(forms.Form):
    nameDOI = forms.CharField(label='DOI ', max_length=1000)
    folder = forms.ModelChoiceField(queryset=Path_Biblio.objects.all(), required=True, help_text="Choose folder ")
