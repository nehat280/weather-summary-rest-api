from django.http import HttpResponse
from weather_api.web_scrapper.scrap_data import ExtractData

# Create your views here.
def get_data(region, parameter):
    scrap = ExtractData()
    try:
        scrap.select_and_get_data(region,parameter)
    except ValueError:
        return HttpResponse("NOT FOUND", status=404)
    scrap.parse_data()
    scrap.insert_data()
    response = HttpResponse("OK", status=200)
    return response
    
