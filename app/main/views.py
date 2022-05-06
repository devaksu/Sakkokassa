from django.shortcuts import render, redirect
from .models import Pelaajat, Kulut, Maksu, Sakko
from .forms import MaksuForm, SakkoForm, KuluForm
from django.db.models import Sum, F
from django.contrib import messages
from django.contrib.auth.decorators import login_required

@login_required(login_url='/UserAuth/login_user')
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
            messages.success(response, ("Sakko lisätty!"))

            sakko_update = Pelaajat.objects.get(pelaaja_nimi=p)
            sakko_update.saadut_sakot += a
            sakko_update.save(update_fields = ["saadut_sakot"])
            
            return redirect('/sakko')

    else:
        form = SakkoForm()
        
    return render(response, "main/sakko.html", {"form":form})

@login_required(login_url='/UserAuth/login_user')
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
            messages.success(response, ("Kulu lisätty!"))
            return redirect('/kulu')
        
    else:
        form = KuluForm()

    return render(response, "main/kulu.html", {"form":form})

@login_required(login_url='/UserAuth/login_user')
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
            messages.success(response, ("Maksu lisätty!"))

            maksu_update = Pelaajat.objects.get(pelaaja_nimi=p)
            maksu_update.maksetut_sakot += s
            maksu_update.save(update_fields = ['maksetut_sakot'])

            return redirect('/maksu')

    else:
        form = MaksuForm()                    

    return render(response, "main/maksu.html", {"form":form})

@login_required(login_url='/UserAuth/login_user')
def tapahtumat(response):
    kulut = Kulut.objects.all()
    sakko = Sakko.objects.all()
    sakko = sakko.order_by('pelaaja_id')
    maksu = Maksu.objects.all()

    saadut = Pelaajat.objects.aggregate(sum=Sum('saadut_sakot'))
    if saadut['sum'] is None:
        saadut['sum'] = 0
    
    maksetut = Pelaajat.objects.aggregate(sum=Sum('maksetut_sakot'))
    if maksetut['sum'] is None:
        maksetut['sum'] = 0
    
    kulutettu = Kulut.objects.aggregate(sum=Sum('kulu_summa'))
    if kulutettu['sum'] is None:
        kulutettu['sum'] = 0
    
    return render(response, "main/tapahtumat.html", 
                {"kulut":kulut, "sakot":sakko, "maksut":maksu, "saadut":saadut, "maksetut":maksetut, "kulutettu":kulutettu}) 

@login_required(login_url='/UserAuth/login_user')
def maksamatta(response):
    pelaaja = Pelaajat.objects.all()
    
    maksamatta = Pelaajat.objects.annotate(maksamatta_sakot=F('saadut_sakot')-F('maksetut_sakot')).aggregate(sum=Sum('maksamatta_sakot'))
    if maksamatta is None:
        maksamatta = 0
    
    return render(response, "main/maksamatta.html", { "pelaaja":pelaaja, "maksamatta":maksamatta,})

@login_required(login_url='/UserAuth/login_user')
def index(response):
    saadut = Pelaajat.objects.aggregate(sum=Sum('saadut_sakot'))
    if saadut['sum'] is None:
        saadut['sum'] = 0
    
    kulutettu = Kulut.objects.aggregate(sum=Sum('kulu_summa'))
    if kulutettu['sum'] is None:
        kulutettu['sum'] = 0
    
    maksamatta = Pelaajat.objects.annotate(maksamatta_sakot=F('saadut_sakot')-F('maksetut_sakot')).aggregate(sum=Sum('maksamatta_sakot'))
    if maksamatta['sum'] is None:
        maksamatta['sum'] = 0

    kassa = saadut['sum'] - maksamatta['sum'] - kulutettu['sum']
    
    return render(response, "main/index.html", {"saadut":saadut, "kulutettu":kulutettu, "maksamatta":maksamatta,"kassa":kassa})