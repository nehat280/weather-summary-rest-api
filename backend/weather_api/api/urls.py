from django.urls import path
from weather_api.api import views

urlpatterns = [
   path("yearly_data/<int:year>/<str:region>/<str:parameter>/", views.yearly_data, name="yearly_data"),
   path("parametric_data/<str:region>/<str:parameter>/", views.parametric_data, name="parametric_data"),
]
