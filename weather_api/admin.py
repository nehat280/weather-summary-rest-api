from django.contrib import admin
from django.urls import reverse

from weather_api.models import Region, Parameter, MonthlyData, SeasonsalData, AnnualData
from weather_api.models import Season, Month
from django.utils.html import format_html

def create_link(obj,object_name):
    
    id = getattr(getattr(obj, object_name),'id')
    url = (
        reverse(f"admin:weather_api_{object_name}_change"
        ,args=(id,)
        ))    
    return format_html('<a href="{}">{}</a>', url, getattr(getattr(obj, object_name),'name'))
    


class RegionAdmin(admin.ModelAdmin):
    list_display = ('name',)

class ParameterAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_filter = ("name", )


class SeasonAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_filter = ("name", )


class MonthAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_filter = ("name", )


class MonthlyDataAdmin(admin.ModelAdmin):
    list_display = ('region','show_parameter_url','year','show_month_url','value')
    list_filter = ("region","parameter","month","year")

    def show_month_url(self, obj):
        return create_link(obj, "month")
    show_month_url.short_description = "Month"

    def show_parameter_url(self, obj):
        return create_link(obj,'parameter')
    show_parameter_url.short_description = "Parameter"
    
class SeasonalDataAdmin(admin.ModelAdmin):
    list_display = ('region','parameter','year','show_season_url','value')
    list_filter = ("region","parameter","season")
    
    def show_season_url(self, obj):
        return create_link(obj,'season')
    show_season_url.short_description = "Season"

class AnnualDataAdmin(admin.ModelAdmin):
    list_display = ('region','parameter','year','annual_data')
    list_filter = ("region","parameter","year")
    

admin.site.register(Region,RegionAdmin)
admin.site.register(Parameter, ParameterAdmin)
admin.site.register(MonthlyData, MonthlyDataAdmin)
admin.site.register(SeasonsalData, SeasonalDataAdmin)
admin.site.register(AnnualData, AnnualDataAdmin)
admin.site.register(Season, SeasonAdmin)
admin.site.register(Month, MonthAdmin)
