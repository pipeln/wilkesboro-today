#!/usr/bin/env python3
"""
Weather Update Agent
Fetches weather data and updates website twice daily
"""

import os
import json
import requests
from datetime import datetime
from config import config

# Wilkesboro, NC coordinates
LAT = 36.1585
LON = -81.1526

def fetch_weather():
    """Fetch weather from Open-Meteo (free, no API key needed)."""
    try:
        url = f"https://api.open-meteo.com/v1/forecast?latitude={LAT}&longitude={LON}&current=temperature_2m,relative_humidity_2m,apparent_temperature,weather_code,wind_speed_10m&daily=temperature_2m_max,temperature_2m_min,weather_code&timezone=America/New_York&forecast_days=5"
        
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            
            # Map weather codes to conditions
            weather_codes = {
                0: 'Clear sky',
                1: 'Mainly clear', 2: 'Partly cloudy', 3: 'Overcast',
                45: 'Foggy', 48: 'Depositing rime fog',
                51: 'Light drizzle', 53: 'Moderate drizzle', 55: 'Dense drizzle',
                61: 'Slight rain', 63: 'Moderate rain', 65: 'Heavy rain',
                71: 'Slight snow', 73: 'Moderate snow', 75: 'Heavy snow',
                95: 'Thunderstorm', 96: 'Thunderstorm with hail'
            }
            
            current = data.get('current', {})
            daily = data.get('daily', {})
            
            weather_data = {
                'location': 'Wilkesboro, NC',
                'last_updated': datetime.now().isoformat(),
                'current': {
                    'temperature': current.get('temperature_2m'),
                    'feels_like': current.get('apparent_temperature'),
                    'humidity': current.get('relative_humidity_2m'),
                    'wind_speed': current.get('wind_speed_10m'),
                    'condition': weather_codes.get(current.get('weather_code'), 'Unknown')
                },
                'forecast': []
            }
            
            # Build 5-day forecast
            for i in range(5):
                weather_data['forecast'].append({
                    'date': daily.get('time', [])[i] if i < len(daily.get('time', [])) else None,
                    'high': daily.get('temperature_2m_max', [])[i] if i < len(daily.get('temperature_2m_max', [])) else None,
                    'low': daily.get('temperature_2m_min', [])[i] if i < len(daily.get('temperature_2m_min', [])) else None,
                    'condition': weather_codes.get(daily.get('weather_code', [])[i], 'Unknown') if i < len(daily.get('weather_code', [])) else 'Unknown'
                })
            
            return weather_data
            
    except Exception as e:
        print(f"Error fetching weather: {e}")
    
    return None


def save_weather(weather_data):
    """Save weather data to website data directory."""
    if not weather_data:
        return False
    
    data_dir = config.ASTRO_BUILD_DIR + '/src/data'
    os.makedirs(data_dir, exist_ok=True)
    
    filepath = os.path.join(data_dir, 'weather.json')
    with open(filepath, 'w') as f:
        json.dump(weather_data, f, indent=2)
    
    print(f"✅ Weather saved to {filepath}")
    return True


def main():
    print("="*60)
    print("WEATHER UPDATE AGENT")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)
    
    weather = fetch_weather()
    
    if weather:
        print(f"\nCurrent Conditions:")
        print(f"  Location: {weather['location']}")
        print(f"  Temperature: {weather['current']['temperature']}°F")
        print(f"  Feels Like: {weather['current']['feels_like']}°F")
        print(f"  Condition: {weather['current']['condition']}")
        print(f"  Humidity: {weather['current']['humidity']}%")
        print(f"  Wind: {weather['current']['wind_speed']} mph")
        
        print(f"\n5-Day Forecast:")
        for day in weather['forecast'][:5]:
            print(f"  {day['date']}: High {day['high']}°F / Low {day['low']}°F - {day['condition']}")
        
        save_weather(weather)
        print("\n✅ Weather update complete!")
    else:
        print("\n❌ Failed to fetch weather data")


if __name__ == "__main__":
    main()
