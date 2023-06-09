from django.urls import path
from weather_api.api import views

urlpatterns = [
   path("<int:year>/<str:region>/<str:parameter>/", views.parameter_specific_data, name="parametric_data"),
]