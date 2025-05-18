from django.shortcuts import render
from django.http import HttpResponse
from .upload_forms import UploadFileForm


def index(request):
    return HttpResponse("Here the user will be capable to import files like .ris and .BibTex")

def upload(request):
    return render(request, "upload/upload.html")

def upload_this(request):
    file_content = None  
    uploaded_file = None
    filename = None

    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES['file']
            file_content = uploaded_file.read().decode('utf-8')
            filename = uploaded_file.name

        if uploaded_file.name.endswith('.ris'):
            print('Ris file recieved')

        elif uploaded_file.name.endswith('.bib') or uploaded_file.endswith('.bibtex'):
            print('BibTex file received')
            return render(request, {'filename': uploaded_file.name})
        else:
             print('Unsupported file type')
        

    else:
        form = UploadFileForm()

    return render(request, 'upload/upload_this.html', {
        'form': form,
        'file_content': file_content,
        'filename': filename
    })