from django.db import models

## one specific region can have multiple data objects based on parameter, year.
class Region(models.Model):
    name = models.CharField(max_length=50, unique=True)
    
    def __str__(self):
        return self.name


class Parameter(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Month(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Season(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


#a weatherdata can have multiple regions hence region model is made.
class MonthlyData(models.Model):
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    parameter = models.ForeignKey(Parameter, on_delete=models.CASCADE)
    year = models.IntegerField(null=False)
    month = models.ForeignKey(Month, on_delete=models.CASCADE)
    value = models.FloatField(null=True)

    class Meta:
        verbose_name_plural = "Monthly Data"
        unique_together = ('region', 'parameter','year','month')
    
class AnnualData(models.Model):
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    parameter = models.ForeignKey(Parameter, on_delete=models.CASCADE)
    year = models.IntegerField(null=False)
    annual_data = models.FloatField(null=True)

    class Meta:
        verbose_name_plural = "Annual Data"
        unique_together = ('region', 'parameter','year')
    
    
class SeasonsalData(models.Model):
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    parameter = models.ForeignKey(Parameter, on_delete=models.CASCADE)
    year = models.IntegerField(null=False)
    season = models.ForeignKey(Season, on_delete=models.CASCADE)
    value = models.FloatField(null=True)

    class Meta:
        verbose_name_plural = "Seasonal Data"
        unique_together = ('region', 'parameter','year','season')

    