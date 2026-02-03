from django.shortcuts import render
from django.contrib import messages
import requests
import datetime


# ================= CONFIG ================= #

WEATHER_API_KEY = "7ad7e2a85b607ffd4adfb771051df29b"

UNSPLASH_ACCESS_KEY = "fLMgFAJidDQcEgkBM7_pdWjNwGW-lvWIgf1elDCYqW4"


# ================= VIEW ================= #

def home(request):

    city = request.POST.get('city', 'Pune')

    # -------- WEATHER API -------- #

    weather_url = "https://api.openweathermap.org/data/2.5/weather"

    params = {
        'q': city,
        'appid': WEATHER_API_KEY,
        'units': 'metric'
    }

    # -------- UNSPLASH IMAGE API -------- #

    image_url = None

    unsplash_url = (
        f"https://api.unsplash.com/search/photos"
        f"?query={city} city skyline&per_page=1&client_id={UNSPLASH_ACCESS_KEY}"
    )

    try:
        img_data = requests.get(unsplash_url, timeout=5).json()
        results = img_data.get("results", [])

        if results:
            image_url = results[0]["urls"]["regular"]

    except:
        image_url = None

    # -------- WEATHER DATA -------- #

    try:
        weather_data = requests.get(weather_url, params=params, timeout=5).json()

        if weather_data.get("cod") != 200:
            raise ValueError("City not found")

        description = weather_data['weather'][0]['description']
        icon = weather_data['weather'][0]['icon']
        temp = weather_data['main']['temp']
        day = datetime.date.today()

        return render(request, 'home.html', {
            'description': description,
            'icon': icon,
            'temp': temp,
            'day': day,
            'city': city,
            'image_url': image_url,
            'exception_occurred': False
        })

    except:

        messages.error(request, "City not found — showing default weather")

        return render(request, 'home.html', {
            'description': 'clear sky',
            'icon': '01d',
            'temp': 25,
            'day': datetime.date.today(),
            'city': 'Pune',
            'image_url': image_url,
            'exception_occurred': True
        })
