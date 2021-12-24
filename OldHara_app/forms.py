from django import forms

from .models import Folder_Refs

"""
OldHara_app forms used.
"""

class form_create_folder(forms.Form):
    """
    Form for the creation of a new folder.
    """
    nameFolder = forms.CharField(label='', max_length=100)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nameFolder'].widget.attrs['style'] = 'width:80%; display: inline;'
        self.fields['nameFolder'].widget.attrs['class'] = 'form-control form-control-sm'
        self.fields['nameFolder'].widget.attrs['placeholder'] = 'New folder name'


class form_create_doi(forms.Form):
    """
    Form for the creation of a new ref from a DOI.
    """
    nameDOI = forms.CharField(label='', max_length=1000)
    folder = forms.ModelChoiceField(queryset=Folder_Refs.objects.all(), required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nameDOI'].widget.attrs['style'] = 'width:80%; display: inline;'
        self.fields['nameDOI'].widget.attrs['class'] = 'form-control form-control-sm'
        self.fields['nameDOI'].widget.attrs['placeholder'] = 'doi'

class form_update_doi(forms.Form):
    """
    Form for updating a DOI.
    """
    doi = forms.CharField(label='', max_length=1000)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['doi'].widget.attrs['style'] = 'width:80%; height:40px; display: inline;'
        self.fields['doi'].widget.attrs['class'] = 'form-control form-control-sm'
        self.fields['doi'].widget.attrs['placeholder'] = 'Add or update doi'

class form_manual_search(forms.Form):
    """
    Form for manual search of a DOI.
    """
    search = forms.CharField(label='', max_length=1000)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['search'].widget.attrs['style'] = 'width:80%; height:40px; display: inline;'
        self.fields['search'].widget.attrs['class'] = 'form-control form-control-sm'
        self.fields['search'].widget.attrs['placeholder'] = 'Manual search. Try title + authors...'
