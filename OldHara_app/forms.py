from django import forms

from .models import Folder_Refs

"""
OldHara_app forms used.
"""

class form_create_folder(forms.Form):
    """
    Form for the creation of a new folder.
    """
    nameFolder = forms.CharField(label='New folder name ', max_length=100)


class form_create_doi(forms.Form):
    """
    Form for the creation of a new ref from a DOI.
    """
    nameDOI = forms.CharField(label='DOI ', max_length=1000)
    folder = forms.ModelChoiceField(queryset=Folder_Refs.objects.all(), required=True, help_text="Choose folder ")

class form_update_doi(forms.Form):
    """
    Form for updating a DOI.
    """
    doi = forms.CharField(label='Update doi ', max_length=1000)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['doi'].widget.attrs['style'] = 'width:80%; height:40px;'

class form_manual_search(forms.Form):
    """
    Form for manual search of a DOI.
    """
    search = forms.CharField(label='Manual search ', max_length=1000)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['search'].widget.attrs['style'] = 'width:80%; height:40px;'
