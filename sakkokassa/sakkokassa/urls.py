from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("index/", include("main.urls")),
    path('admin/', admin.site.urls),
    path('',  include("main.urls")),
    path('Sakko',  include("main.urls")),
    path('Maksu',  include("main.urls")),
    path('Kulu',  include("main.urls")),
    path('UserAuth/', include('UserAuth.urls')),
    path('UserAuth/', include('django.contrib.auth.urls')),

]
