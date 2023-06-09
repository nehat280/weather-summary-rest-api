from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

from web_scrapper.models import WeatherData
from weather_api.api.serializers import WeatherDataSerializer
from web_scrapper.views import get_data

@api_view()
def year_specific_data(request, year, region,parameter):
    print("year,region, parameter",year,region, parameter)
    if request.method == "GET":
        try:
            climate = WeatherData.objects.get(year=year, region=region, parameter=parameter) 
            # if climate.exists():
            #     climate = climate.first()
            #     print(climate)
        except:
            response = get_data(request, region, parameter)
            if response.status_code == 200:
                print(year, region, parameter)
                try:
                    climate = WeatherData.objects.get(year=year, region=region, parameter=parameter)
                except WeatherData.DoesNotExist:
                    return Response({'error':"weather data with given inputs not found. Kindly check documentation for valid inputs.Possible reasons: Year out of range.",
                                     'status':status.HTTP_404_NOT_FOUND})
                
        serializer = WeatherDataSerializer(climate)
        print("serializer.data",serializer)
        return Response(serializer.data)

