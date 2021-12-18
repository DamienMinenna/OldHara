import os

from .models import Folder_Refs
from .forms import form_create_folder

def create_folder(request):
    form_create_folder_isCreated = False
    form_create_folder_isExist = False

    # create a form instance and populate it with data from the request:
    form_create_folder_form = form_create_folder(request.POST)
    
    # check whether it's valid:
    if form_create_folder_form.is_valid():

        nameFolder = request.POST['nameFolder']
        path = str('media/') + nameFolder

        if nameFolder == "no folder selected":
            form_create_folder_isExist = True
        elif not os.path.exists(path):
            os.mkdir(path)

            db = Folder_Refs(path = nameFolder)
            db.save()

            form_create_folder_isCreated = True
        else:
            form_create_folder_isExist = True

    return form_create_folder_form, form_create_folder_isCreated, form_create_folder_isExist 