import os
import requests
import json

from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.template.loader import render_to_string
from django.http import HttpResponse, JsonResponse

from .models import Biblio, Path_Biblio
from .forms import addfolderForm, addDOIForm

# Create your views here.

def view_home(request):
    template_name = 'index.html'

    isCreated = False
    isExist = False
    isModaladdfolder = False
    isDOICreated = False
    isDOIExist = False
    isDOInotValid = False
    isModaladdDOI = False
    if request.method == 'POST':

        if 'nameFolder' in request.POST:
            # create a form instance and populate it with data from the request:
            form_addfolder = addfolderForm(request.POST)
            form_doi = addDOIForm()
            # check whether it's valid:
            if form_addfolder.is_valid():

                nameFolder = request.POST['nameFolder']
                path = str('media/') + nameFolder

                if not os.path.exists(path):
                    os.mkdir(path)

                    b = Path_Biblio(path=nameFolder)
                    b.save()

                    isCreated = True
                else:
                    isExist = True
                isModaladdfolder = True

        elif 'nameDOI' in request.POST:
            # create a form instance and populate it with data from the request:
            form_doi = addDOIForm(request.POST)
            form_addfolder = addfolderForm()

            # check whether it's valid:
            if form_doi.is_valid():
                nameDOI = str(request.POST['nameDOI']).lower()
                folder = request.POST['folder']

                refs = Biblio.objects.all()

                for ref_i in refs:
                    refidoi = ref_i.getDOI()

                    if refidoi == nameDOI:
                        isDOIExist = True

                if not isDOIExist:
                        crossrefurl = 'https://api.crossref.org/v1/works/' + nameDOI
                        r = requests.get(crossrefurl)

                        if r.status_code == 200:
                            isDOInotValid = False
                            isDOICreated = True

                            d = json.loads(r.text)  # r.text == <class 'str'>  and d == <class 'dict'>
                            title_newentry = str(d['message']['title'][0])
                            c = Biblio(
                                title = title_newentry,
                                data = d,
                                json_payload = r.text,
                                folder = Path_Biblio.objects.get(id=folder)
                            )

                            c.save()

                            # Add id to the data
                            temp = {}
                            temp["id"] = c.id
                            temp["folder"] = c.folder.path
                            d["OldHara"] = temp

                            c.data = d
                            c.json_payload = json.dumps(d)
                            c.save()


                        else:
                            isDOInotValid = True

                            # dico_1 = {}
                            # dico_1["status"] = "ok"
                            # dico_1["DOI"] = nameDOI
                            # dico_2 = {}
                            # dico_2["message"] = dico_1
                            # c = Ref(
                            #     title = nameDOI,
                            #     data = dico_2,
                            #     json_payload = json.dumps(dico_2)
                            # )
                            # c.save()


                        isModaladdDOI = True

        else:
            form_addfolder = addfolderForm()
            form_doi = addDOIForm()


    # if a GET (or any other method) we'll create a blank form
    else:
        form_addfolder = addfolderForm()
        form_doi = addDOIForm()

    refs = Biblio.objects.order_by('-created_on')
    paths = Path_Biblio.objects.order_by('path')
    folder_list = [x for x in Path_Biblio.objects.values_list('path', flat=True).distinct()]

    return render(request, template_name,{
        'refs' : refs,
        'form_addfolder' : form_addfolder,
        'paths': paths,
        'folder_list': folder_list,
        'page': 'home',
        'isCreated': isCreated,
        'isExist': isExist,
        'isModaladdfolder': isModaladdfolder,
        'form_doi': form_doi,
        'isDOICreated': isDOICreated,
        'isDOIExist': isDOIExist,
        'isDOInotValid': isDOInotValid,
        'isModaladdDOI' : isModaladdDOI
        })



@csrf_exempt
def modify_volume(request):
    ref_id = int(request.POST['id'])
    volume = request.POST['volume']
    t = Biblio.objects.get(id=ref_id)

    dico_temp = t.data["message"]
    dico_temp["volume"] = volume
    t.data["message"] = dico_temp

    t.json_payload = json.dumps(t.data)
    t.save()

    responseData = t.data
    return JsonResponse(responseData)

@csrf_exempt
def modify_folder(request):

    ref_id = int(request.POST['id'])
    t = Biblio.objects.get(id=ref_id)

    t.data["OldHara"]["folder"] = request.POST['folder']
    t.json_payload = json.dumps(t.data)
    t.folder = Path_Biblio.objects.get(path=request.POST['folder'])
    t.save()

    responseData = t.data
    return JsonResponse(responseData)

#
#
# def view_addfolder(request):
#     template_name = 'index.html'
#     isCreated = False
#     isExist = False
#
#     # if this is a POST request we need to process the form data
#     if request.method == 'POST':
#         # create a form instance and populate it with data from the request:
#         form = addfolderForm(request.POST)
#         # check whether it's valid:
#         if form.is_valid():
#             nameFolder = request.POST['nameFolder']
#             path = str('media/') + nameFolder
#
#             if not os.path.exists(path):
#                 os.mkdir(path)
#
#                 b = Path_Ref(path=nameFolder)
#                 b.save()
#
#                 isCreated = True
#             else:
#                 isExist = True
#
#     # if a GET (or any other method) we'll create a blank form
#     else:
#         form = addfolderForm()
#
#     paths = Path_Ref.objects.order_by('path')
#
#     return render(request, template_name, {
#         'paths': paths,
#         'form': form,
#         'page': 'addfolder',
#         'isCreated': isCreated,
#         'isExist': isExist}
#         )
#
#
# def view_addentry(request):
#     template_name = 'index.html'
#
#     isDOICreated = False
#     isDOIExist = False
#
#     # if this is a POST request we need to process the form data
#     if request.method == 'POST':
#         # create a form instance and populate it with data from the request:
#         form_doi = addDOIForm(request.POST)
#         # check whether it's valid:
#         if form_doi.is_valid():
#             nameDOI = str(request.POST['nameDOI']).lower()
#
#             #
#             # if not os.path.exists(path):
#             #     os.mkdir(path)
#             #
#             #     b = Path_Ref(path=nameFolder)
#             #     b.save()
#
#             refs = Ref.objects.all()
#
#             for ref_i in refs:
#                 refidoi = ref_i.getDOI()
#                 if refidoi == nameDOI:
#                     isDOIExist = True
#
#             if not isDOIExist:
#
#                     crossrefurl = 'https://api.crossref.org/v1/works/' + nameDOI
#
#                     r = requests.get(crossrefurl)
#
#                     if r.status_code == 200:
#
#                         d = json.loads(r.text)
#
#                         title_newentry = str(d['message']['title'][0])
#                         c = Ref(
#                             title = title_newentry,
#                             data = d,
#                             json_payload = r.text
#                         )
#                         c.save()
#
#                     else:
#                         dico_1 = {}
#                         dico_1['DOI'] = nameDOI
#                         dico_2 = {}
#                         dico_2['message'] = dico_1
#                         c = Ref(title = nameDOI,data=dico_2)
#                         c.save()
#
#                     isDOICreated = True
#
#
#     # if a GET (or any other method) we'll create a blank form
#     else:
#         form_doi = addDOIForm()
#
#     paths = Path_Ref.objects.order_by('path')
#
#     return render(request, template_name, {
#         'paths': paths,
#         'form_doi': form_doi,
#         'page': 'addentry',
#         'isDOICreated': isDOICreated,
#         'isDOIExist': isDOIExist}
#         )
