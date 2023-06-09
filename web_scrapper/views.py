from django.shortcuts import render
from django.http import HttpResponse
from web_scrapper.scrap_data import ExtractData

# Create your views here.
def get_data(request, region, parameter):
    scrap = ExtractData()
    scrap.select_and_get_data(region,parameter)
    scrap.parse_data()
    scrap.insert_data()
    response = HttpResponse("OK", status=200)
    return response
    
