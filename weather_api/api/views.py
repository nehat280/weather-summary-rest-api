from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

from weather_api.models import WeatherData
from weather_api.api.serializers import WeatherDataSerializer
from weather_api.web_scrapper.get_data import get_data

@api_view(['GET','DELETE'])
def year_specific_data(request, year, region,parameter):
    if request.method == "GET":
        try:
            climate = WeatherData.objects.get(year=year, region=region, parameter=parameter) 
            if climate.exists():
                climate = climate.first()
        except:
            response = get_data(region, parameter)
            if response.status_code == 200:
                try:
                    climate = WeatherData.objects.get(year=year, region=region, parameter=parameter)
                except WeatherData.DoesNotExist:
                    return Response({'error':"weather data with given inputs not found. Kindly check documentation for valid inputs.Possible reasons: Year out of range.",
                                     'status':status.HTTP_404_NOT_FOUND})
            elif response.status_code == 404:
                return Response({'error':"Invalid Parameter value given,",
                                     'status':status.HTTP_404_NOT_FOUND})
                
        serializer = WeatherDataSerializer(climate)
        return Response(serializer.data)
    if request.method == "DELETE":
        try:
            weather = WeatherData.objects.get(year=year, region=region, parameter=parameter)
            weather.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except WeatherData.DoesNotExist:
            return Response({"error":"weather data with given inputs does not exists",status:status.HTTP_404_NOT_FOUND})
        
    

