from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

from weather_api.models import WeatherData
from weather_api.api.serializers import WeatherDataSerializer
from weather_api.web_scrapper.get_data import get_data

@api_view(['GET','DELETE'])
def parameter_specific_data(request, year, region,parameter):
    if request.method == "GET":
        try:
            climate = WeatherData.objects.get(year=year, region=region, parameter=parameter) 
        except Exception as e:
            response = get_data(region, parameter)
            if response.status_code == 200:
                try:
                    climate = WeatherData.objects.get(year=year, region=region, parameter=parameter)
                except WeatherData.DoesNotExist:
                    return Response(data={'error':"weather data with given inputs not found. Kindly check documentation for valid inputs.Possible reasons: Year out of range."},
                                     status=status.HTTP_404_NOT_FOUND)
            elif response.status_code == 404:
                return Response(data={'error':"Invalid Parameter value given"},
                                     status=status.HTTP_404_NOT_FOUND)
        serializer = WeatherDataSerializer(climate)
        return Response({'data':serializer.data},status=status.HTTP_200_OK)
    
    if request.method == "DELETE":
        try:
            weather = WeatherData.objects.get(year=year, region=region, parameter=parameter)
            weather.delete()
            return Response(status=status.HTTP_202_ACCEPTED)
        except WeatherData.DoesNotExist:
            return Response(data={"error":"weather data with given inputs does not exists"},status=status.HTTP_404_NOT_FOUND)
        
    

