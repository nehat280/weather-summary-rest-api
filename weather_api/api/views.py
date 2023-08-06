from django.db.models import Avg
from django.db.models.functions import Round
from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated

from weather_api.models import Region, Parameter, MonthlyData, SeasonsalData,AnnualData
from weather_api.api.serializers import MonthlyDataSerializer,YearlyDataSerializer,AnnualDataSerializer, SeasonsalDataSerializer,DictionarySerializer
from weather_api.web_scrapper.get_data import get_data
from weather_api.web_scrapper.Constants import PARAMETERS, REGIONS, MONTHS
from rest_framework import generics

class ValidInputsMixin:
    def dispatch(self, request, *args, **kwargs):
        if not self.is_valid_inputs(request, *args, **kwargs):
            raise Http404("Invalid Inputs")
    
        return super().dispatch(request, *args, **kwargs)

    def is_valid_inputs(self, request, *args, **kwargs):
        region = kwargs.get("region")
        parameter = kwargs.get("parameter")
        month = kwargs.get("month",None)

        if region not in REGIONS:
            return False
        if parameter not in PARAMETERS:
            return False
        if month is not None and month not in MONTHS:
            return False
        
        return True

    
class MonthlyDataView(ValidInputsMixin, generics.RetrieveAPIView):
    queryset = MonthlyData.objects.all()
    serializer_class = MonthlyDataSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        region = self.kwargs["region"]
        parameter = self.kwargs["parameter"]
        year = self.kwargs["year"]
        month = self.kwargs["month"]

        try:
            return get_object_or_404(MonthlyData,year = year, month__name=month, 
                                                  region__name=region, 
                                                  parameter__name = parameter)
        except (MonthlyData.DoesNotExist,Region.DoesNotExist, Parameter.DoesNotExist):
            get_data(region, parameter)
            data = get_object_or_404(MonthlyData,year = year, month__name=month, 
                                                  region__name=region, 
                                                  parameter__name = parameter)

            return data



class AverageDataView(ValidInputsMixin, generics.ListAPIView):
    serializer_class = DictionarySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        region = self.kwargs["region"]
        parameter = self.kwargs["parameter"]

        filtered_weather = (MonthlyData.objects
                                    .filter(region__name=region, parameter__name=parameter))
        
        if not filtered_weather.exists():
            get_data(region, parameter)
            filtered_weather = (MonthlyData.objects
                                    .filter(region__name=region, parameter__name=parameter))
            
        averages = (filtered_weather.values('region', 'parameter', 'month__name')
                                .annotate(avg_month_value=Round(Avg('value'),2)))
        return averages


class YearlyDataView(ValidInputsMixin, generics.ListAPIView):
    serializer_class = YearlyDataSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        region = self.kwargs["region"]
        parameter = self.kwargs["parameter"]
        year = self.kwargs['year']

        climate = (MonthlyData.objects.filter(year=year, 
                                                region__name=region,
                                                parameter__name=parameter)
                                        .order_by('year'))
        if not climate.exists():
            get_data(region, parameter)
            climate = (MonthlyData.objects.filter(year=year, 
                                                region__name=region,
                                                parameter__name=parameter)
                                        .order_by('year'))
        return climate
    

class SeasonalDataView(ValidInputsMixin, generics.ListAPIView):
    serializer_class = SeasonsalDataSerializer

    def get_queryset(self):
        region = self.kwargs["region"]
        parameter = self.kwargs["parameter"]
        year = self.kwargs['year']
        climate = SeasonsalData.objects.filter(year=year, 
                                               region__name=region,
                                               parameter__name=parameter)

        if not climate.exists():
            get_data(region, parameter)
            climate = SeasonsalData.objects.filter(year=year, 
                                                   region__name=region, 
                                                   parameter__name=parameter)
        return climate


#inserting data not implemented
class AnnualDataView(ValidInputsMixin, generics.RetrieveAPIView):
    serializer_class = AnnualDataSerializer

    def get_object(self):
        region = self.kwargs["region"]
        parameter = self.kwargs["parameter"]
        year = self.kwargs['year']

        climate = AnnualData.objects.filter(year=year, 
                                               region__name=region,
                                               parameter__name=parameter)

        if not climate.exists():
            get_data(region, parameter)
            climate = AnnualData.objects.filter(year=year, 
                                                   region__name=region, 
                                                   parameter__name=parameter)
        return climate