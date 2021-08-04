from django.shortcuts import render
from decouple import config
import requests
from pprint import pprint
from .models import City
from .forms import CityForm
from django.contrib import messages

# Create your views here.
def index(request):
    form = CityForm(request.POST or None)
    cities = City.objects.all()
    url = config('BASE_URL')
    # city = 'Berlin'
    # response = requests.get(url.format(city))
    # content = response.json()
    # pprint(content)
    # print(type(content))
    

    if form.is_valid():
        n_city = form.cleaned_data["name"]
        if not City.objects.filter(name=n_city).exists():
            r = requests.get(url.format(n_city))
            if r.status_code == 200:
                form.save()
            else:
                messages.warning(request, "City does not exists.")
        else:
            messages.warning(request, "City already exists.")
    city_data = []
    for city in cities:
        print(city)
        response = requests.get(url.format(city))
        content = response.json()
        pprint(content)
        data = {
            'city' : city.name,
            'temprature' : content['main']['temp'],
            'description' : content['weather'][0]['description'],
            'icon' : content['weather'][0]['icon']
        }
        city_data.append(data)
    print(city_data)
    context = {
        'city_data': city_data,
        'form' : form
    }
    return render(request, 'weather_api/index.html', context)