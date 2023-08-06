from django.conf import settings
import re
import csv
import io
import os
import requests
import pandas as pd
import numpy as np

from contextlib import closing
from io import StringIO
from collections import defaultdict
from django.db import connection
from django.utils import timezone

from weather_api.models import Region, Parameter, Month, Season, MonthlyData, SeasonsalData
from weather_api.web_scrapper.Constants import MONTHS, SEASONS, new_columns, month_columns,  season_columns

class ExtractData:
    url = "https://www.metoffice.gov.uk/pub/data/weather/uk/climate/datasets"
    
    def __init__(self, region="UK", parameter="Tmax"):
        self.data = ""
        self.region = region
        self.parameter = parameter
        self.file_path = settings.BASE_DIR
    
    
    def select_and_get_data(self):
        extraction_url = f"{ExtractData.url}/{self.parameter}/date/{self.region}.txt"
        page = requests.get(extraction_url)
        self.data = page.text


    def parse_data(self):
        # Create a file-like object from the CSV string
        csv_file = io.StringIO(self.data)
        # Create a CSV reader object
        reader = csv.reader(csv_file)
        
        with open(os.path.join(self.file_path,"scrapped_data.csv"), "w") as f:
            flag = False
            for row in reader:
                if re.search(r'year\s+jan\s+feb\s+mar\s+', row[0]) or flag == True:
                    flag=True
                    data = re.split(r"\s+",row[0])
                    f.write(','.join(data))
                    f.write('\n')
    
    def handling_nan(self,df, groupby_on, map_column ):
        """
         Any nan values in data is replaced by the average of historical data
        """

        # below statement means -> data.groupby(['month_name']).mean(numeric_only=True).monthly_data
        aggregation_series = df.groupby(groupby_on).mean(numeric_only=True)[map_column].round(2)

        df[map_column] =  df[map_column].fillna(df[groupby_on].map(aggregation_series))
        return df

    def process_monthly_data(self, df):
        # separate monthly data
        data1 = df[month_columns].copy()
        monthly_data = pd.melt(data1,id_vars = ['year'], var_name = "month_id",value_name="value")
        monthly_data['value'] = monthly_data['value'].astype(float)
        monthly_data['year'] = monthly_data['year'].astype(int)
        monthly_data = self.handling_nan(monthly_data, "month_id", "value")
        monthly_data.to_csv(os.path.join(self.file_path,"monthly_data.csv"), index=False)

    def process_seasonal_data(self, df):
        # separating seasonal data
        data2 = df[season_columns].copy()
        seasonal_data = pd.melt(data2,id_vars = ['year'], var_name = "season_id",value_name="value")
        seasonal_data['value'] = seasonal_data['value'].astype(float)
        seasonal_data['year'] = seasonal_data['year'].astype(int)
        seasonal_data = self.handling_nan(seasonal_data, "season_id", "value")
        seasonal_data.to_csv(os.path.join(self.file_path,"seasonal_data.csv"), index=False)

    
    def data_cleaning(self):
        actual_data = pd.read_csv(os.path.join(self.file_path,"scrapped_data.csv"), delimiter=",",index_col=None)
        actual_data.rename(columns= new_columns, inplace=True)

        replacements = {"---":np.nan, "NaN":np.nan,'':np.nan}
        actual_data.replace(replacements,inplace=True)
        self.process_monthly_data(actual_data)
        self.process_seasonal_data(actual_data)
        print("data cleaning")

    @staticmethod
    def replace_name_with_ids(file_path, replacement_dict, region_id, parameter_id):
        data = pd.read_csv(file_path)
        data["region_id"] = region_id
        data["parameter_id"] = parameter_id
        data = data.replace(replacement_dict)
        data.to_csv(file_path,index=False)
        
    def bulk_insert(self, model_name, file_path):
        ids_dict = defaultdict(int)
        region,_ = Region.objects.get_or_create(name=self.region)
        parameter,_ = Parameter.objects.get_or_create(name=self.parameter)
        
        if model_name.__name__ == 'MonthlyData':
            
            for month_name in MONTHS:
                month,_ = Month.objects.get_or_create(name = month_name)
                ids_dict[month_name] = month.id
            
        else:
            for season_name in SEASONS:
                season,_ = Season.objects.get_or_create(name = season_name)
                ids_dict[season_name] = season.id
                
        ExtractData.replace_name_with_ids(file_path, ids_dict, region.id, parameter.id)
        
        f = open(file_path, 'r')
        f.readline()
        with closing(connection.cursor()) as cursor:
            if model_name.__name__ == 'MonthlyData':
                cursor.copy_from(
                    file = f,
                    table = 'weather_api_monthlydata',
                    sep = ',',
                    columns = ['year','month_id','value','region_id','parameter_id']                
                )
            else:          
                cursor.copy_from(
                    file = f,
                    table = 'weather_api_seasonsaldata',
                    sep = ',',
                    columns = ['year','season_id','value','region_id','parameter_id']                
                )
        

    def insert_data(self):
        monthly_weather_obj = (MonthlyData.objects.select_related('region')
                                                  .select_related('parameter')
                                                  .filter(region__name = self.region, parameter__name = self.parameter))
        seasonal_data_obj = (SeasonsalData.objects.select_related('region')
                                                  .select_related('parameter')
                                                  .filter(region__name = self.region, parameter__name = self.parameter))

        if not monthly_weather_obj.exists():
            self.bulk_insert(MonthlyData,os.path.join(self.file_path,"monthly_data.csv"))
        if not seasonal_data_obj.exists():
            self.bulk_insert(SeasonsalData,os.path.join(self.file_path,"seasonal_data.csv"))
        # delete the scrapped file
        for file_name in ("scrapped_data.csv","monthly_data.csv","seasonal_data.csv"):
            os.remove(os.path.join(self.file_path,file_name))
