from django.db.utils import IntegrityError
from django.conf import settings
import re
import csv
import io
import os
import requests
import time
import pandas as pd
from web_scrapper.models import WeatherData

class ExtractData:
    url = "https://www.metoffice.gov.uk/pub/data/weather/uk/climate/datasets"
    
    def __init__(self) -> None:
        self.data=""
        self.region="UK"
        self.parameter="Max temp"
        self.file_path = os.path.join(settings.BASE_DIR,"scrapped_data.csv")       
    
    @staticmethod
    def make_region(region):
        if "&" in region.split(" "):
            region = region.replace("&","and")
        return region
        
        
    
    def select_and_get_data(self, region="UK", parameter="Max_temp"):
        parameter_dict = {
            "Max_temp": "Tmax",
            "Min_temp": "Tmin",
            "Mean_temp": "Tmean",
            "Sunshine":"Sunshine",
            "Rainfall":'Rainfall',
            "Rain_days_1.0mm":"Raindays1mm",
            "Days_of_Air_Frost": "AirFrost"
           }
        self.region = region
        self.parameter = parameter
        print(region, parameter)
        updated_region = ExtractData.make_region(region)
        updated_parameter = parameter_dict.get(parameter, None)
        if updated_parameter is None or updated_region is None:
            raise ValueError("Invalid parameter or region passed")
        extraction_url = f"{ExtractData.url}/{updated_parameter}/date/{updated_region}.txt"
        page = requests.get(extraction_url)
        self.data = page.text
        
    def parse_data(self):
        # Create a file-like object from the CSV string
        csv_file = io.StringIO(self.data)
        # Create a CSV reader object
        reader = csv.reader(csv_file)
        file_path = settings.BASE_DIR
        
        with open(os.path.join(file_path,"scrapped_data.csv"), "w") as f:
            flag = False
            for row in reader:
                if re.search(r'year\s+jan\s+feb\s+mar\s+', row[0]) or flag == True:
                    flag=True
                    data = re.split(r"\s+",row[0])
                    f.write(','.join(data))
                    f.write('\n')
    
    def rename_cols(self):
        actual_data =pd.read_csv(self.file_path, delimiter=",",index_col=None)
        actual_data.rename(columns={"win":"winter","spr":"spring","aut":"autmn","sum":"summer"}, inplace=True)
        replacements = {"---":0.0, "NaN":0.0,'':0.0}
        actual_data.replace(replacements,inplace=True)
        actual_data.fillna(0.0, inplace=True)
        actual_data.to_csv(self.file_path, index=False)
        
    def insert_data(self):
        self.rename_cols()
        with open(self.file_path, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                region = self.region
                parameter = self.parameter
                year = int(row['year'])
                jan =  float(row['jan'])
                feb =  float(row['feb'])
                mar =  float(row['mar'])
                apr =  float(row['apr'])
                may =  float(row['may'])
                jun =  float(row['jun'])
                jul =  float(row['jul'])
                aug =  float(row['aug'])
                sep =  float(row['sep'])
                oct =  float(row['oct'])
                nov =  float(row['nov'])
                dec =  float(row['dec'])
                winter = float(row['winter'])
                summer = float(row['summer'])
                autmn = float(row['autmn'])
                spring = float(row['spring'])
                # Create a new model instance
                try:
                    model_instance = WeatherData(region = region, parameter = parameter,year=year,
                                                jan=jan, feb=feb, mar=mar, apr=apr,may=may,jun=jun,jul=jul,aug=aug,sep=sep,
                                                oct=oct,nov=nov,dec=dec, winter=winter,summer=summer, autmn=autmn, spring=spring)

                    # Save the model instance to the database
                    model_instance.save()
                except IntegrityError as e:
                    pass                    
        # delete the scrapped file
        os.remove(self.file_path)
        self.file_path=""
