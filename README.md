# Weather Forecast Telegram Bot


## Features
- City Weather: Get weather updates by sending the name of a city.
- Location-Based Weather:  Share your location to get weather updates for your current location (works only in the     mobile Telegram app, not in the desktop version).
- Predefined City Buttons: Quick access buttons for Berlin, London, and Kyiv.
- City Image: Provides an image of the requested city using the Unsplash API.
- Multilingual Support: Uses I18nMiddleware for internationalization.

## Prerequisites
- Python 3.x
- Telegram Bot Token
- OpenWeatherMap API Key
- Unsplash API Key

## Installation

1. ### Clone the repository
git clone git@github.com:VitaliyPryyemskyy/Weather_Forecast_Telegram_Bot.git
cd Weather_Forecast_Telegram_Bot

2. ### Configure API Keys
Open config.py and replace the placeholder values with your actual API keys.
- OpenWeatherMap API: https://openweathermap.org/api
- Unsplash API: https://unsplash.com/developers
- Telegram Bot Registration: https://docs.expertflow.com/cx/4.3/telegram-bot-creation-guide

3. ### Run the setup script in terminal
./build.sh

This script creates a virtual environment, installs necessary packages, and launches the application.

## Bot Interactions
- Predefined City Buttons: Click on Berlin, London, or Kyiv buttons to get the weather forecast.
- Location Sharing: Share your location to receive weather updates for your current location.
- City Name Input: Type and send the name of any city to get the weather forecast.

## Run as a Python Script
python main.py