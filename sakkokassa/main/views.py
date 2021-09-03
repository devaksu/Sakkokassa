from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(response):
    return HttpResponse("<h1>Sakkokassa<h1/>")

def sakko(response):
    return HttpResponse("<h1>Lisää sakko<h1/>")

def maksu(response):
    return HttpResponse("<h1>Lisää maksu<h1/>")

def kulu(response):
    return HttpResponse("<h1>Lisää kulu<h1/>")

def kassa(response):
    return HttpResponse("<h1>Kassa<h1/>")

def maksamatta(response):
    return HttpResponse("<h1>Maksamattomat sakot<h1/>")

def sakot(response):
    return HttpResponse("<h1>Kaikki sakot<h1/>")        


