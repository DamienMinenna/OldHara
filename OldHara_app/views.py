import os
import sys
import json
import PyPDF2
from PIL import Image
import pytesseract
from pdf2image import convert_from_path

from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.template.loader import render_to_string
from django.http import HttpResponse, JsonResponse
from django.conf import settings

from .models import Biblio, Path_Biblio
from .forms import addfolderForm, addDOIForm

from .add_folder import add_folder
from .add_entry import add_doi, add_file_from_dropzone, check_doi
from .read_file_for_db import read_metadata, read_firstpages

# Create your views here.

def view_home(request):
    """
    Main view.
    """
    template_name = 'index.html'

    isCreated = False
    isExist = False
    isModaladdfolder = False
    if request.method == 'POST':

        # Add folder
        if 'nameFolder' in request.POST:
            form_addfolder, isCreated, isExist, isModaladdfolder = add_folder(request) # See add_folder.py

        else:
            form_addfolder = addfolderForm()


    # if a GET (or any other method) we'll create a blank form
    else:
        form_addfolder = addfolderForm()

    refs = Biblio.objects.order_by('-created_on')
    paths = Path_Biblio.objects.order_by('path')
    folder_list = [x for x in Path_Biblio.objects.values_list('path', flat=True).distinct()]

    countFileStore = Biblio.objects.filter(status = 1).count()

    return render(request, template_name,{
        'refs' : refs,
        'form_addfolder' : form_addfolder,
        'paths': paths,
        'folder_list': folder_list,
        'countFileStore' : countFileStore,
        'isCreated': isCreated,
        'isExist': isExist,
        'isModaladdfolder': isModaladdfolder,
        })

def view_add_biblio(request):
    """
    View for adding file
    """
    template_name = 'add_biblio.html'

    isCreated = False
    isExist = False
    isModaladdfolder = False
    isDOICreated = False
    isDOIExist = False
    isDOInotValid = False
    if request.method == 'POST':

        if 'dropzone_folder' in request.POST: 

            fileAdded = add_file_from_dropzone(request)

            return JsonResponse({
                'fileAdded' : fileAdded,
                'countFileStore' : int(Biblio.objects.filter(status = 1).count())
            })

        # Add folder
        if 'nameFolder' in request.POST:
            form_doi = addDOIForm()
            form_addfolder, isCreated, isExist, isModaladdfolder = add_folder(request) # See add_folder.py

        # Add DOI
        elif 'nameDOI' in request.POST:
            form_addfolder = addfolderForm()
            form_doi, isDOIExist, isDOInotValid, isDOICreated = add_doi(request) # See add_entry.py

        # POST but without registered keys
        else:
            form_addfolder = addfolderForm()
            form_doi = addDOIForm()

    # Create blank forms
    else:
        form_addfolder = addfolderForm()
        form_doi = addDOIForm()

    refs = Biblio.objects.order_by('-created_on')
    paths = Path_Biblio.objects.order_by('path')
    folder_list = [x for x in Path_Biblio.objects.values_list('path', flat=True).distinct()]

    countFileStore = Biblio.objects.filter(status = 1).count()

    return render(request, template_name,{
        'refs' : refs,
        'form_addfolder' : form_addfolder,
        'paths': paths,
        'folder_list': folder_list,
        'countFileStore' : countFileStore,
        'isCreated': isCreated,
        'isExist': isExist,
        'isModaladdfolder': isModaladdfolder,
        'form_doi': form_doi,
        'isDOICreated': isDOICreated,
        'isDOIExist': isDOIExist,
        'isDOInotValid': isDOInotValid,
        })


def view_check_biblio(request, num=-1):
    """
    View for check the files
    """
    template_name = 'check_biblio.html'

    isCreated = False
    isExist = False
    isModaladdfolder = False
    if request.method == 'POST':

        # Add folder
        if 'nameFolder' in request.POST:
            form_addfolder, isCreated, isExist, isModaladdfolder = add_folder(request) # See add_folder.py

        else:
            form_addfolder = addfolderForm()

        if 'del_toSort' in request.POST:
            id_toDel = request.POST['del_toSort']
            t = Biblio.objects.get(id = id_toDel)
            t.delete()


    # Create blank forms
    else:
        form_addfolder = addfolderForm()


    refs = Biblio.objects.order_by('-created_on')
    paths = Path_Biblio.objects.order_by('path')
    folder_list = [x for x in Path_Biblio.objects.values_list('path', flat=True).distinct()]

    countFileStore = Biblio.objects.filter(status = 1).count()
    file_to_sort = Biblio.objects.filter(status = 1).order_by('-created_on')


    if num == -1:
        file_selected = ''
        doi = ''
    else:
        file_selected = Biblio.objects.get(id = num)
        doi = read_metadata(file_selected)

        if doi == '':
            doi = read_firstpages(file_selected)


        if doi != '':
            doi = check_doi(doi)

    return render(request, template_name,{
        'refs' : refs,
        'form_addfolder' : form_addfolder,
        'paths': paths,
        'folder_list': folder_list,
        'countFileStore' : countFileStore,
        'file_to_sort' : file_to_sort,
        'file_selected' : file_selected,
        'isCreated': isCreated,
        'isExist': isExist,
        'isModaladdfolder': isModaladdfolder,
        'pdf_info': doi,
        })

@csrf_exempt
def modify_biblio(request):
    """
    Request AJAX to modify the biblio
    """

    ref_id = int(request.POST['id'])
    t = Biblio.objects.get(id = ref_id)

    if 'title' in request.POST:
        t.db["title"] = request.POST['title'].rstrip("\n")
        t.db_text = json.dumps(t.db)
        t.save()

        responseData = t.db
        return JsonResponse(responseData)

    elif 'volume' in request.POST:
        t.db['volume'] = str(request.POST['volume']).rstrip("\n")
        t.db_text = json.dumps(t.db)
        t.save()

        responseData = t.db
        return JsonResponse(responseData)

    elif 'issue' in request.POST:
        t.db["issue"] = request.POST['issue'].rstrip("\n")
        t.db_text = json.dumps(t.db)
        t.save()

        responseData = t.db
        return JsonResponse(responseData)

    elif 'page' in request.POST:
        t.db["page"] = request.POST['page'].rstrip("\n")
        t.db_text = json.dumps(t.db)
        t.save()

        responseData = t.db
        return JsonResponse(responseData)

    elif 'ArtNumb' in request.POST:
        t.db["articlenumber"] = request.POST['ArtNumb'].rstrip("\n")
        t.db_text = json.dumps(t.db)
        t.save()

        responseData = t.db
        return JsonResponse(responseData)

    elif 'folder' in request.POST:
        t.db["folder"] = request.POST['folder']
        t.db_text = json.dumps(t.db)
        t.folder = Path_Biblio.objects.get(path=request.POST['folder'])
        t.save()

        responseData = t.db
        return JsonResponse(responseData)

    elif 'edDelete' in request.POST:
        edDelete = request.POST['edDelete']
        if edDelete == 'true':
            t.delete()

        return JsonResponse({})
