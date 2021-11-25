from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Pelaajat, Kulut, Maksu, Rikkeet, Sakko
from .forms import MaksuForm, SakkoForm, KuluForm

# Create your views here

def sakko(response):
    if response.method == "POST":
        form = SakkoForm(response.POST)
    
        if form.is_valid():
            p = form.cleaned_data["pelaaja_id"]
            r = form.cleaned_data["rike_id"]
            s = form.cleaned_data["sakko_selite"]
            d = form.cleaned_data["pvm"]
            a = form.cleaned_data["sakko_summa"]
            sakko = Sakko(  pelaaja_id=p,
                            rike_id=r,
                            sakko_selite=s,
                            pvm=d,
                            sakko_summa=a
                        )
            sakko.save()
            return redirect('/sakko')

    else:
        form = SakkoForm()
        
    return render(response, "main/sakko.html", {"form":form})


def kulu(response):
    if response.method == "POST":
        form = KuluForm(response.POST)

        if form.is_valid():
            a = form.cleaned_data["kulu_summa"]
            s = form.cleaned_data["kulu_selite"]
            d = form.cleaned_data["pvm"]
            kulu = Kulut(   kulu_pvm=d,
                            kulu_selite=s,
                            kulu_summa=a
                        )
            kulu.save()
            return redirect('/kulu')
        
    else:
        form = KuluForm()

    return render(response, "main/kulu.html", {"form":form})


def maksu(response):
    if response.method == "POST":
        form = MaksuForm(response.POST)

        if form.is_valid():
            p = form.cleaned_data["pelaaja"]
            d = form.cleaned_data["pvm"]
            s = form.cleaned_data["summa"]
            maksu = Maksu(  pelaaja_id=p,
                            pvm=d,
                            maksu_summa=s
                        )
            maksu.save()
            return redirect('/maksu')

    else:
        form = MaksuForm()                    

    return render(response, "main/maksu.html", {"form":form})


def tapahtumat(response):
    kulut = Kulut.objects.all()
    return render(response, "main/tapahtumat.html", {"kulut":kulut}) 

def index(response):
    return render(response, "main/home.html", {})

def kassa(response):
    return render(response, "main/base.html", {})

def maksamatta(response):
    return render(response, "main/base.html", {})


