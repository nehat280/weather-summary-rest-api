from django.http import HttpResponse
from weather_api.web_scrapper.scrap_data import ExtractData

# Create your views here.
def get_data(region, parameter):
    try:
        scrap = ExtractData()
        scrap.select_and_get_data(region,parameter)
        scrap.parse_data()
        scrap.data_cleaning()
        scrap.insert_data()
        response = HttpResponse("OK", status=200)
    except:
        return HttpResponse("Not OK",status=400)
    return response
    
