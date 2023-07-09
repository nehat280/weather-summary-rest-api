from django.urls import path
from weather_api.api import views

urlpatterns = [
   path("monthly_data/<str:region>/<str:parameter>/<int:year>/<str:month>/", views.MonthlyDataView.as_view(), name="monthly_data"),
   path("average_data/<str:region>/<str:parameter>/", views.AverageDataView.as_view(), name="average_data"),
   path("yearly_data/<int:year>/<str:region>/<str:parameter>/", views.YearlyDataView.as_view(), name="yearly_data"),
   path("annual_data/<str:region>/<str:parameter>/<int:year>/", views.AnnualDataView.as_view(), name="annual_data"),
   path("seasonal_data/<str:region>/<str:parameter>/<int:year>/", views.SeasonalDataView.as_view(), name="seasonal_data"),
]
