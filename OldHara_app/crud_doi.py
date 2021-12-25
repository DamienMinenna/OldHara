import json
import requests

from .models import Ref, Folder_Refs
from .forms import form_create_doi, form_update_doi

def create_entry_from_crossref_doi(crossrefrequest, folder, entry_DOI):
    data_crossref = json.loads(crossrefrequest.text)  # .text == <class 'str'>  and d == <class 'dict'>
    title_newentry = str(data_crossref['message']['title'][0])

    ref = Ref(
        title = title_newentry,
        folder = Folder_Refs.objects.get(id = folder),
        status = 0,
        doi = entry_DOI,
    )
    ref.save()

    # Add db 
    temp = {}
    temp["id"] = ref.id
    temp["folder"] = ref.folder.path

    temp["status"] = 0

    if 'message' in data_crossref:
        temp["title"] = ''
        if 'title' in data_crossref['message']:
            temp["title"] = str(data_crossref['message']['title'][0])

        # Get date
        temp["dateY"] = ''
        temp["dateM"] = ''
        temp["dateMword"] = ''
        temp["dateD"] = ''
        if 'issued' in data_crossref['message']:
            if 'date-parts' in data_crossref['message']['issued']:
                if len(data_crossref['message']['issued']['date-parts'][0]) >= 1:
                    temp["dateY"] = str(data_crossref['message']['issued']['date-parts'][0][0])

                if len(data_crossref['message']['issued']['date-parts'][0]) >= 2:
                    temp["dateM"] = str(data_crossref['message']['issued']['date-parts'][0][1])
                    if data_crossref['message']['issued']['date-parts'][0][1] == 1:
                        temp["dateMword"] = 'January'
                    elif data_crossref['message']['issued']['date-parts'][0][1] == 2:
                        temp["dateMword"] = 'February'
                    elif data_crossref['message']['issued']['date-parts'][0][1] == 3:
                        temp["dateMword"] = 'March'
                    elif data_crossref['message']['issued']['date-parts'][0][1] == 4:
                        temp["dateMword"] = 'April'
                    elif data_crossref['message']['issued']['date-parts'][0][1] == 5:
                        temp["dateMword"] = 'May'
                    elif data_crossref['message']['issued']['date-parts'][0][1] == 6:
                        temp["dateMword"] = 'June'
                    elif data_crossref['message']['issued']['date-parts'][0][1] == 7:
                        temp["dateMword"] = 'July'
                    elif data_crossref['message']['issued']['date-parts'][0][1] == 8:
                        temp["dateMword"] = 'August'
                    elif data_crossref['message']['issued']['date-parts'][0][1] == 9:
                        temp["dateMword"] = 'September'
                    elif data_crossref['message']['issued']['date-parts'][0][1] == 10:
                        temp["dateMword"] = 'October'
                    elif data_crossref['message']['issued']['date-parts'][0][1] == 11:
                        temp["dateMword"] = 'November'
                    elif data_crossref['message']['issued']['date-parts'][0][1] == 12:
                        temp["dateMword"] = 'December'

                if len(data_crossref['message']['issued']['date-parts'][0]) == 3:  
                    temp["dateD"] = str(data_crossref['message']['issued']['date-parts'][0][2])
       
        temp["issue"] = ''
        if 'issue' in data_crossref['message']:
            temp["issue"] = str(data_crossref['message']['issue'])

        temp["DOI"] = ''
        if 'DOI' in data_crossref['message']: 
            temp["DOI"] = str(data_crossref['message']['DOI'].lower())
        temp["isDOIvalid"] = 'true'

        temp["type"] = 'other'
        if 'type' in data_crossref['message']: 
            temp["type"] = str(data_crossref['message']['type'])

        temp["journal"] = ''
        if 'container-title' in data_crossref['message']: 
            temp["journal"] = str(data_crossref['message']['container-title'][0])
        
        temp["volume"] = ''
        if 'volume' in data_crossref['message']: 
            temp["volume"] = str(data_crossref['message']['volume'])

        temp["page"] = ''
        if 'page' in data_crossref['message']: 
            temp["page"] = str(data_crossref['message']['page'])

        temp["articlenumber"] = ''
        if 'articlenumber' in data_crossref['message']: 
            temp["article-number"] = str(data_crossref['message']['article-number'])

        # Get authors
        temp["numberauthor"] = 0
        temp["listauthor"] = ''
        temp["author"] = {}
        temp_list = {}
        if 'author' in data_crossref['message']: 
            for author_i in data_crossref['message']['author']:
                temp["listauthor"] = temp["listauthor"] + str(author_i['given']) + ' ' + str(author_i['family']) + ', '
                temp["numberauthor"] = temp["numberauthor"] + 1

                temp_author = {}
                temp_author['given'] = author_i['given']
                temp_author['family'] = author_i['family']
     
                temp_list[str(int(temp["numberauthor"]))] = temp_author
                
            if temp["numberauthor"] > 0:
                temp["listauthor"] = temp["listauthor"][:-2]

            temp["author"] = temp_list

    ref.data = temp # Main OldHara data
    ref.data_text = json.dumps(temp) # Text version
    ref.save()

