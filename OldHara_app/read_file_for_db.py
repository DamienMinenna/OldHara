import numpy as np
import PyPDF2

from .models import Biblio

def read_metadata(file_selected):

    filepath = "media/" + file_selected.file.name

    pdf_toread = PyPDF2.PdfFileReader(open(filepath, "rb"))
    pdf_info = str(pdf_toread.getDocumentInfo())

    doi = ''
    find_doi = pdf_info.lower().find("doi:")
    if find_doi != -1:
        next_space = pdf_info.lower().find(" ",find_doi +8)
        next_comma = pdf_info.lower().find(",",find_doi +8)
        next_apostroph = pdf_info.lower().find("'",find_doi +8)
        next_linebreack = pdf_info.lower().find("\n", find_doi +8)

        arr = np.array([next_space, next_comma, next_apostroph, next_linebreack,len(pdf_info)])
        next_end = np.min(arr[np.where(arr > 0)])

        doi = pdf_info[int(find_doi)+4: int(next_end)]

    # pdf_info = 'I find this doi in the metadata: ' + doi
    return doi

def read_firstpages(file_selected):

    filepath = "media/" + file_selected.file.name

    pdf_toread = PyPDF2.PdfFileReader(open(filepath, "rb"))
    number_of_pages = pdf_toread.getNumPages()
    page_content = ''
    for i in range(4):
        if i+1 < number_of_pages:
            page = pdf_toread.getPage(i)
            page_content += page.extractText()

    doi = ''
    find_doi = page_content.lower().find("doi:")
    find_doi2 = page_content.lower().find("doi/")
    find_doi3 = page_content.lower().find("10.")
    find_doi4 = page_content.lower().find("doi.org/")
    if find_doi != -1:
        next_space = page_content.lower().find(" ",find_doi +8)
        next_comma = page_content.lower().find(",",find_doi +8)
        next_apostroph = page_content.lower().find("'",find_doi +8)
        next_linebreack = page_content.lower().find("\n", find_doi +8)

        arr = np.array([next_space, next_comma, next_apostroph, next_linebreack,len(page_content)])
        next_end = np.min(arr[np.where(arr > 0)])

        doi = page_content[int(find_doi)+4: int(next_end)]

    elif find_doi2 != -1:
        next_space = page_content.lower().find(" ",find_doi2 +8)
        next_comma = page_content.lower().find(",",find_doi2 +8)
        next_apostroph = page_content.lower().find("'",find_doi2 +8)
        next_linebreack = page_content.lower().find("\n", find_doi2 +8)

        arr = np.array([next_space, next_comma, next_apostroph, next_linebreack,len(page_content)])
        next_end = np.min(arr[np.where(arr > 0)])

        doi = page_content[int(find_doi2)+4: int(next_end)]

    elif find_doi3 != -1:
        next_space = page_content.lower().find(" ",find_doi3)
        next_comma = page_content.lower().find(",",find_doi3)
        next_apostroph = page_content.lower().find("'",find_doi3)
        next_linebreack = page_content.lower().find("\n", find_doi3)

        arr = np.array([next_space, next_comma, next_apostroph, next_linebreack,len(page_content)])
        next_end = np.min(arr[np.where(arr > 0)])

        doi = page_content[int(find_doi3): int(next_end)]
        
    elif find_doi4 != -1:
        next_space = page_content.lower().find(" ",find_doi4)
        next_comma = page_content.lower().find(",",find_doi4)
        next_apostroph = page_content.lower().find("'",find_doi4)
        next_linebreack = page_content.lower().find("\n", find_doi4)

        arr = np.array([next_space, next_comma, next_apostroph, next_linebreack,len(page_content)])
        next_end = np.min(arr[np.where(arr > 0)])

        doi = page_content[int(find_doi4)+8: int(next_end)]

    
    #page_content = 'I find this doi in the first page: ' + doi
    return doi