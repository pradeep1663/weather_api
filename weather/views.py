from django.shortcuts import render
import requests
from datetime import datetime, timedelta

API_KEY = "61a26b4f4ac9aa51dca9c48e5480e39a"

icons = {
    "Clear": "clear.png",
    "Clouds": "clouds.png",
    "Rain": "rain.png",
    "Drizzle": "drizzle.png",
    "Mist": "mist.png",
}

def home(request):

    context = {}

    city = request.GET.get("city")

    if city:

        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

        response = requests.get(url)
        data = response.json()

        if response.status_code == 200:

            condition = data["weather"][0]["main"]

            #to get the timezone
            timezone_offset = data["timezone"]

            # UTC time present
            utc_time = datetime.utcnow()

            # Converting utc to local time
            city_time = utc_time + timedelta(seconds=timezone_offset)

            # Format date and time
            formatted_time = city_time.strftime("%A, %d %b %Y | %I:%M %p")

            context = {
                "city": data["name"],
                "temp": round(data["main"]["temp"]),
                "humidity": data["main"]["humidity"],
                "wind": round(data["wind"]["speed"], 2),
                "description": data["weather"][0]["description"].title(),
                "icon": icons.get(condition, "clear.png"),
                "date": formatted_time,
            }

        else:
            context["error"] = "Invalid City Name"

    return render(request, "index.html", context)