import json
import ntpath
import os


from django.conf import settings
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.http import JsonResponse

from .models import Ref, Folder_Refs, TYPE_REF, MONTH_WORD
from .forms import form_create_folder, form_create_doi, form_create_search, form_update_doi, form_manual_search, form_filter_search, form_create_ME
from .crud_folder import create_folder, delete_folder
from .crud_doi import create_doi, update_doi
from .crud_entryfile import create_entry_from_dropzone
from .crud_manual_entry import create_manual_entry
from .scan_file import read_metadata, read_firstpages
from .queries import query_CrossRef

"""
OldHara_app views
"""

def view_home(request):
    """
    Main view.
    """
    template_name = 'index-home.html' # Main template

    # Initiate folders
    folders = Folder_Refs.objects.order_by('path')

    # Filter by folders
    filter_selected_folder = -1
    filter_selected_folder_name = "no folder selected"

    # Filter by search
    form_filter_search_form = form_filter_search()

    # Manage POST request from the header
    form_create_folder_form, form_create_folder_isCreated, form_create_folder_isExist, form_create_folder_isModal, form_create_doi_form, form_create_doi_isCreated, form_create_doi_isExist, form_create_doi_isnotValid, form_create_doi_isModal, form_create_search_form, form_create_search_parsed_items, form_create_search_isNotValid, form_create_search_isModal, form_create_ME_form, form_create_ME_isCreated, form_create_ME_isModal = check_header_post(request)

    # Check post
    if request.method == 'POST':

        # Create entry from files
        if 'dropzone_folder' in request.POST: 
            isfiledropzoneadded = create_entry_from_dropzone(request)

            return JsonResponse({
                'isfiledropzoneadded' : isfiledropzoneadded,
            })

        # Filter: selection by folder
        if 'filter_folder' in request.POST:
            filter_selected_folder = request.POST['filter_folder']
            if filter_selected_folder == "no folder selected":
                refs = Ref.objects.order_by('-created_on')
            else:
                # Only Ref objects filtered
                refs = Ref.objects.filter(folder = filter_selected_folder).order_by('-created_on')
                filter_selected_folder_name = Folder_Refs.objects.get(id = filter_selected_folder).path

        elif 'filter_search_in_refs' in request.POST:
            filter_search = request.POST['filter_search_in_refs']
            form_filter_search_form = form_filter_search({'filter_search_in_refs': filter_search})
            refs = Ref.objects.filter(data_text__contains=filter_search).order_by('-created_on')  

        else:
            # All Ref objects
            refs = Ref.objects.order_by('-created_on')

        # Delete folder
        if 'remove-folder' in request.POST:
            delete_folder(request)

            # Reload models
            folders = Folder_Refs.objects.order_by('path')
            refs = Ref.objects.order_by('-created_on')

    else:
        # All Ref objects
        refs = Ref.objects.order_by('-created_on')


    folder_list = [x for x in Folder_Refs.objects.values_list('path', flat=True).distinct()]

    selected_ref = refs[0]

    return render(request, template_name,
    {
    'selected_ref': selected_ref, # Selected ref
    'refs' : refs, # List of Ref objects
    'folders': folders, # List of Folder_Refs objects
    'filter_selected_folder': filter_selected_folder, # Filter selected folder id
    'filter_selected_folder_name': filter_selected_folder_name, # Filter selected folder name
    'folder_list': folder_list, # List of folder for update_folder
    'type_ref': TYPE_REF, # List of type of ref
    'month_word': MONTH_WORD, # List of month for date update
    'form_create_folder_form' : form_create_folder_form, # Form for creating a folder: Django form
    'form_create_folder_isCreated': form_create_folder_isCreated, # Form for creating a folder: Boolean if folder is created
    'form_create_folder_isExist': form_create_folder_isExist, # Form for creating a folder: Boolean if folder already exists
    'form_create_folder_isModal': form_create_folder_isModal, # Form for creating a folder: Boolean if display modal
    'form_create_doi_form' : form_create_doi_form, # Form for creating an entry from doi: Django form
    'form_create_doi_isCreated': form_create_doi_isCreated, # Form for creating an entry from doi: Boolean if entry is created
    'form_create_doi_isExist': form_create_doi_isExist, # Form for creating an entry from doi: Boolean if doi already exists in database
    'form_create_doi_isnotValid': form_create_doi_isnotValid, # Form for creating an entry from doi: Boolean if doi is not valid
    'form_create_doi_isModal': form_create_doi_isModal, # Form for creating an entry from doi: Boolean if display modal
    'form_create_search_form': form_create_search_form, # Form for creating an entry from a manual search
    'form_create_search_isModal': form_create_search_isModal, # Form for creating an entry from a manual search: Boolean if display modal
    'form_create_search_parsed_items': form_create_search_parsed_items, # Form for creating an entry from a manual search: list of item found
    'form_create_search_isNotValid': form_create_search_isNotValid, # Form for creating an entry from a manual search:  Check if the search query return a valid answer
    'form_filter_search_form': form_filter_search_form, # Filter from the search bar
    'form_create_ME_form': form_create_ME_form, # Form for creating a new entry manually
    'form_create_ME_isCreated': form_create_ME_isCreated, # Form for creating a new entry manually: Boolean if entry is created
    'form_create_ME_isModal': form_create_ME_isModal, # Form for creating a new entry manually: Boolean if display modal
    })

