import traceback
from weather_api.web_scrapper.scrap_data import ExtractData

# Create your views here.
def get_data(region, parameter):
    try:
        scrap = ExtractData(region,parameter)
        scrap.select_and_get_data()
        scrap.parse_data()
        scrap.data_cleaning()
        scrap.insert_data()
        return True

    except:
        traceback.print_exc()
        return False
    
    
