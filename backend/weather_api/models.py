from django.db import models


class WeatherData(models.Model):
    region = models.CharField(max_length=50, null=False)
    parameter = models.CharField(max_length=50, null=False)
    year = models.IntegerField(default=0,null=False)
    jan= models.FloatField(default=0,null=True)
    feb= models.FloatField(default=0,null=True)
    mar= models.FloatField(default=0,null=True)
    apr= models.FloatField(default=0,null=True)
    may= models.FloatField(default=0,null=True)
    jun= models.FloatField(default=0,null=True)
    jul= models.FloatField(default=0,null=True)
    aug= models.FloatField(default=0,null=True)
    sep = models.FloatField(default=0,null=True)
    oct= models.FloatField(default=0,null=True)
    nov= models.FloatField(default=0,null=True)
    dec= models.FloatField(default=0,null=True)
    winter = models.FloatField(default=0,null=True)
    summer = models.FloatField(default=0,null=True)
    autmn= models.FloatField(default=0,null=True)
    spring = models.FloatField(default=0,null=True)
    annual = models.FloatField(default=0,null=True)
    
    def __str__(self) -> str:
        return str(self.year)
        
    class Meta:
        unique_together = ('region', 'parameter','year')
    