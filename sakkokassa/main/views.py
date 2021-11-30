from django.shortcuts import render, redirect
from .models import Pelaajat, Kulut, Maksu, Sakko
from .forms import MaksuForm, SakkoForm, KuluForm
from django.db.models import Sum, F

def sakko(response):
    if response.method == "POST":
        form = SakkoForm(response.POST)
    
        if form.is_valid():
            p = form.cleaned_data["pelaaja_id"]
            r = form.cleaned_data["rike_id"]
            s = form.cleaned_data["sakko_selite"]
            d = form.cleaned_data["pvm"]
            a = form.cleaned_data["sakko_summa"]
            sakko = Sakko( pelaaja_id=p,
                            rike_id=r,
                            sakko_selite=s,
                            pvm=d,
                            sakko_summa=a
                        )
            sakko.save()

            sakko_update = Pelaajat.objects.get(pelaaja_nimi=p)
            sakko_update.saadut_sakot += a
            sakko_update.save(update_fields = ["saadut_sakot"])
            
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

            maksu_update = Pelaajat.objects.get(pelaaja_nimi=p)
            maksu_update.maksetut_sakot += s
            maksu_update.save(update_fields = ['maksetut_sakot'])

            return redirect('/maksu')

    else:
        form = MaksuForm()                    

    return render(response, "main/maksu.html", {"form":form})


def tapahtumat(response):
    kulut = Kulut.objects.all()
    sakko = Sakko.objects.all()
    sakko = sakko.order_by('pelaaja_id')
    maksu = Maksu.objects.all()
    saadut = Pelaajat.objects.aggregate(sum=Sum('saadut_sakot'))
    maksetut = Pelaajat.objects.aggregate(sum=Sum('maksetut_sakot'))
    kulutettu = Kulut.objects.aggregate(sum=Sum('kulu_summa'))
    return render(response, "main/tapahtumat.html", 
                {"kulut":kulut, "sakot":sakko, "maksut":maksu, "saadut":saadut, "maksetut":maksetut, "kulutettu":kulutettu}) 


def maksamatta(response):
    pelaaja = Pelaajat.objects.all()
    maksamatta = Pelaajat.objects.annotate(maksamatta_sakot=F('saadut_sakot')-F('maksetut_sakot')).aggregate(sum=Sum('maksamatta_sakot'))

    return render(response, "main/maksamatta.html", { "pelaaja":pelaaja, "maksamatta":maksamatta,})


def index(response):
    return render(response, "main/home.html", {})
