from django.urls import path
from weather_api.api import views

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)

urlpatterns = [
   path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
   path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
   
   path("monthly_data/<str:region>/<str:parameter>/<int:year>/<str:month>/", views.MonthlyDataView.as_view(), name="monthly_data"),
   path("average_data/<str:region>/<str:parameter>/", views.AverageDataView.as_view(), name="average_data"),
   path("yearly_data/<int:year>/<str:region>/<str:parameter>/", views.YearlyDataView.as_view(), name="yearly_data"),
   path("annual_data/<str:region>/<str:parameter>/<int:year>/", views.AnnualDataView.as_view(), name="annual_data"),
   path("seasonal_data/<str:region>/<str:parameter>/<int:year>/", views.SeasonalDataView.as_view(), name="seasonal_data"),
]
