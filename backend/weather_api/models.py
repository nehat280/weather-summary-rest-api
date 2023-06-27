from django.db import models

## one specific region can have multiple data objects based on parameter, year.
class Region(models.Model):
    name = models.CharField(max_length=50, unique=True)
    
class Parameter(models.Model):
    parameter_name = models.CharField(max_length=50, unique=True)


#a weatherdata can have multiple regions hence region model is made.
class MonthlyData(models.Model):
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    parameter = models.ForeignKey(Parameter, on_delete=models.CASCADE)
    year = models.IntegerField(null=False)
    month_name= models.CharField(max_length=50)
    monthly_data = models.FloatField(null=True)
    annual_data = models.FloatField(null=True)

    class Meta:
        unique_together = ('region', 'parameter','year','month_name')
    
class AnnualData(models.Model):
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    parameter = models.ForeignKey(Parameter, on_delete=models.CASCADE)
    year = models.IntegerField(null=False)
    annual_data = models.FloatField(null=True)

    class Meta:
        unique_together = ('region', 'parameter','year')
    
    
class SeasonsalData(models.Model):
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    parameter = models.ForeignKey(Parameter, on_delete=models.CASCADE)
    year = models.IntegerField(null=False)
    season_name = models.CharField(max_length=20)
    seasonal_data = models.FloatField(null=True)

    class Meta:
        unique_together = ('region', 'parameter','year','season_name')

    