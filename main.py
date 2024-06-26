import requests

# from pprint import pprint
from config import open_weather_token
import datetime


def get_wether(city, open_wether_token):
    try:
        r = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={open_wether_token}&units=metric"
        )
        data = r.json()

        city = data["name"]
        cur_weather = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]
        sky = data["weather"][0]["description"]
        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        wind = data["wind"]["speed"]
        sunrise_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])

        sunset_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunset"])
        lenght_of_day = datetime.datetime.fromtimestamp(
            data["sys"]["sunset"]
        ) - datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
        print(
            f"Today is: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
            f"Wether in {city}\n"
            f"Temperature: {cur_weather}°C\nFeels like: {feels_like}\n"
            f"Sky is: {sky}\nHumidity: {humidity}%\nPressure: {pressure}mm\nWind speed: {wind}m/sec\n"
            f"Sunrise at {sunrise_timestamp}\nSunset at {sunset_timestamp}\nLenght of day is:{lenght_of_day}"
        )
    except Exception as ex:
        print(ex)
        print(f"check name of city")


def main():
    city = input("Enter your city: ")
    get_wether(city, open_weather_token)


if __name__ == "__main__":
    main()
