from django.db import models
from django.utils import timezone

class Pelaajat(models.Model):
    """ Joukkueen jäsenet ja yhteenveto heidän sakoista ja maksuista """
    pelaaja_id = models.PositiveSmallIntegerField(primary_key=True)
    pelaaja_nimi = models.CharField(max_length=15)
    saadut_sakot = models.PositiveSmallIntegerField(default=0)
    maksetut_sakot = models.PositiveSmallIntegerField(default=0)
    DisplayFields = ['pelaaja_id', 'pelaaja_nimi', 'saadut_sakot', 'maksetut_sakot', 'maksamatta_sakot']

    def __str__(self):
        return u'{0}'.format(self.pelaaja_nimi)

    @property
    def maksamatta_sakot(self):
        maksamatta_sakot = self.saadut_sakot - self.maksetut_sakot
        return maksamatta_sakot
    

class Kulut(models.Model):
    """ Sakkokassasta maksetut kulut ja niiden tiedot """
    kulu_id = models.AutoField(primary_key=True)
    kulu_pvm = models.DateField()
    kulu_selite = models.CharField(max_length=50, blank=True)
    kulu_summa = models.PositiveSmallIntegerField(default=0)
    DisplayFields = ['kulu_id','kulu_pvm', 'kulu_selite','kulu_summa']

    def __str__(self):
        return self.kulu_selite


class Rikkeet(models.Model):
    """ Sakkokassan säännöt """
    rike_id = models.PositiveSmallIntegerField(primary_key=True)
    rike_kuvaus = models.CharField(max_length=50)
    DisplayFields=['rike_id', 'rike_kuvaus',]

    def __str__(self):
        return u'{0}'.format(self.rike_kuvaus)


class Sakko(models.Model):
    """ Sakkokassaan kirjatut rikkeet ja niistä tuomitut rangaistukset """
    pelaaja_id = models.ForeignKey(Pelaajat, on_delete=models.DO_NOTHING, default=0)
    rike_id = models.ForeignKey(Rikkeet, on_delete=models.DO_NOTHING, default=0)
    pvm = models.DateField()
    sakko_selite = models.CharField(max_length=100)
    sakko_summa = models.PositiveSmallIntegerField(default=0)
    DisplayFields=['pelaaja_id','rike_id', 'pvm', 'sakko_selite', 'sakko_summa']
    

class Maksu(models.Model):
    """ Pelaajien sakkokassaan tekemät maksut """
    pelaaja_id = models.ForeignKey(Pelaajat, on_delete=models.DO_NOTHING, default=0)
    pvm = models.DateField()
    maksu_summa = models.PositiveSmallIntegerField(default=0)
    DisplayFields=['pelaaja_id','pvm','maksu_summa']
