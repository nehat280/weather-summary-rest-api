from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

from weather_api.models import WeatherData
from weather_api.api.serializers import WeatherDataSerializer,YearlyWeatherDataSerializer
from weather_api.web_scrapper.get_data import get_data
from weather_api.api.pagination import StandardResultsSetPagination


def check_inputs_validity(region, parameter):
    accepted_parameters = ["Max_temp","Min_temp","Mean_temp","Sunshine","Rainfall","Rain_days_1.0mm","Days_of_Air_Frost"]
    accepted_region = ["UK","England","Wales","Scotland","Northern_Ireland","England_&_Wales","England_N","England_S",
                        "Scotland_N","Scotland_E","Scotland_W","England_E_&_NE","England_NW_&_N_Wales","Midlands","East_Angelia",
                        "England_SW_&_S_Wales","England_SE_&_Central_S"]    
    if region not in accepted_region:
        return False
    if parameter not in accepted_parameters:
        return False
    return True

@api_view(['GET','DELETE'])
def yearly_data(request, year, region,parameter):
    if request.method == "GET":
        data_check = check_inputs_validity(region,parameter)
        if data_check:
            
            try:
                climate = WeatherData.objects.get(year=year, region=region, parameter=parameter)
            except Exception as e:
                response = get_data(region, parameter)
                if response.status_code == 200:
                    try:
                        climate = WeatherData.objects.get(year=year, region=region, parameter=parameter)
                    except WeatherData.DoesNotExist:
                        return Response(data={'error':"weather data with given Year not found. Kindly check documentation for valid inputs.Possible reasons: Year out of range."},
                                        status=status.HTTP_404_NOT_FOUND)  
                else:
                    return Response(data={'error':"Error while scraping data"},status=status.HTTP_404_NOT_FOUND)  
                
            serializer = WeatherDataSerializer(climate)
            return Response(data = serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'error':'Invalid region or parameter passed'}, status = status.HTTP_400_BAD_REQUEST)
        
    if request.method == "DELETE":
        try:
            weather = WeatherData.objects.get(year=year, region=region, parameter=parameter)
            weather.delete()
            return Response(status=status.HTTP_202_ACCEPTED)
        except WeatherData.DoesNotExist:
            return Response(data={"error":"weather data with given inputs does not exists"},status=status.HTTP_404_NOT_FOUND)
        
        
@api_view(['GET',])
def parametric_data(request, region, parameter):
    if request.method == "GET":
        data_check = check_inputs_validity(region,parameter)
        if data_check:
            climate = WeatherData.objects.filter(region=region, parameter=parameter).order_by('year')
            if not climate.exists():
                response = get_data(region, parameter)
                if response.status_code == 200:
                        climate = WeatherData.objects.filter(region=region, parameter=parameter).order_by('year')
                else :
                    return Response(data={'error':"Error while scraping data"},status=status.HTTP_404_NOT_FOUND)
            
            paginator = StandardResultsSetPagination()
            paginated_queryset = paginator.paginate_queryset(climate, request)

            # Serialize the paginated results
            serializer = YearlyWeatherDataSerializer(paginated_queryset, many=True)
            return paginator.get_paginated_response(serializer.data)

        else:
            return Response({'error':'Invalid region or parameter passed'}, status = status.HTTP_400_BAD_REQUEST)