from django.shortcuts import render
from django.http import HttpResponse
from .upload_forms import UploadFileForm


def index(request):
    return HttpResponse("Here the user will be capable to import files like .ris and .BibTex")

def upload(request):
    return render(request, "upload/upload.html")

def upload_this(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.File)
        if form.is_valid():
            uploaded_file = request.FILES['file']
            file_content = uploaded_file.read().decode9=('utf-8')

    if uploaded_file.name.endswith('.ris'):
        print('Ris file recieved')

    elif uploaded_file.name.endswith('.bib') or uploaded_file.endswith('.bibtex'):
        print('BibTex file received')
        return render(request, {'filename': uploaded_file.name})
    else:
        form = UploadFileForm()

    return render(request, 'upload/upload_form.html', {'form': form})