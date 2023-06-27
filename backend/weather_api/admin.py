from django.contrib import admin
from weather_api.models import Region, Parameter, MonthlyData, SeasonsalData, AnnualData

# class WeatherDataAdmin(admin.ModelAdmin):
#     list_display = ('year','region','parameter','annual')
    
admin.site.register(Region)
admin.site.register(Parameter)
admin.site.register(MonthlyData)
admin.site.register(SeasonsalData)
admin.site.register(AnnualData)
