from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',  include("main.urls")),
    path('UserAuth/', include('UserAuth.urls')),
    path('UserAuth/', include('django.contrib.auth.urls')),

]
#     path("index/", include("main.urls")),