import os

from django.conf import settings

from .models import Ref, Folder_Refs
from .forms import form_create_folder

def create_folder(request):
    form_create_folder_isCreated = False
    form_create_folder_isExist = False

    # create a form instance and populate it with data from the request:
    form_create_folder_form = form_create_folder(request.POST)
    
    # check whether it's valid:
    if form_create_folder_form.is_valid():

        create_folder = request.POST['create_folder']
        path = str('media/') + create_folder

        if create_folder == "no folder selected":
            form_create_folder_isExist = True
        elif not os.path.exists(path):
            os.mkdir(path)

            db = Folder_Refs(path = create_folder)
            db.save()

            form_create_folder_isCreated = True
        else:
            form_create_folder_isExist = True

    return form_create_folder_form, form_create_folder_isCreated, form_create_folder_isExist 

def delete_folder(request):
    remove_folder = request.POST['remove-folder']

    refs = Ref.objects.filter(folder = remove_folder)
    folder = Folder_Refs.objects.get(id = remove_folder)
    folder_name = settings.MEDIA_ROOT + Folder_Refs.objects.get(id = remove_folder).path

    for ref in refs:
        path = ref.file.path
        os.remove(path)

    os.rmdir(folder_name)

    refs.delete()
    folder.delete()