def create_doi(request):
    """
    Create entry from its doi.
    """
    form_create_doi_isExist = False
    form_create_doi_isnotValid = False
    form_create_doi_isCreated = False
    
    # create a form instance and populate it with data from the request:
    form_create_doi_form = form_create_doi(request.POST)
    
    # check whether it's valid:
    if form_create_doi_form.is_valid():
        entry_DOI = str(request.POST['entry_DOI']).lower()
        folder = request.POST['folder']
        refs = Ref.objects.all()

        # check if DOI exist
        for ref_i in refs:
            refidoi = ref_i.doi

            if refidoi == entry_DOI:
                form_create_doi_isExist = True

        if not form_create_doi_isExist:
                crossrefurl = 'https://api.crossref.org/v1/works/' + entry_DOI
                crossrefrequest = requests.get(crossrefurl)

                if crossrefrequest.status_code == 200:
                    form_create_doi_isnotValid = False
                    form_create_doi_isCreated = True

                    create_entry_from_crossref_doi(crossrefrequest, folder, entry_DOI)
                    
                else:
                    form_create_doi_isnotValid = True

    return form_create_doi_form, form_create_doi_isCreated, form_create_doi_isExist, form_create_doi_isnotValid 


def update_entry_from_crossref_doi(crossrefrequest, doi, selected_ref):
    """
    Update a ref from a given doi
    """
    data_crossref = json.loads(crossrefrequest.text)  # .text == <class 'str'>  and d == <class 'dict'>

    selected_ref.title = str(data_crossref['message']['title'][0])
    selected_ref.doi = doi

    # Add db 
    temp = {}
    temp["id"] = selected_ref.id
    temp["folder"] = selected_ref.folder.path

    temp["status"] = 0

    if 'message' in data_crossref:
        temp["title"] = ''
        if 'title' in data_crossref['message']:
            temp["title"] = str(data_crossref['message']['title'][0])

        # Get date
        temp["dateY"] = ''
        temp["dateM"] = ''
        temp["dateMword"] = ''
        temp["dateD"] = ''
        if 'issued' in data_crossref['message']:
            if 'date-parts' in data_crossref['message']['issued']:
                if len(data_crossref['message']['issued']['date-parts'][0]) >= 1:
                    temp["dateY"] = str(data_crossref['message']['issued']['date-parts'][0][0])

                if len(data_crossref['message']['issued']['date-parts'][0]) >= 2:
                    temp["dateM"] = str(data_crossref['message']['issued']['date-parts'][0][1])
                    if data_crossref['message']['issued']['date-parts'][0][1] == 1:
                        temp["dateMword"] = 'January'
                    elif data_crossref['message']['issued']['date-parts'][0][1] == 2:
                        temp["dateMword"] = 'February'
                    elif data_crossref['message']['issued']['date-parts'][0][1] == 3:
                        temp["dateMword"] = 'March'
                    elif data_crossref['message']['issued']['date-parts'][0][1] == 4:
                        temp["dateMword"] = 'April'
                    elif data_crossref['message']['issued']['date-parts'][0][1] == 5:
                        temp["dateMword"] = 'May'
                    elif data_crossref['message']['issued']['date-parts'][0][1] == 6:
                        temp["dateMword"] = 'June'
                    elif data_crossref['message']['issued']['date-parts'][0][1] == 7:
                        temp["dateMword"] = 'July'
                    elif data_crossref['message']['issued']['date-parts'][0][1] == 8:
                        temp["dateMword"] = 'August'
                    elif data_crossref['message']['issued']['date-parts'][0][1] == 9:
                        temp["dateMword"] = 'September'
                    elif data_crossref['message']['issued']['date-parts'][0][1] == 10:
                        temp["dateMword"] = 'October'
                    elif data_crossref['message']['issued']['date-parts'][0][1] == 11:
                        temp["dateMword"] = 'November'
                    elif data_crossref['message']['issued']['date-parts'][0][1] == 12:
                        temp["dateMword"] = 'December'

                if len(data_crossref['message']['issued']['date-parts'][0]) == 3:  
                    temp["dateD"] = str(data_crossref['message']['issued']['date-parts'][0][2])
       
        temp["issue"] = ''
        if 'issue' in data_crossref['message']:
            temp["issue"] = str(data_crossref['message']['issue'])

        temp["DOI"] = ''
        if 'DOI' in data_crossref['message']: 
            temp["DOI"] = str(data_crossref['message']['DOI'].lower())
        temp["isDOIvalid"] = 'true'

        temp["type"] = 'other'
        if 'type' in data_crossref['message']: 
            temp["type"] = str(data_crossref['message']['type'])

        temp["journal"] = ''
        if 'container-title' in data_crossref['message']: 
            if data_crossref['message']['container-title']:
                temp["journal"] = str(data_crossref['message']['container-title'][0])

        
        temp["volume"] = ''
        if 'volume' in data_crossref['message']: 
            temp["volume"] = str(data_crossref['message']['volume'])

        temp["page"] = ''
        if 'page' in data_crossref['message']: 
            temp["page"] = str(data_crossref['message']['page'])

        temp["articlenumber"] = ''
        if 'articlenumber' in data_crossref['message']: 
            temp["article-number"] = str(data_crossref['message']['article-number'])

        # Get authors
        temp["numberauthor"] = 0
        temp["listauthor"] = ''
        temp["author"] = {}
        temp_list = {}
        if 'author' in data_crossref['message']: 
            for author_i in data_crossref['message']['author']:
                temp["listauthor"] = temp["listauthor"] + str(author_i['given']) + ' ' + str(author_i['family']) + ', '
                temp["numberauthor"] = temp["numberauthor"] + 1

                temp_author = {}
                temp_author['given'] = author_i['given']
                temp_author['family'] = author_i['family']
     
                temp_list[str(int(temp["numberauthor"]))] = temp_author
                
            if temp["numberauthor"] > 0:
                temp["listauthor"] = temp["listauthor"][:-2]

            temp["author"] = temp_list

    selected_ref.data = temp # Main OldHara data
    selected_ref.data_text = json.dumps(temp) # Text version
    selected_ref.save()


def update_doi(request,selected_ref):
    """
    Update entry from its doi.
    """
    doi = request.POST['doi']

    # create a form instance and populate it with data from the request:
    form_update_doi_form = form_update_doi({'doi': doi})
    form_update_doi_isUpdated = False
    
    # check whether it's valid:
    if form_update_doi_form.is_valid():
        doi = str(request.POST['doi']).lower()

        crossrefurl = 'https://api.crossref.org/v1/works/' + doi
        crossrefrequest = requests.get(crossrefurl)

        if crossrefrequest.status_code == 200:
            form_update_doi_isnotValid = False
            form_update_doi_isUpdated = True

            update_entry_from_crossref_doi(crossrefrequest, doi, selected_ref)
            
        else:
            form_update_doi_isnotValid = True
    else:
        form_update_doi_isnotValid = True

    return form_update_doi_form, form_update_doi_isUpdated, form_update_doi_isnotValid 

