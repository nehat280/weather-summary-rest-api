from django.urls import path
from weather_api.api import views

urlpatterns = [
   path("monthly_data/<str:region>/<str:parameter>/<int:year>/<str:month>/", views.monthly_data, name="monthly_data"),
   path("yearly_data/<int:year>/<str:region>/<str:parameter>/", views.yearly_data, name="yearly_data"),
   path("seasonal_data/<str:region>/<str:parameter>/", views.parametric_data, name="parametric_data"),
]
