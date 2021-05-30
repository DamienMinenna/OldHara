import json
import requests

from .models import Biblio, Path_Biblio
from .forms import addDOIForm

def add_doi_to_db(r, folder):
    d = json.loads(r.text)  # r.text == <class 'str'>  and d == <class 'dict'>
    title_newentry = str(d['message']['title'][0])

    c = Biblio(
        title = title_newentry,
        data = d,
        json_payload = r.text,
        folder = Path_Biblio.objects.get(id = folder),
        status = 1,
    )

    c.save()

    # Add db 
    temp = {}
    temp["id"] = c.id
    temp["folder"] = c.folder.path

    if 'message' in d:

        temp["title"] = ''
        if 'title' in d['message']:
            temp["title"] = str(d['message']['title'][0])

        # Get date
        temp["dateY"] = ''
        temp["dateM"] = ''
        temp["dateMword"] = ''
        temp["dateD"] = ''
        if 'issued' in d['message']:
            if 'date-parts' in d['message']['issued']:
                if len(d['message']['issued']['date-parts'][0]) >= 1:
                    temp["dateY"] = str(d['message']['issued']['date-parts'][0][0])

                if len(d['message']['issued']['date-parts'][0]) >= 2:
                    temp["dateM"] = str(d['message']['issued']['date-parts'][0][1])
                    if d['message']['issued']['date-parts'][0][1] == 1:
                        temp["dateMword"] = 'January'
                    elif d['message']['issued']['date-parts'][0][1] == 2:
                        temp["dateMword"] = 'Febuary'
                    elif d['message']['issued']['date-parts'][0][1] == 3:
                        temp["dateMword"] = 'March'
                    elif d['message']['issued']['date-parts'][0][1] == 4:
                        temp["dateMword"] = 'April'
                    elif d['message']['issued']['date-parts'][0][1] == 5:
                        temp["dateMword"] = 'May'
                    elif d['message']['issued']['date-parts'][0][1] == 6:
                        temp["dateMword"] = 'June'
                    elif d['message']['issued']['date-parts'][0][1] == 7:
                        temp["dateMword"] = 'July'
                    elif d['message']['issued']['date-parts'][0][1] == 8:
                        temp["dateMword"] = 'August'
                    elif d['message']['issued']['date-parts'][0][1] == 9:
                        temp["dateMword"] = 'September'
                    elif d['message']['issued']['date-parts'][0][1] == 10:
                        temp["dateMword"] = 'October'
                    elif d['message']['issued']['date-parts'][0][1] == 11:
                        temp["dateMword"] = 'November'
                    elif d['message']['issued']['date-parts'][0][1] == 12:
                        temp["dateMword"] = 'December'

                if len(d['message']['issued']['date-parts'][0]) == 3:  
                    temp["dateD"] = str(d['message']['issued']['date-parts'][0][2])
       
        temp["issue"] = ''
        if 'issue' in d['message']:
            temp["issue"] = str(d['message']['issue'])

        temp["DOI"] = ''
        if 'DOI' in d['message']: 
            temp["DOI"] = str(d['message']['DOI'].lower())

        temp["type"] = 'other'
        if 'type' in d['message']: 
            temp["type"] = str(d['message']['type'])

        temp["journal"] = ''
        if 'container-title' in d['message']: 
            temp["journal"] = str(d['message']['container-title'][0])
        
        temp["volume"] = ''
        if 'volume' in d['message']: 
            temp["volume"] = str(d['message']['volume'])

        temp["page"] = ''
        if 'page' in d['message']: 
            temp["page"] = str(d['message']['page'])

        temp["articlenumber"] = ''
        if 'articlenumber' in d['message']: 
            temp["article-number"] = str(d['message']['article-number'])

        # Get authors
        temp["numberauthor"] = 0
        temp["listauthor"] = ''
        temp["author"] = {}
        temp_list = {}
        if 'author' in d['message']: 
            for author_i in d['message']['author']:
                temp["listauthor"] = temp["listauthor"] + str(author_i['given']) + ' ' + str(author_i['family']) + ', '
                temp["numberauthor"] = temp["numberauthor"] + 1

                temp_author = {}
                temp_author['given'] = author_i['given']
                temp_author['family'] = author_i['family']
     
                temp_list[str(int(temp["numberauthor"]))] = temp_author
                
            if temp["numberauthor"] > 0:
                temp["listauthor"] = temp["listauthor"][:-2]

            temp["author"] = temp_list
    
    c.db = temp # Main Old Hara db
    c.json_payload = json.dumps(temp)

    d["OldHara"] = temp
    c.data = d
    
    c.save()

def add_doi(request):
    isDOIExist = False
    isDOInotValid = False
    isDOICreated = False
    
    # create a form instance and populate it with data from the request:
    form_doi = addDOIForm(request.POST)
    
    # check whether it's valid:
    if form_doi.is_valid():
        nameDOI = str(request.POST['nameDOI']).lower()
        folder = request.POST['folder']
        refs = Biblio.objects.all()

        # check if DOI exist
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

                    add_doi_to_db(r, folder)
                    
                else:
                    isDOInotValid = True

    return form_doi, isDOIExist, isDOInotValid, isDOICreated