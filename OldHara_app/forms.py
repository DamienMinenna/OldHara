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

class form_create_search(forms.Form):
    """
    Form for the creation of a new ref from a manual search.
    """
    entry_search = forms.CharField(label='', max_length=1000)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['entry_search'].widget.attrs['style'] = 'width:80%; display: inline;'
        self.fields['entry_search'].widget.attrs['class'] = 'form-control form-control-sm'
        self.fields['entry_search'].widget.attrs['placeholder'] = 'Manual search. Try title + authors...'

class form_filter_search(forms.Form):
    """
    Form for filter visible refs within the database.
    """
    filter_search_in_refs = forms.CharField(label='', max_length=1000)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['filter_search_in_refs'].widget.attrs['aria-label'] = 'Search in app'
        self.fields['filter_search_in_refs'].widget.attrs['aria-describedby'] = 'btnGroupAddon'
        self.fields['filter_search_in_refs'].widget.attrs['class'] = 'form-control form-control-sm'
        self.fields['filter_search_in_refs'].widget.attrs['placeholder'] = 'Search in app'


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
