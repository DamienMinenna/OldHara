from django import forms

class addfolderForm(forms.Form):
    nameFolder = forms.CharField(label='Add a new folder', max_length=100)


class addDOIForm(forms.Form):
    nameDOI = forms.CharField(label='Add a doi', max_length=1000)
