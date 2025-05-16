from django.shortcuts import render

from django.http import HttpResponse


def index(request):
    return HttpResponse("Here the user will be capable to import files like .ris and .BibTex")