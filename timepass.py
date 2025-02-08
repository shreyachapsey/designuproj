import requests
import time
from plyer import notification
from datetime import datetime, timedelta

# OpenWeatherMap API Key (Replace with your own key)
API_KEY = ""
CITY = "Minneapolis"

# Fetch weather data
def get_weather():
    url = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        temp = data['main']['temp']
        weather = data['weather'][0]['main']
        return temp, weather
    else:
        return None, None

# Provide clothing recommendation
def get_clothing_recommendation(temp, weather):
    if temp is None:
        return "Unable to fetch weather data."
    
    if temp < 5:
        recommendation = "It's very cold! Wear a thick jacket, gloves, and a scarf."
    elif 5 <= temp < 15:
        recommendation = "It's chilly. Wear a sweater and a light jacket."
    elif 15 <= temp < 25:
        recommendation = "The weather is moderate. A t-shirt and jeans should be fine."
    else:
        recommendation = "It's hot! Wear shorts and a light t-shirt."
    
    if "rain" in weather.lower():
        recommendation += " Also, carry an umbrella!"
    elif "snow" in weather.lower():
        recommendation += " Wear boots and warm clothing."
    
    return recommendation

# Send desktop notification
def send_notification(message):
    notification.notify(
        title="Weather Outfit Recommendation",
        message=message,
        timeout=10
    )

# Function to wait until 7 AM
def wait_until_morning():
    now = datetime.now()
    next_run = datetime.combine(now.date(), datetime.min.time()) + timedelta(days=1, hours=7)
    if now.hour >= 7:  # If it's already past 7 AM, schedule for next day
        next_run += timedelta(days=1)
    
    wait_time = (next_run - now).total_seconds()
    print(f"Waiting {int(wait_time)} seconds until 7 AM...")
    time.sleep(wait_time)

def main():
    while True:
        temp, weather = get_weather()
        message = get_clothing_recommendation(temp, weather)
        send_notification(message)
        
        # Wait until 7 AM the next day
        wait_until_morning()

if __name__ == "__main__":
    main()
