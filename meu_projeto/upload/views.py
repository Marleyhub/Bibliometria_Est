from django.shortcuts import render
from django.http import HttpResponse
from .upload_forms import UploadFileForm

import os
from django.conf import settings
from django.core.files.storage import FileSystemStorage

import rispy, bibtexparser, pandas

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
            ris_dict = parse_ris(file_path)
            print(ris_dict)

        ## .bib/.bibtex entry
        elif uploaded_file.name.endswith('.bib') or uploaded_file.endswith('.bibtex'):
            bib_dict = parse_bibtex(file_path)
            print(bib_dict)

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
    return bib_database.entries

## parsing .ris files
def parse_ris(file_path):
    with open (file_path, 'r', encoding='utf-8') as risfile:
        ris_database = rispy.load(risfile)
    return ris_database
