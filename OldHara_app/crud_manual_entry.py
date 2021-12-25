import json
import requests

from .models import Ref, Folder_Refs
from .forms import form_create_ME

def create_manual_entry(request):
    """
    Create manually an new entry
    """

    # create a form instance and populate it with data from the request:
    form_create_ME_form = form_create_ME(request.POST)
    form_create_ME_isCreated = False

    # check whether it's valid:
    if form_create_ME_form.is_valid():

        folder = request.POST['ME_folder']

        ref = Ref(
            title = request.POST['ME_title'],
            folder = Folder_Refs.objects.get(id = folder),
            status = 0,
            doi = '',
        )
        ref.save()

        # Add db 
        temp = {}
        temp["id"] = ref.id
        temp["folder"] = ref.folder.path

        temp["status"] = 0

        # title
        temp["title"] = request.POST['ME_title']

        # Get date
        temp["dateY"] = request.POST['ME_dateY']
        temp["dateM"] = ''
        temp["dateMword"] = request.POST['ME_dateMword']
        temp["dateD"] = request.POST['ME_dateD']

        temp["issue"] = request.POST['ME_issue']

        temp["DOI"] = ''

        temp["type"] = request.POST['ME_type']

        temp["journal"] = request.POST['ME_journal']
        
        temp["volume"] = request.POST['ME_volume']

        temp["page"] = request.POST['ME_page']

        temp["articlenumber"] = request.POST['ME_articlenumber']

        # Get authors
        temp["listauthor"] = request.POST['ME_listauthor']
        temp["author"] = {}

        ref.data = temp # Main OldHara data
        ref.data_text = json.dumps(temp) # Text version
        ref.save()

        form_create_ME_isCreated = True

    return form_create_ME_form, form_create_ME_isCreated