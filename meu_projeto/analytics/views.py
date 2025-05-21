from django.shortcuts import render
from django.http import HttpResponse

## Home
def index(request):
    return HttpResponse("Here the user will be capable to do mathematical analitcs from your uploaded .ris or .bib file")

def analyse_this(request):
    return HttpResponse("You've Analised this")