def view_ref(request, num=-1):
    """
    View for selected ref
    """
    template_name = 'index-selected-ref.html'

    # Initiate folders
    folders = Folder_Refs.objects.order_by('path')

    # Filter by folders (not used here)
    filter_selected_folder = -1

    # Check number selected
    if num == -1:
        selected_ref = ''
        isEntryExist = False
    else:
        try:
            selected_ref = Ref.objects.get(id = num)
            isEntryExist = True
        except Ref.DoesNotExist:
            selected_ref = ''
            isEntryExist = False

    # Initiate check doi form
    form_update_doi_form = form_update_doi()
    form_update_doi_isUpdated = False
    form_update_doi_isnotValid = False

    # Initiate scanfile
    scanfile_status = 0 # 0 = no scan file; 1 doi found; 2 doi not found
    scanfile_doi = ''

    # Initiate manual search
    form_manual_search_form = form_manual_search()
    manual_search_parsed_items = []
    manual_search_isNotValid = False

    # Manage POST request from the header
    form_create_folder_form, form_create_folder_isCreated, form_create_folder_isExist, form_create_folder_isModal, form_create_doi_form, form_create_doi_isCreated, form_create_doi_isExist, form_create_doi_isnotValid, form_create_doi_isModal, form_create_search_form, form_create_search_parsed_items, form_create_search_isNotValid, form_create_search_isModal, form_create_ME_form, form_create_ME_isCreated, form_create_ME_isModal = check_header_post(request)

    if isEntryExist == True:

        # Check post
        if request.method == 'POST':

            # Create entry from files
            if 'dropzone_folder' in request.POST: 
                isfiledropzoneadded = create_entry_from_dropzone(request)

                return JsonResponse({
                    'isfiledropzoneadded' : isfiledropzoneadded,
                })

            if 'update_doi' in request.POST: 
                form_update_doi_form, form_update_doi_isUpdated, form_update_doi_isnotValid = update_doi(request,selected_ref)

            if 'scan-file' in request.POST: 
                # Find DOI
                scanfile_doi, scanfile_status = read_metadata(selected_ref)

                if scanfile_status == 2:
                    scanfile_doi, scanfile_status = read_firstpages(selected_ref)

                if scanfile_status == 1:
                    form_update_doi_form = form_update_doi({'update_doi': scanfile_doi})


            if 'search' in request.POST: 
                search = str(request.POST['search'])
                manual_search_parsed_items, manual_search_isNotValid = query_CrossRef(search)

    folder_list = [x for x in Folder_Refs.objects.values_list('path', flat=True).distinct()]

    return render(request, template_name,
    {
        'selected_ref': selected_ref, # Selected ref
        'folders': folders, # List of Folder_Refs objects
        'form_create_folder_form' : form_create_folder_form, # Form for creating a folder: Django form
        'form_create_folder_isCreated': form_create_folder_isCreated, # Form for creating a folder: Boolean if folder is created
        'form_create_folder_isExist': form_create_folder_isExist, # Form for creating a folder: Boolean if folder already exists
        'form_create_folder_isModal': form_create_folder_isModal, # Form for creating a folder: Boolean if display modal
        'form_create_doi_form' : form_create_doi_form, # Form for creating an entry from doi: Django form
        'form_create_doi_isCreated': form_create_doi_isCreated, # Form for creating an entry from doi: Boolean if entry is created
        'form_create_doi_isExist': form_create_doi_isExist, # Form for creating an entry from doi: Boolean if doi already exists in database
        'form_create_doi_isnotValid': form_create_doi_isnotValid, # Form for creating an entry from doi: Boolean if doi is not valid
        'form_create_doi_isModal': form_create_doi_isModal, # Form for creating an entry from doi: Boolean if display modal
        'form_create_search_form': form_create_search_form, # Form for creating an entry from a manual search
        'form_create_search_isModal': form_create_search_isModal, # Form for creating an entry from a manual search: Boolean if display modal
        'form_create_search_parsed_items': form_create_search_parsed_items, # Form for creating an entry from a manual search: list of item found
        'form_create_search_isNotValid': form_create_search_isNotValid, # Form for creating an entry from a manual search:  Check if the search query return a valid answer
        'form_create_ME_form': form_create_ME_form, # Form for creating a new entry manually
        'form_create_ME_isCreated': form_create_ME_isCreated, # Form for creating a new entry manually: Boolean if entry is created
        'form_create_ME_isModal': form_create_ME_isModal, # Form for creating a new entry manually: Boolean if display modal
        'filter_selected_folder': -1, # Filter selected folder id (not used here, but needed to display remove folder button)
        'filter_selected_folder_name': "no folder selected", # Filter selected folder name (not used here, but needed to display remove folder button)
        'isEntryExist': isEntryExist, # Is entry exist or not
        'folder_list': folder_list, # List of folder for update_folder
        'type_ref': TYPE_REF, # List of type of ref
        'month_word': MONTH_WORD, # List of month for date update
        'form_update_doi_form': form_update_doi_form, # Form for updating the doi of a ref
        'form_update_doi_isUpdated': form_update_doi_isUpdated, # Form for updating the doi of a ref: Boolean if entry is updated
        'form_update_doi_isnotValid': form_update_doi_isnotValid, # Form for updating the doi of a ref: is doi not valid
        'scanfile_status': scanfile_status, # Status of the scan file
        'scanfile_doi': scanfile_doi, # doi of the scan file
        'form_manual_search_form': form_manual_search_form, # Form for a manual search of a ref
        'manual_search_parsed_items': manual_search_parsed_items, # List of item obtained from the manual search query
        'manual_search_isNotValid': manual_search_isNotValid # Check if the manual search query return a valid answer
    })


