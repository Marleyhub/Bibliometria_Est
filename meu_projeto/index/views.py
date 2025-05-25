from django.shortcuts import render

def index(request):
    return render(request, 'index/index.html')

def begin_upload(request):
    return render(request,'upload/upload.html')
