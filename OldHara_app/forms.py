from django import forms

from .models import Folder_Refs, TYPE_REF, MONTH_WORD

"""
OldHara_app forms used.
"""

class form_create_folder(forms.Form):
    """
    Form for the creation of a new folder.
    """
    create_folder = forms.CharField(label='', max_length=100)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['create_folder'].widget.attrs['style'] = 'width:80%; display: inline;'
        self.fields['create_folder'].widget.attrs['class'] = 'form-control form-control-sm'
        self.fields['create_folder'].widget.attrs['placeholder'] = 'New folder name'


class form_create_doi(forms.Form):
    """
    Form for the creation of a new ref from a DOI.
    """
    entry_DOI = forms.CharField(label='DOI', max_length=1000)
    entry_folder = forms.ModelChoiceField(label='Folder', queryset=Folder_Refs.objects.all(), required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['entry_DOI'].widget.attrs['style'] = 'width:80%; display: inline;'
        self.fields['entry_DOI'].widget.attrs['class'] = 'form-control form-control-sm'
        self.fields['entry_DOI'].widget.attrs['placeholder'] = 'doi'

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
    update_doi = forms.CharField(label='', max_length=1000)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['update_doi'].widget.attrs['style'] = 'width:80%; height:40px; display: inline;'
        self.fields['update_doi'].widget.attrs['class'] = 'form-control form-control-sm'
        self.fields['update_doi'].widget.attrs['placeholder'] = 'Add or update doi'

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


class form_create_ME(forms.Form):
    """
    Form for the creation of a new ref (ME: Manual Entry)
    """
    
    ME_folder = forms.ModelChoiceField(label='*Folder', queryset=Folder_Refs.objects.all(), required=True)
    ME_title = forms.CharField(label='*Title', required=True)
    ME_type = forms.ChoiceField(label='*Type', choices=TYPE_REF, required=True)
    ME_listauthor = forms.CharField(label='Authors', required=False)

    ME_journal = forms.CharField(label='Journal', required=False)
    ME_volume = forms.CharField(label='Volume', max_length=1000, required=False)
    ME_issue = forms.CharField(label='Issue', max_length=1000, required=False)

    ME_dateD = forms.CharField(label='Day', max_length=1000, required=False)
    ME_dateMword = forms.ChoiceField(label='Month', choices=MONTH_WORD)
    ME_dateY = forms.CharField(label='Year', max_length=1000, required=False)

    ME_page = forms.CharField(label='Page', max_length=1000, required=False)
    ME_articlenumber = forms.CharField(label='Article number', max_length=1000, required=False)

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     for visible in self.visible_fields():
    #         visible.field.widget.attrs['style'] = 'display: grid; grid-template-columns: 1fr 3fr;'

