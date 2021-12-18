import json
import ntpath
import os

from django.conf import settings

from .models import Ref, Folder_Refs

def create_entry_from_dropzone(request):
    """
    Create new entry from file.
    """
    folder = request.POST['dropzone_folder']
    uploaded_file = request.FILES['file']

    # Create entry
    ref = Ref(
        title = uploaded_file.name,
        status = 1,
        folder = Folder_Refs.objects.get(id = folder),
        file = uploaded_file, 
    )
    ref.save()

    # Move file to the selected folder
    initial_path = ref.file.path
    filename = ntpath.basename(ref.file.name)
    ref.file.name = Folder_Refs.objects.get(id = folder).path + '/' +  filename
    new_path = settings.MEDIA_ROOT + ref.file.name
    os.rename(initial_path, new_path)
    ref.save()

    # Add info to data 
    temp = {}
    temp["id"] = ref.id
    temp["folder"] = ref.folder.path
    temp["title"] = uploaded_file.name

    # Other data (empty)
    temp["dateY"] = ''
    temp["dateM"] = ''
    temp["dateMword"] = ''
    temp["dateD"] = ''
    temp["issue"] = ''
    temp["DOI"] = ''
    temp["type"] = 'other'
    temp["journal"] = ''
    temp["volume"] = ''
    temp["page"] = ''
    temp["articlenumber"] = ''
    temp["numberauthor"] = 0
    temp["listauthor"] = ''
    temp["author"] = {}

    ref.data = temp # Main Old Hara data
    ref.data_text = json.dumps(temp)
    ref.save()

    isfiledropzoneadded = True
    return isfiledropzoneadded