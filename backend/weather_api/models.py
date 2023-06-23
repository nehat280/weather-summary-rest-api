from django.db import models


class Region(models.Model):
    name = models.CharField(max_length=50)
    
class Parameter(models.Model):
    parameter_name = models.CharField(max_length=50, unique=True)

class Year(models.Model):
    year_name = models.IntegerField(default=0)

class Month(models.Model):
    month_name= models.CharField(max_length=50,unique=True)
    monthly_data = models.FloatField(null=True)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    parameter = models.ForeignKey(Parameter, on_delete=models.CASCADE)
    year = models.ForeignKey(Year, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ('region', 'parameter','year','month_name')
    
    
class Seasons(models.Model):
    name = models.CharField(max_length=20, unique=  True)
    data = models.FloatField(null=True)
    
    
class WeatherData(models.Model):
    pass