@csrf_exempt
def update_ref(request):
    """
    Request AJAX to modify the biblio
    """

    id_ref = int(request.POST['id'])
    ref = Ref.objects.get(id = id_ref)

    if 'title' in request.POST:
        ref.data["title"] = request.POST['title'].rstrip("\n")
        ref.data_text = json.dumps(ref.data)
        ref.save()

        responseData = ref.data
        return JsonResponse(responseData)

    elif 'listauthor' in request.POST:
        ref.data['listauthor'] = str(request.POST['listauthor']).rstrip("\n")
        ref.data_text = json.dumps(ref.data)
        ref.save()

        responseData = ref.data
        return JsonResponse(responseData)

    
    elif 'journal' in request.POST:
        ref.data['journal'] = str(request.POST['journal']).rstrip("\n")
        ref.data_text = json.dumps(ref.data)
        ref.save()

        responseData = ref.data
        return JsonResponse(responseData)

    elif 'volume' in request.POST:
        ref.data['volume'] = str(request.POST['volume']).rstrip("\n")
        ref.data_text = json.dumps(ref.data)
        ref.save()

        responseData = ref.data
        return JsonResponse(responseData)

    elif 'issue' in request.POST:
        ref.data["issue"] = request.POST['issue'].rstrip("\n")
        ref.data_text = json.dumps(ref.data)
        ref.save()

        responseData = ref.data
        return JsonResponse(responseData)

    elif 'page' in request.POST:
        ref.data["page"] = request.POST['page'].rstrip("\n")
        ref.data_text = json.dumps(ref.data)
        ref.save()

        responseData = ref.data
        return JsonResponse(responseData)

    elif 'articlenumber' in request.POST:
        ref.data["articlenumber"] = request.POST['articlenumber'].rstrip("\n")
        ref.data_text = json.dumps(ref.data)
        ref.save()

        responseData = ref.data
        return JsonResponse(responseData)

    elif 'dateD' in request.POST:
        ref.data["dateD"] = request.POST['dateD'].rstrip("\n")
        ref.data_text = json.dumps(ref.data)
        ref.save()

        responseData = ref.data
        return JsonResponse(responseData)

    elif 'dateMword' in request.POST:
        ref.data["dateMword"] = request.POST['dateMword']
        ref.data_text = json.dumps(ref.data)
        ref.save()

        responseData = ref.data
        return JsonResponse(responseData)
    
    elif 'dateY' in request.POST:
        ref.data["dateY"] = request.POST['dateY'].rstrip("\n")
        ref.data_text = json.dumps(ref.data)
        ref.save()

        responseData = ref.data
        return JsonResponse(responseData)

    elif 'folder' in request.POST:
        folder = request.POST['folder']
        ref.data["folder"] = folder
        ref.data_text = json.dumps(ref.data)
        ref.folder = Folder_Refs.objects.get(path=folder)

        if ref.file != '':
            # Move file to the selected folder
            initial_path = ref.file.path
            filename = ntpath.basename(ref.file.name)
            ref.file.name = Folder_Refs.objects.get(path = folder).path + '/' +  filename
            new_path = settings.MEDIA_ROOT + ref.file.name
            os.rename(initial_path, new_path)

        ref.save()

        responseData = ref.data
        return JsonResponse(responseData)

    elif 'type' in request.POST:
        ref.data["type"] = request.POST['type']
        ref.data_text = json.dumps(ref.data)
        ref.save()

        responseData = ref.data
        return JsonResponse(responseData)

    elif 'delete_ref' in request.POST:
        delete_ref = request.POST['delete_ref']
        if delete_ref == 'true':
            ref.delete()

        return JsonResponse({})


