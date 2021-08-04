from django.shortcuts import render
from decouple import config
import requests
from pprint import pprint

# Create your views here.
def index(request):
    url = config('BASE_URL')
    city= 'Berlin'
    response = requests.get(url.format(city))
    content = response.json()
    pprint(content)
    print(type(content))
    return render(request, 'weather_api/index.html')