import datetime
from django import forms
from .models import Pelaajat, Rikkeet, Sakko, Kulut, Maksu

class SakkoForm(forms.Form):
    pelaaja_id = forms.ModelChoiceField(queryset=Pelaajat.objects.order_by("pelaaja_id"), label="Nimi:", required=True, )
    rike_id = forms.ModelChoiceField(queryset=Rikkeet.objects.order_by("rike_id"), label="Rike:", required=True)
    sakko_selite = forms.CharField(widget=forms.Textarea, required=False, max_length=100, label="Selite:")
    pvm = forms.DateField(initial=datetime.date.today,label="Päivämäärä:")
    sakko_summa = forms.IntegerField(initial= 5, required=True,label="Summa:",min_value=1)
    
    class Meta:
        model = Sakko
        
class KuluForm(forms.Form):
    kulu_summa  = forms.IntegerField(required=True,label="Summa:", min_value=1)
    kulu_selite = forms.CharField(widget=forms.Textarea, required=True, max_length=100, label="Selite:")
    pvm = forms.DateField(initial=datetime.date.today,label="Päivämäärä:")

    class Meta:
        model = Kulut

class MaksuForm(forms.Form):
    pelaaja = forms.ModelChoiceField(queryset=Pelaajat.objects.order_by("pelaaja_id"), label="Nimi:", required=True, )
    pvm = forms.DateField(initial=datetime.date.today,label="Päivämäärä:")
    summa = forms.IntegerField(initial=15, required=True,label="Summa:",min_value=1)

    class Meta:
        model = Maksu