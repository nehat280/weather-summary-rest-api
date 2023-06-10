from rest_framework import serializers
from weather_api.models import WeatherData

class WeatherDataSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = WeatherData
        fields= "__all__"
        
        
class YearlyWeatherDataSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = WeatherData
        fields= ('year',"jan", "feb","mar","apr","may","jun","jul","aug","sep",
                 "oct","nov","dec","winter","summer","spring","autmn","annual",)
        
        