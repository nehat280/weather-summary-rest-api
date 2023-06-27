from django.contrib import admin
from django.urls import path, include
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/", include('weather_api.api.urls')),
    path("__debug__/", include("debug_toolbar.urls"))
]
 
