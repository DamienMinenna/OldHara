import os

from .models import Path_Biblio
from .forms import addfolderForm


def add_folder(request):
    isCreated = False
    isExist = False
    isModaladdfolder = False

    # create a form instance and populate it with data from the request:
    form_addfolder = addfolderForm(request.POST)
    # check whether it's valid:
    if form_addfolder.is_valid():

        nameFolder = request.POST['nameFolder']
        path = str('media/') + nameFolder

        if not os.path.exists(path):
            os.mkdir(path)

            b = Path_Biblio(path = nameFolder)
            b.save()

            isCreated = True
        else:
            isExist = True
        isModaladdfolder = True

    return form_addfolder, isCreated, isExist, isModaladdfolder