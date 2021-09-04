from django.db import models
from django.utils import timezone

# Create your models here.
class Pelaajat(models.Model):
    pelaaja_id = models.PositiveSmallIntegerField(primary_key=True)
    pelaaja_nimi = models.CharField(max_length=15)
    saadut_sakot = models.PositiveSmallIntegerField(default=0)
    maksetut_sakot = models.PositiveSmallIntegerField(default=0)
    DisplayFields = ['pelaaja_id', 'pelaaja_nimi', 'saadut_sakot', 'maksetut_sakot', 'maksamatta_sakot']

    @property
    def maksamatta_sakot(self):
        maksamatta_sakot = self.saadut_sakot - self.maksetut_sakot
        return maksamatta_sakot
    

class Kulut(models.Model):
    kulu_id = models.AutoField(primary_key=True)
    kulu_pvm = models.DateField(default=timezone.now)
    kulu_selite = models.CharField(max_length=50)
    kulu_summa = models.PositiveSmallIntegerField()
    DisplayFields = ['kulu_id','kulu_pvm', 'kulu_selite','kulu_summa']


class Rikkeet(models.Model):
    rike_id = models.AutoField(primary_key=True)
    rike_kuvaus = models.CharField(max_length=50)
    rike_summa = models.PositiveSmallIntegerField()
    DisplayFields=['rike_id', 'rike_kuvaus', 'rike_summa']


class Sakko(models.Model):
    pelaaja_id = models.ForeignKey(Pelaajat, on_delete=models.DO_NOTHING, default=0)
    rike_id = models.ForeignKey(Rikkeet, on_delete=models.DO_NOTHING, default=0)
    pvm = models.DateField(default=timezone.now)
    sakko_selite = models.CharField(max_length=100)
    sakko_summa = models.PositiveSmallIntegerField(default=0)
    tuplasakko = models.BooleanField(default=0)
    DisplayFields=['pelaaja_id','rike_id', 'pvm', 'sakko_selite', 'sakko_summa', 'tuplasakko']
    