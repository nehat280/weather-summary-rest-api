from django.contrib import admin
from weather_api.models import WeatherData
# Register your models here.
class WeatherDataAdmin(admin.ModelAdmin):
    list_display = ('year','region','parameter','annual')
    
admin.site.register(WeatherData, WeatherDataAdmin)