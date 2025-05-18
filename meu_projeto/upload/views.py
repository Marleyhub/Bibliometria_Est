from django.shortcuts import render
from django.http import HttpResponse
from .upload_forms import UploadFileForm

import os
from django.conf import settings
from django.core.files.storage import FileSystemStorage

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

            upload_dir = os.path.join(settings.MEDIA_ROOT, 'uploads')
            os.makedirs(upload_dir, exist_ok=True)

            fs = FileSystemStorage(location=upload_dir)
            saved_filename = fs.save(filename, uploaded_file)
            saved_file_path = fs.path(saved_filename) 

            print(f'File saved at: {saved_file_path}')
            
        if uploaded_file.name.endswith('.ris'):
            print('Ris file recieved')
        elif uploaded_file.name.endswith('.bib') or uploaded_file.endswith('.bibtex'):
            print('BibTex file received')
        else:
             print('Unsupported file type')
        
    else:
        form = UploadFileForm()

    ## Rendering contents
    return render(request, 'upload/upload_this.html', {
        'form': form,
        'file_content': file_content,
        'filename': filename
    })