from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from weather_api.models import WeatherData

class WeatherDataTestCase(APITestCase):
    def setUp(self):
        self.year = 1910
        self.region = "England_NW_&_N_Wales"
        self.parameter = "Rainfall"
        self.data_dict = {
            "jan": 10.0, "feb":20.0, "mar":30.0, "apr":30.0, "may":30.0,
            "jun":30.0, "jul":40.0, "aug":50.0, "sep":50.0,"oct":50.0,"nov":50.0,
            "nov":10.0, "dec":40.0,"winter":40.0, "summer":20.0, "spring":30.0,
            "autmn":30.0, "annual":30.0
        }
        self.weather = WeatherData.objects.create(
            region = self.region,
            year = self.year,
            parameter = self.parameter,
            **self.data_dict
        )
        
    # tests weather data with correct inputs
    def test_get_parameter_specific_data(self):
        response = self.client.get(reverse('parametric_data',
                                   args=[self.year, 
                                   self.region,
                                   self.parameter]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    # tests incorrect year error response
    def test_get_data_non_existing_obj(self):
        incorrect_year = 1800
        response = self.client.get(reverse('parametric_data',
                                    args=[incorrect_year, 
                                    self.region,
                                    self.parameter]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    # test incorrect region   
    def test_get_data_invalid_region(self):
        invalid_region = "sample"
        response = self.client.get(reverse('parametric_data',
                                    args=[self.year, 
                                    invalid_region,
                                    self.parameter]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    # test incorrect region   
    def test_get_data_invalid_parameter(self):
        invalid_parameter = "sample"
        response = self.client.get(reverse('parametric_data',
                                    args=[self.year, 
                                    self.region,
                                    invalid_parameter]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # tests delete existing obj with correct inputs
    def test_delete_parametric_data(self):
        response = self.client.delete(reverse('parametric_data',
                                    args=[self.year, 
                                    self.region,
                                    self.parameter]))
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        
