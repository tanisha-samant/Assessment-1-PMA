from flask import Flask, render_template, request, jsonify
from datetime import datetime, timedelta
import requests
import logging

app = Flask(__name__)

# Set up logging
logging.basicConfig(level=logging.DEBUG)

# Validate location using OpenWeatherMap Geocoding API
def validate_location(location):
    api_key = "0314a6f2ab0167a2a1788b159ebbfacd"  # Replace with your API key
    app.logger.debug(f"Validating location: {location}")

    # Handle coordinates input (e.g., "40.7128,-74.0060")
    if ',' in location:
        try:
            lat, lon = map(float, location.split(','))
            # Validate latitude and longitude ranges
            if -90 <= lat <= 90 and -180 <= lon <= 180:
                # Use reverse geocoding to get city name
                url = f"http://api.openweathermap.org/geo/1.0/reverse?lat={lat}&lon={lon}&limit=1&appid={api_key}"
                app.logger.debug(f"Reverse geocoding URL: {url}")
                try:
                    response = requests.get(url, timeout=5)
                    response.raise_for_status()  # Raise exception for bad status codes
                    data = response.json()
                    app.logger.debug(f"Reverse geocoding response: {data}")
                    if data and len(data) > 0:
                        return lat, lon, data[0]['name'] or "Unknown Location", None
                    return None, None, None, "No location found for coordinates"
                except requests.RequestException as e:
                    app.logger.error(f"Reverse geocoding error: {str(e)}")
                    return None, None, None, f"Reverse geocoding failed: {str(e)}"
            return None, None, None, "Invalid coordinate range"
        except ValueError as e:
            app.logger.error(f"Coordinate parsing error: {str(e)}")
            return None, None, None, "Invalid coordinate format"
    
    # Handle city or ZIP code input
    url = f"http://api.openweathermap.org/geo/1.0/direct?q={location}&limit=1&appid={api_key}"
    app.logger.debug(f"Direct geocoding URL: {url}")
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        app.logger.debug(f"Direct geocoding response: {data}")
        if data and len(data) > 0:
            return data[0]['lat'], data[0]['lon'], data[0]['name'], None
        return None, None, None, "Location not found"
    except requests.RequestException as e:
        app.logger.error(f"Direct geocoding error: {str(e)}")
        return None, None, None, f"Geocoding failed: {str(e)}"

# Fetch weather data from Open-Meteo
def fetch_weather(lat, lon):
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m,weather_code,precipitation_probability&forecast_days=5"
    app.logger.debug(f"Fetching weather data: {url}")
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        app.logger.error(f"Weather API error: {str(e)}")
        return None

# Home route
@app.route('/')
def index():
    return render_template('index.html')

# Get current weather and 5-day forecast
@app.route('/weather', methods=['POST'])
def get_weather():
    location = request.form.get('location')
    lat, lon, city_name, error = validate_location(location)
    if not lat or not lon:
        app.logger.error(f"Invalid location: {location}, Error: {error}")
        return jsonify({'error': error or 'Invalid location'}), 400
    
    # Fetch weather data
    weather_data = fetch_weather(lat, lon)
    if not weather_data:
        app.logger.error(f"Failed to fetch weather data for {lat}, {lon}")
        return jsonify({'error': 'Failed to fetch weather data'}), 500
    
    return jsonify({
        'city': city_name,
        'weather': weather_data['hourly'],
        'latitude': lat,
        'longitude': lon
    })

if __name__ == '__main__':
    app.run(debug=True)