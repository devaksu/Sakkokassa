from django.shortcuts import render, redirect
from .models import Pelaajat, Kulut, Maksu, Sakko
from .forms import MaksuForm, SakkoForm, KuluForm
from django.db.models import Sum, F
from django.contrib import messages
from django.contrib.auth.decorators import login_required


@login_required(login_url='/UserAuth/login_user')
def index(response):
    """ Etusivu näyttää yhteenvedon kassan sen hetkisestä tilanteesta """

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
    
    return render(response, "main/index.html", {
                            "saadut":saadut, 
                            "kulutettu":kulutettu, 
                            "maksamatta":maksamatta,
                            "kassa":kassa
                            }
                        )


@login_required(login_url='/UserAuth/login_user')
def sakko(response):
    """ Funktiolla lisätään pelaajalle sakko """
    if response.method == "POST":
        form = SakkoForm(response.POST)
    
        if form.is_valid():
            pelaaja = form.cleaned_data["pelaaja_id"]
            rike = form.cleaned_data["rike_id"]
            selite = form.cleaned_data["sakko_selite"]
            date = form.cleaned_data["pvm"]
            summa = form.cleaned_data["sakko_summa"]
            sakko = Sakko( pelaaja_id=pelaaja,
                            rike_id=rike,
                            sakko_selite=selite,
                            pvm=date,
                            sakko_summa=summa
                        )
            sakko.save()
            messages.success(response, ("Sakko lisätty!"))

            sakko_update = Pelaajat.objects.get(pelaaja_nimi=pelaaja)
            sakko_update.saadut_sakot += summa
            sakko_update.save(update_fields = ["saadut_sakot"])
            
            return redirect('/sakko')

    else:
        form = SakkoForm()
        
    return render(response, "main/sakko.html", {"form":form})

@login_required(login_url='/UserAuth/login_user')
def kulu(response):
    """ Funktiolla lisätään kassasta maksettuja kuluja """
    if response.method == "POST":
        form = KuluForm(response.POST)

        if form.is_valid():
            summa = form.cleaned_data["kulu_summa"]
            selite = form.cleaned_data["kulu_selite"]
            date = form.cleaned_data["pvm"]
            kulu = Kulut(   kulu_pvm=date,
                            kulu_selite=selite,
                            kulu_summa=summa
                        )
            kulu.save()
            messages.success(response, ("Kulu lisätty!"))
            return redirect('/kulu')
        
    else:
        form = KuluForm()

    return render(response, "main/kulu.html", {"form":form})

@login_required(login_url='/UserAuth/login_user')
def maksu(response):
    """ Funktiolla kuitataan pelaajan maksaneen sakkoja kassaan """
    if response.method == "POST":
        form = MaksuForm(response.POST)

        if form.is_valid():
            pelaaja = form.cleaned_data["pelaaja_id"]
            date = form.cleaned_data["pvm"]
            summa = form.cleaned_data["summa"]
            maksu = Maksu(  pelaaja_id=pelaaja,
                            pvm=date,
                            maksu_summa=summa
                        )
            maksu.save()
            messages.success(response, ("Maksu lisätty!"))

            maksu_update = Pelaajat.objects.get(pelaaja_nimi=pelaaja)
            maksu_update.maksetut_sakot += summa
            maksu_update.save(update_fields = ['maksetut_sakot'])

            return redirect('/maksu')

    else:
        form = MaksuForm()                    

    return render(response, "main/maksu.html", {"form":form})

@login_required(login_url='/UserAuth/login_user')
def tapahtumat(request):
    """ Funktiolla kerätään kaikki sakkokassan tapahtumat yhdelle sivulle """

    # Poista sakko
    if request.method == "POST":
        poistettava_id = request.POST.get("sakko-id")
        poistettava = Sakko.objects.filter(id=poistettava_id).first()
        if poistettava:
            pelaaja = poistettava.pelaaja_id
            summa = poistettava.sakko_summa
            poistettava.delete()
            sakko_update = Pelaajat.objects.get(pelaaja_nimi=pelaaja)
            sakko_update.saadut_sakot -= summa
            sakko_update.save(update_fields = ["saadut_sakot"])
    
    kulut = Kulut.objects.all().order_by('-kulu_pvm')
    sakot = Sakko.objects.all().order_by('-pvm')
    maksu = Maksu.objects.all().order_by('-pvm')

    # Huomioidaan if-lauseella mikäli tietokannassa ei ole tietoja 
    saadut = Pelaajat.objects.aggregate(sum=Sum('saadut_sakot'))
    if saadut['sum'] is None:
        saadut['sum'] = 0
    
    maksetut = Pelaajat.objects.aggregate(sum=Sum('maksetut_sakot'))
    if maksetut['sum'] is None:
        maksetut['sum'] = 0
    
    kulutettu = Kulut.objects.aggregate(sum=Sum('kulu_summa'))
    if kulutettu['sum'] is None:
        kulutettu['sum'] = 0
    
    return render(request, "main/tapahtumat.html", 
                {"kulut":kulut, 
                "sakot":sakot, 
                "maksut":maksu, 
                "saadut":saadut, 
                "maksetut":maksetut, 
                "kulutettu":kulutettu}) 

@login_required(login_url='/UserAuth/login_user')
def maksamatta(response):
    """ Kerätään kaikki maksamattomat sakot pelaajakohtaisesti """
    
    pelaaja = Pelaajat.objects.all()
    
    maksamatta = Pelaajat.objects.annotate(maksamatta_sakot=F('saadut_sakot')-F('maksetut_sakot')).aggregate(sum=Sum('maksamatta_sakot'))
    if maksamatta['sum'] is None:
        maksamatta['sum'] = 0
    
    return render(response, "main/maksamatta.html", { "pelaaja":pelaaja, "maksamatta":maksamatta,})


@login_required(login_url='/UserAuth/login_user')
def pelaajat(response):
    pelaaja = Pelaajat.objects.values("pelaaja_id", "saadut_sakot", "pelaaja_nimi")
    sakot = Sakko.objects.values("pelaaja_id", "rike_id__rike_kuvaus", "pvm","sakko_selite", "sakko_summa")
    return render(response, "main/pelaajat.html", { "pelaaja":pelaaja, "sakot":sakot})