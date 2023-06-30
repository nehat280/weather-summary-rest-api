from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from django.db.models import Avg
from django.db.models.functions import Round

from weather_api.models import Region, Parameter, MonthlyData, SeasonsalData
from weather_api.api.serializers import MonthlyDataSerializer, SeasonsalDataSerializer,DictionarySerializer
from weather_api.web_scrapper.get_data import get_data
from weather_api.api.pagination import StandardResultsSetPagination
from weather_api.web_scrapper.Constants import PARAMETERS, REGIONS

def check_inputs_validity(region, parameter):
    if region not in REGIONS:
        return False
    if parameter not in PARAMETERS:
        return False
    return True

@api_view(['GET'])
def monthly_data(request, region,parameter, year, month):
    
    if request.method == "GET":
        data_check = check_inputs_validity(region,parameter)
        if data_check:
            
            try:
                climate = MonthlyData.objects.get(year = year, month__name=month, 
                                                  region__name=region, 
                                                  parameter__name = parameter)
                
            except (MonthlyData.DoesNotExist, Region.DoesNotExist, Parameter.DoesNotExist):
                
                result = get_data(region, parameter)
        
                if result:
                    try:
                        climate = MonthlyData.objects.get(year = year, month__name=month,
                                                           region__name=region,
                                                            parameter__name = parameter)
                    except MonthlyData.DoesNotExist:
                        return Response(data={'error':"weather data with given month not found. Kindly check documentation for valid inputs."},
                                        status=status.HTTP_404_NOT_FOUND)  
                else:
                    return Response(data={'error':"Error while scraping data"},status=status.HTTP_404_NOT_FOUND)  
            print(climate)
            serializer = MonthlyDataSerializer(climate)
            return Response(data = serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'error':'Invalid region or parameter passed'}, status = status.HTTP_400_BAD_REQUEST)
        

@api_view(['GET'])
def average_data(request, region,parameter):
    
    if request.method == "GET":
        data_check = check_inputs_validity(region,parameter)
        if data_check:
            
            try:

                filtered_weather = (MonthlyData.objects
                                    .filter(region__name=region, parameter__name=parameter))

            except (MonthlyData.DoesNotExist, Region.DoesNotExist, Parameter.DoesNotExist):
                
                result = get_data(region, parameter)

                if result:
                    try:
                        filtered_weather = MonthlyData.objects.filter(region__name=region, parameter__name=parameter)
                        
                    except MonthlyData.DoesNotExist:
                        return Response(data={'error':"weather data with given month not found. Kindly check documentation for valid inputs."},
                                        status=status.HTTP_404_NOT_FOUND)  
                else:
                    return Response(data={'error':"Error while scraping data"},status=status.HTTP_404_NOT_FOUND)  

            averages = (filtered_weather.values('region', 'parameter', 'month__name')
                                .annotate(avg_month_value=Round(Avg('value'),2)))
            serializer = DictionarySerializer(averages,many=True)

            return Response(data = serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'error':'Invalid region or parameter passed'}, status = status.HTTP_400_BAD_REQUEST)

@api_view(['GET','DELETE'])
def yearly_data(request, year, region,parameter):
    if request.method == "GET":
        data_check = check_inputs_validity(region,parameter)
        if data_check:
           
            try:
                climate = SeasonsalData.objects.get(year=year, region=region, parameter=parameter)
            except Exception as e:
                response = get_data(region, parameter)
                if response.status_code == 200:
                    try:
                        climate = SeasonsalData.objects.get(year=year, region=region, parameter=parameter)
                    except SeasonsalData.DoesNotExist:
                        return Response(data={'error':"weather data with given Year not found. Kindly check documentation for valid inputs.Possible reasons: Year out of range."},
                                        status=status.HTTP_404_NOT_FOUND)  
                else:
                    return Response(data={'error':"Error while scraping data"},status=status.HTTP_404_NOT_FOUND)  
                
            serializer = SeasonsalData(climate)
            return Response(data = serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'error':'Invalid region or parameter passed'}, status = status.HTTP_400_BAD_REQUEST)
        
    if request.method == "DELETE":
        try:
            weather = SeasonsalData.objects.get(year=year, region=region, parameter=parameter)
            weather.delete()
            return Response(status=status.HTTP_202_ACCEPTED)
        except SeasonsalData.DoesNotExist:
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