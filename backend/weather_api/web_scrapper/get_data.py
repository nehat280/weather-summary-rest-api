import traceback
from weather_api.web_scrapper.scrap_data import ExtractData


def get_data(region, parameter):
    try:
        scrap = ExtractData(region,parameter)
        scrap.select_and_get_data()
        scrap.parse_data()
        scrap.data_cleaning()
        scrap.insert_data()
        

    except:
        traceback.print_exc()
        
    
    
