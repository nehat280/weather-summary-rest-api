from django.urls import path
from . import views

urlpatterns = [
    path("get_data/<str:region>/<str:parameter>", views.get_data, name="get_data"),
]