from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(Pelaajat)
class PelaajatAdmin(admin.ModelAdmin):
    list_display=Pelaajat.DisplayFields


@admin.register(Kulut)
class KulutAdmin(admin.ModelAdmin):
    list_display=Kulut.DisplayFields


@admin.register(Sakko)
class SakkoAdmin(admin.ModelAdmin):
    list_display=Sakko.DisplayFields   


@admin.register(Rikkeet)
class RikkeetAdmin(admin.ModelAdmin):
    list_display=Rikkeet.DisplayFields        