def check_header_post(request):
    """
    Check if there is a POST request from the header function.
    Used for: create an entry and add a folder.
    """

    # Initiate create folder form
    form_create_folder_isCreated = False
    form_create_folder_isExist = False
    form_create_folder_isModal = False
    form_create_folder_form = form_create_folder()

    # Initiate create doi form
    form_create_doi_form = form_create_doi()#initial = {'folder': Folder_Refs.objects.get(path='unsorted') })
    form_create_doi_isCreated = False
    form_create_doi_isExist = False
    form_create_doi_isnotValid = False
    form_create_doi_isModal = False

    # Initiate create entry from search
    form_create_search_form = form_create_search()
    form_create_search_isModal = False
    form_create_search_parsed_items = []
    form_create_search_isNotValid = False

    # Initiate create manually a new entry
    form_create_ME_form = form_create_ME()
    form_create_ME_isCreated = False
    form_create_ME_isModal = False

    # Check post
    if request.method == 'POST':

        # Create a new folder
        if 'create_folder' in request.POST:
            form_create_folder_form, form_create_folder_isCreated, form_create_folder_isExist = create_folder(request) # See crud_folder.py
            form_create_folder_isModal = True

        # Create entry from DOI
        if 'entry_DOI' in request.POST:
            form_create_doi_form, form_create_doi_isCreated, form_create_doi_isExist, form_create_doi_isnotValid = create_doi(request) # See crud_doi.py
            form_create_doi_isModal = True

        # Create entry from search
        if 'entry_search' in request.POST:
            entry_search = str(request.POST['entry_search'])
            form_create_search_form = form_create_search({'entry_search': request.POST['entry_search']})
            form_create_search_parsed_items, form_create_search_isNotValid = query_CrossRef(entry_search)
            form_create_search_isModal = True

        # Create manual entry
        if 'ME_folder' in request.POST:
            form_create_ME_form, form_create_ME_isCreated = create_manual_entry(request)
            form_create_ME_isModal = True

    return form_create_folder_form, form_create_folder_isCreated, form_create_folder_isExist, form_create_folder_isModal, form_create_doi_form, form_create_doi_isCreated, form_create_doi_isExist, form_create_doi_isnotValid, form_create_doi_isModal, form_create_search_form, form_create_search_parsed_items, form_create_search_isNotValid, form_create_search_isModal, form_create_ME_form, form_create_ME_isCreated, form_create_ME_isModal
