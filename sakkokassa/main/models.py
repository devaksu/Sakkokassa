from django.db import models
import datetime

# Create your models here.
class Sakko(models.Model):
    PELAAJA = (
        (32,'Aksu'),
        (18,'Hoppe'),
        (101,'Jone'),
    )

    RIKE = (
        (1,'1. CT Unohdus - 5€'),
        (2,'2. Varusteen unohdus - 5€'), 
        (3,'3. Jäähy 2min - 2€'),
        (4,'4. Jäähy 5min - 5€'),
        (5,'5. Muu sakko - 5€'),
        (6,'6. Myöhästyminen - 5€'),
        (7,'7. Väärä varuste - 5€'),
        (8,'8. ISO Muu sakko - 10€'), 
    )

    KERROIN = (
        (1,'x1'),
        (2,'x2'),
        (3,'x3'),
        (4,'x4'),
        (5,'x5')
        )

    pelaaja =models.PositiveSmallIntegerField(max_length=3, choices=PELAAJA, on_delete=models.CASCADE)
    rike =models.PositiveSmallIntegerField(max_lenght=1, choices=RIKE)
    pvm =models.DateField(default=datetime.date.today())
    kerroin =models.PositiveSmallIntegerField(max_length=1, choices=KERROIN)
    selite =models.CharField(max_length=100)