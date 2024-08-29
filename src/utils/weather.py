import requests
from config import API_KEY

def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return {
            "temp": data['main']['temp'],
            "feels_like": data['main']['feels_like'],
            "description": data['weather'][0]['description'],
            "icon": data['weather'][0]['icon'],
            "humidity": data['main']['humidity'],
            "wind_speed": data['wind']['speed'],
           
        }
    else:
        return None

def get_forecast(city):
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        forecast_list = []
        for entry in data['list']:
            forecast_list.append({
                "datetime": entry['dt_txt'],
                "temp": entry['main']['temp'],
                "description": entry['weather'][0]['description'],
                "icon": entry['weather'][0]['icon']
            })
        return forecast_list
    else:
        return None
def get_alerts(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        alerts = data.get('alerts', [])
        return alerts
    else:
        return None
def get_clothing_recommendations(temp, description, wind_speed):
    recommendations = []

    # Temperature-based recommendations
    if temp > 30:
        recommendations.append("Wear light and breathable clothing (e.g., t-shirt, shorts).")
        recommendations.append("Stay hydrated and avoid direct sunlight.")
    elif 20 <= temp <= 30:
        recommendations.append("Wear comfortable clothing (e.g., t-shirt, jeans).")
    elif 10 <= temp < 20:
        recommendations.append("Wear a light jacket or sweater.")
    elif 0 <= temp < 10:
        recommendations.append("Wear a warm jacket, scarf, and gloves.")
    else:
        recommendations.append("Wear heavy winter clothing, including a coat, hat, gloves, and scarf.")
        recommendations.append("Consider layering up to stay warm.")

    # Weather condition-based recommendations
    if "rain" in description.lower():
        recommendations.append("Carry an umbrella or wear a raincoat.")
        recommendations.append("Wear waterproof footwear.")
    elif "snow" in description.lower():
        recommendations.append("Wear snow boots and a warm hat.")
        recommendations.append("Consider wearing layers to stay warm.")

    # Wind speed-based recommendations
    if wind_speed > 15:
        recommendations.append("It's windy, so wear something windproof.")
    
    return recommendations
