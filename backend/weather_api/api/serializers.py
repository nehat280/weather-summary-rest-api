from rest_framework import serializers
from weather_api.models import MonthlyData, SeasonsalData, AnnualData, Region, Parameter, Month

class MonthlyDataSerializer(serializers.ModelSerializer):

    class Meta:
        model = MonthlyData
        fields = ['region','parameter','year','month','value']

class DictionarySerializer(serializers.Serializer):
    region = serializers.CharField(max_length=200)
    month__name = serializers.CharField(max_length=200)
    parameter = serializers.CharField(max_length=200)
    avg_month_value = serializers.FloatField()

class AnnualDataSerializer(serializers.ModelSerializer):
    value = serializers.FloatField(source="annual_data")
    class Meta:
        model = AnnualData
        fields = ['region','parameter','year','annual_data']
        
        
class SeasonsalDataSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = SeasonsalData
        fields= ['region','parameter','year','season','value']
        