import graphene
from graphene_django import DjangoObjectType

from weather_api.models import MonthlyData, Region, Parameter, Month,Season
from weather_api.web_scrapper.get_data import get_data


class MonthDataType(DjangoObjectType):
    class Meta:
        model = MonthlyData


class RegionType(DjangoObjectType):
    class Meta:
        model = Region

class ParameterType(DjangoObjectType):
    class Meta:
        model = Parameter

class MonthType(DjangoObjectType):
    class Meta:
        model = Month

class SeasonType(DjangoObjectType):
    class Meta:
        model = Season

class Query(graphene.ObjectType):
    all_regions = graphene.List(RegionType)
    all_parameters = graphene.List(ParameterType)
    all_months = graphene.List(MonthType)
    all_seasons = graphene.List(SeasonType)
    monthData = graphene.List(MonthDataType, region = graphene.String(),
                              parameter = graphene.String(),
                              month = graphene.String(),
                              year = graphene.Int())
    yearlyData = graphene.List(MonthDataType, region = graphene.String(),
                              parameter = graphene.String(),
                              year = graphene.Int())

    def resolve_all_regions(self, info):
        return Region.objects.all()

    def resolve_all_parameters(self, info):
        return Parameter.objects.all()

    def resolve_all_months(self, info):
        return Month.objects.all()

    def resolve_all_seasons(self, info):
        return Season.objects.all()
    
    def resolve_monthData(self, info, **kwargs):
        try:
            return (MonthlyData.objects.get(year = kwargs["year"], month__name=kwargs["month"], 
                                                    region__name=kwargs["region"], 
                                                    parameter__name = kwargs["parameter"]))
        except (MonthlyData.DoesNotExist,Region.DoesNotExist, Parameter.DoesNotExist):
            get_data(kwargs["region"], kwargs["parameter"])
            return (MonthlyData.objects.get(year = kwargs["year"], month__name=kwargs["month"], 
                                                    region__name=kwargs["region"], 
                                                    parameter__name = kwargs["parameter"]))
    

    def resolve_yearlyData(self, info, **kwargs):
        climate = (MonthlyData.objects.filter(year=kwargs["year"], 
                                                region__name=kwargs["region"], 
                                                parameter__name = kwargs["parameter"])
                                        .order_by('year'))
        if not climate.exists():
            get_data(kwargs["region"], kwargs["parameter"])
            climate = (MonthlyData.objects.filter(year=kwargs["year"], 
                                                region__name=kwargs["region"], 
                                                    parameter__name = kwargs["parameter"])
                                        .order_by('year'))
        return climate