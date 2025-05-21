from django.shortcuts import render
from django.http import HttpResponse
from .upload_forms import UploadFileForm

import os
from django.conf import settings
from django.core.files.storage import FileSystemStorage

import rispy, bibtexparser
import pandas as pd

## Home
def index(request):
    return HttpResponse("Here the user will be capable to import files like .ris and .BibTex")

## upload interface 
def upload(request):
    return render(request, "upload/upload.html")

## uploading file
def upload_this(request):
    
    ## Default table
    file_content = None  
    uploaded_file = None
    filename = None

    ## Upload logic
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)

        ## validation
        if form.is_valid():
            uploaded_file = request.FILES['file']
            file_content = uploaded_file.read().decode('utf-8')
            filename = uploaded_file.name
            file_extension = filename.split('.')[-1].lower()
            file_path = f'./media/uploads/{filename}'

            upload_dir = os.path.join(settings.MEDIA_ROOT, 'uploads')
            os.makedirs(upload_dir, exist_ok=True)

            fs = FileSystemStorage(location=upload_dir)
            saved_filename = fs.save(filename, uploaded_file)
            saved_file_path = fs.path(saved_filename) 

            print(f'File saved at: {saved_file_path}')
        
        ## .ris entry
        if uploaded_file.name.endswith('.ris'):
            ris_dataframe = parse_ris(file_path)
            print(ris_dataframe)

        ## .bib/.bibtex entry
        elif uploaded_file.name.endswith('.bib') or uploaded_file.endswith('.bibtex'):
            bib_dataframe = parse_bibtex(file_path)
            print(bib_dataframe)

        else:
             print('Unsupported file type')

    ## exception    
    else:
        form = UploadFileForm()

    ## Rendering contents
    return render(request, 'upload/upload_this.html', {
        'form': form,
        'file_content': file_content,
        'filename': filename
    })

## parsing .bib and .bibtex files
def parse_bibtex(file_path):
    with open (file_path, 'r', encoding='utf-8') as bibfile:
        bib_database = bibtexparser.load(bibfile)
        bib_dict = bib_database.entries
        bib_dataframe = pd.DataFrame(bib_dict)
    return bib_dataframe

## parsing .ris files
def parse_ris(file_path):
    with open (file_path, 'r', encoding='utf-8') as risfile:
        ris_database = rispy.load(risfile)
        ris_dataframe = pd.DataFrame(ris_database)
    return ris_dataframe
