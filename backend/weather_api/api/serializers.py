from rest_framework import serializers
from weather_api.models import WeatherData

class WeatherDataSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = WeatherData
        fields= "__all__"
        