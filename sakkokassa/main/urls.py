from django.urls import path
from . import views

urlpatterns = [
    path("index/", views.index, name="index"),
    path("", views.index, name="koti"),
    path("sakko/", views.sakko, name="sakko"),
    path("maksu/", views.maksu, name="maksu"),
    path("kulu/", views.kulu, name="kulu"),
    path("maksamatta/", views.maksamatta, name="maksamatta"),
    path("tapahtumat/", views.tapahtumat, name="tapahtumat"),

]