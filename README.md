# Assessment-1
# Weather App

## Overview
This is a Flask-based web application that provides current weather information and a 5-day forecast for a specified location. Users can input a city name, ZIP code, or coordinates (latitude, longitude) to retrieve weather data. The app also supports fetching the user's current location using the browser's geolocation API.

## Features
- **Location Input**: Enter a city name, ZIP code, or coordinates to get weather data.
- **Geolocation Support**: Use the browser's geolocation to automatically fetch weather for the user's current location.
- **Weather Data**: Displays current temperature, humidity, wind speed, and precipitation probability, along with a 5-day forecast.
- **Responsive Design**: Built with Bootstrap for a mobile-friendly interface.
- **Error Handling**: Provides user-friendly error messages for invalid inputs or API failures.
- **Weather Icons**: Displays icons based on weather conditions using OpenWeatherMap icons.

## Tech Stack
- **Backend**: Flask (Python)
- **Frontend**: HTML, CSS (Bootstrap), JavaScript
- **APIs**:
  - **OpenWeatherMap Geocoding API**: For validating and converting locations to coordinates.
  - **Open-Meteo API**: For retrieving weather data.
- **Dependencies**:
  - Flask
  - Requests
  - Bootstrap 5.3.0
  - Font Awesome 6.4.0

## Setup Instructions

### Prerequisites
- Python 3.8+
- pip (Python package manager)
- An OpenWeatherMap API key (sign up at [openweathermap.org](https://openweathermap.org/) to get one)

