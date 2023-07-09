from rest_framework import serializers
from weather_api.models import MonthlyData, SeasonsalData, AnnualData

class MonthlyDataSerializer(serializers.ModelSerializer):

    class Meta:
        model = MonthlyData
        fields = ['region','parameter','year','month','value']


class DictionarySerializer(serializers.Serializer):
    region = serializers.CharField(max_length=200)
    month = serializers.CharField(source = "month__name")
    parameter = serializers.CharField(max_length=200)
    average_for_month = serializers.FloatField(source = "avg_month_value")


class AnnualDataSerializer(serializers.ModelSerializer):
    value = serializers.FloatField(source="annual_data")
    region = serializers.CharField(source="region.name")
    parameter = serializers.CharField(source="parameter.name")
    
    class Meta:
        model = AnnualData
        fields = ['region','parameter','year','value']


class YearlyDataSerializer(serializers.ModelSerializer):
    month = serializers.CharField(source="month.name")
    region = serializers.CharField(source="region.name")
    parameter = serializers.CharField(source="parameter.name")
    
    class Meta:
        model = MonthlyData
        fields = ['region','parameter','year','month','value']
        
        
class SeasonsalDataSerializer(serializers.ModelSerializer):
    season = serializers.CharField(source="season.name")
    region = serializers.CharField(source="region.name")
    parameter = serializers.CharField(source="parameter.name")
    
    class Meta:
        model = SeasonsalData
        fields= ['region','parameter','year','season','value']
        