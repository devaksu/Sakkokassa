import datetime
from django import forms
from .models import Pelaajat, Rikkeet, Sakko, Kulut, Maksu

class SakkoForm(forms.Form):
    """ Lomake, jolla syötetään uusi sakko järjestelmään """
    pelaaja_id = forms.ModelChoiceField(queryset=Pelaajat.objects.order_by("pelaaja_nimi"), label="Nimi:", required=True, widget=forms.Select(attrs={'class':'form-control'}))
    rike_id = forms.ModelChoiceField(queryset=Rikkeet.objects.order_by("rike_id"), label="Rike:", required=True, widget=forms.Select(attrs={'class':'form-control'}))
    sakko_selite = forms.CharField(required=False, max_length=50, label="Selite:", widget=forms.Textarea(attrs={'class':'form-control', 'rows': '1'}))
    pvm = forms.DateField(initial=datetime.date.today,label="Päivämäärä:", widget=forms.DateInput(attrs={'class':'form-control'}))
    sakko_summa = forms.IntegerField(initial= 5, required=True, label="Summa:", min_value=1, widget=forms.NumberInput(attrs={'class':'form-control'}))
    
    class Meta:
        model = Sakko
        
class KuluForm(forms.Form):
    """ Lomake, jolla syötetään uusi kulu järjestelmään """
    kulu_summa  = forms.IntegerField(required=True,label="Summa:", min_value=1, widget=forms.NumberInput(attrs={'class':'form-control'}))
    kulu_selite = forms.CharField(required=True, max_length=100, label="Selite:", widget=forms.Textarea(attrs={'class':'form-control', 'rows': '1'}))
    pvm = forms.DateField(initial=datetime.date.today,label="Päivämäärä:", widget=forms.DateInput(attrs={'class':'form-control'}))

    class Meta:
        model = Kulut

class MaksuForm(forms.Form):
    """ Lomake, jolla syötetään maksu järjestelmään """
    pelaaja_id = forms.ModelChoiceField(queryset=Pelaajat.objects.order_by("pelaaja_nimi"), label="Nimi:", required=True, widget=forms.Select(attrs={'class':'form-control'}))
    pvm = forms.DateField(initial=datetime.date.today,label="Päivämäärä:", widget=forms.DateInput(attrs={'class':'form-control'}))
    summa = forms.IntegerField(initial=15, required=True,label="Summa:",min_value=1, widget=forms.NumberInput(attrs={'class':'form-control'}))

    class Meta:
        model = Maksu