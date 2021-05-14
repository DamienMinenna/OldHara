import os
import requests
import json

from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.template.loader import render_to_string
from django.http import HttpResponse, JsonResponse

from .models import Biblio, Ref, Path_Ref
from .forms import addfolderForm, addDOIForm

# Create your views here.

def view_home(request):
    template_name = 'index.html'
    id_selected = 0

    refs = Ref.objects.order_by('-created_on')
    ref_selected = Ref.objects.all()[id_selected]
    paths = Path_Ref.objects.order_by('path')

    dic_selected = {}
    dic_selected['Title'] = ref_selected.getTitle()
    dic_selected['Authors'] = ref_selected.getAuthors()

    return render(request, template_name,{
        'refs' : refs,
        'dic_selected' : dic_selected,
        'ref_selected' : ref_selected,
        'paths': paths,
        'page': 'home',
        })

def select_list(request):
    template_name = 'index.html'
    dic_selected = {}
    if request.is_ajax() and request.method == 'GET':
        if 'id' in request.GET:
            ref_wanted = str(request.GET['id'])[:-1]
            # for i in Ref.objects.all():
            for i in range(Ref.objects.all().count()):
                if str(Ref.objects.all()[i]) == ref_wanted:
                    id_selected = i
                    print('I have it!!')

                    ref_selected = Ref.objects.all()[id_selected]

                    dic_selected['Title'] = ref_selected.getTitle()
                    dic_selected['Authors'] = ref_selected.getAuthors()

    # return JsonResponse(response, status=200)
    # html = render_to_string(template_name, dic_selected)
    # return HttpResponse(html)

    return JsonResponse(dic_selected)

def view_addfolder(request):
    template_name = 'index.html'
    isCreated = False
    isExist = False

    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = addfolderForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            nameFolder = request.POST['nameFolder']
            path = str('media/') + nameFolder

            if not os.path.exists(path):
                os.mkdir(path)

                b = Path_Ref(path=nameFolder)
                b.save()

                isCreated = True
            else:
                isExist = True

    # if a GET (or any other method) we'll create a blank form
    else:
        form = addfolderForm()


    paths = Path_Ref.objects.order_by('path')

    return render(request, template_name, {
        'paths': paths,
        'form': form,
        'page': 'addfolder',
        'isCreated': isCreated,
        'isExist': isExist}
        )


def view_addentry(request):
    template_name = 'index.html'

    isDOICreated = False
    isDOIExist = False

    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form_doi = addDOIForm(request.POST)
        # check whether it's valid:
        if form_doi.is_valid():
            nameDOI = str(request.POST['nameDOI']).lower()

            #
            # if not os.path.exists(path):
            #     os.mkdir(path)
            #
            #     b = Path_Ref(path=nameFolder)
            #     b.save()

            refs = Ref.objects.all()

            for ref_i in refs:
                refidoi = ref_i.getDOI()
                if refidoi == nameDOI:
                    isDOIExist = True

            if not isDOIExist:

                    crossrefurl = 'https://api.crossref.org/v1/works/' + nameDOI
                    print(crossrefurl)
                    r = requests.get(crossrefurl)

                    if r.status_code == 200:

                        d = json.loads(r.text)

                        title_newentry = str(d['message']['title'][0])
                        c = Ref(title = title_newentry,data=d)
                        c.save()

                    else:
                        dico_1 = {}
                        dico_1['DOI'] = nameDOI
                        dico_2 = {}
                        dico_2['message'] = dico_1
                        c = Ref(title = nameDOI,data=dico_2)
                        c.save()

                    isDOICreated = True


    # if a GET (or any other method) we'll create a blank form
    else:
        form_doi = addDOIForm()

    paths = Path_Ref.objects.order_by('path')

    return render(request, template_name, {
        'paths': paths,
        'form_doi': form_doi,
        'page': 'addentry',
        'isDOICreated': isDOICreated,
        'isDOIExist': isDOIExist}
        )
