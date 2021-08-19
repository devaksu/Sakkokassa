from django.db import models
from django.utils import timezone

# Create your models here.
class Pelaajat(models.Model):
    pelaaja_id = models.AutoField(primary_key=True)
    pelaaja_nimi = models.CharField(max_length=15)
    saadut_sakot = models.PositiveSmallIntegerField()
    maksetut_sakot = models.PositiveSmallIntegerField()
    jäljellä_sakot = models.PositiveSmallIntegerField()

    @property
    def left():
        jäljellä_sakot = saadut_sakot - maksetut_sakot
        return jäljellä_sakot
    
class Kulut(models.Model):
    kulu_id = models.AutoField(primary_key=True)
    kulu_pvm = models.DateField(default=timezone.now)
    kulu_selite = models.CharField(max_length=50)
    kulu_summa = models.PositiveSmallIntegerField()

class Rikkeet(models.Model):
    rike_id = models.AutoField(primary_key=True)
    rike_kuvaus = models.CharField(max_length=50)
    rike_summa = models.PositiveSmallIntegerField()

class Sakko(models.Model):
    sakko_pelaaja = models.ForeignKey('Pelaajat', on_delete=models.DO_NOTHING, default=0)
    rike = models.ForeignKey('Rikkeet', on_delete=models.DO_NOTHING, default=0)
    pvm = models.DateField(default=timezone.now)
    sakko_selite = models.CharField(max_length=100)
    sakko_summa = models.PositiveSmallIntegerField(default=0)
    tuplasakko = models.BooleanField(default=0)
    