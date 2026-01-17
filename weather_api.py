import requests
import sys

BASE_URL = "https://api.open-meteo.com/v1/forecast"

LOCATIONS = {
    "london" : {"lat" : 51.5074, "lon" : -0.1278},
    "new york" : {"lat" : 40.7128, "lon" : -74.0068},
    "tokyo" : {"lat": 35.6762, "lon": 139.6503},
    "johannesburg" : {"lat": -26.2041, "lon" : 28.0473},
    "soweto" : {"lat" : -26.2661, "lon" : 27.8659},
    "cape town": {"lat" : -33.9249, "lon" : 18.4241} 
}

def get_weather(city_name):
    
    city_key = city_name.lower()
    if city_key not in LOCATIONS:
        print(f"Error: sorry, coordinates for '{city_name}' are not found.")
        print(f"Available cities: {', '.join(LOCATIONS.keys()).title()}")
        
        return None
    
    coords = LOCATIONS[city_key]
    
    
    params = {
        "latitude": coords["lat"],
        "longitude": coords["lon"],
        "current_weather": "true"
    }
    
    try:
        print(f"Fetching waether for {city_name.title()}...")
        response = requests.get(BASE_URL, params=params, timeout=5)
        
        response.raise_for_status()
        data = response.json()
        
        return data['current_weather']
    
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP Error occured: {http_err}")
    except requests.exceptions.ConnectionError:
        print("Error: Unable to connect to the internet.")
    except requests.exceptions.Timeout:
        print(f"Error: The request timed out")
    except requests.exceptions.RequestException as err:
        print(f"An unexpected error occured")
        
    return None

def display_weather(city, weather_data):
    if not weather_data:
        return 
    temperature = weather_data.get('temperature')
    windspeed =  weather_data.get('windspeed')
    
    print("\n" + "="*30)
    print(f" 🌤️ WEATHER REPORT: {city.upper()}")
    print("="*30)
    print(f"Temperature:  {temperature}°C")
    print(f"Wind speed: {windspeed} km/h")
    print("="*30 + "\n")
    
def main():
    print("------------------------------")
    print("         WEATHER APP"          )
    print("------------------------------")
    
    while True:
        user_input = input("Enter a city name (or 'q' to quit)").strip()
        
        if user_input.lower() == 'q':
            print("Exiting program...")
            break
        if not user_input:
            continue
        
        weather = get_weather(user_input)
        
        if weather:
            display_weather(user_input, weather)
            
if __name__ == "__main__":
    main()