from django import forms
from .models import Path_Biblio

class addfolderForm(forms.Form):
    nameFolder = forms.CharField(label='New folder name', max_length=100)


class addDOIForm(forms.Form):
    nameDOI = forms.CharField(label='Add a doi', max_length=1000)
    folder = forms.ModelChoiceField(queryset=Path_Biblio.objects.all(), required=True, help_text="Folder")
