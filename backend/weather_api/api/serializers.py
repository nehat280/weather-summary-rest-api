from rest_framework import serializers
from weather_api.models import MonthlyData, SeasonsalData, AnnualData

class MonthlyDataSerializer(serializers.ModelSerializer):
    value = serializers.FloatField(source="monthly_data")
    class Meta:
        model = MonthlyData
        fields = ['region','parameter','year','month_name','value']
        

class AnnualDataSerializer(serializers.ModelSerializer):
    value = serializers.FloatField(source="annual_data")
    class Meta:
        model = AnnualData
        fields = ['region','parameter','year','annual_data']
        
        
class SeasonsalDataSerializer(serializers.ModelSerializer):
    value = serializers.FloatField(source="seasonal_data")
    class Meta:
        model = SeasonsalData
        fields= ['region','parameter','year','season_name','value']
        
        