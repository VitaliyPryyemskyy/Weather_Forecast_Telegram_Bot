import requests
from datetime import datetime
from config import tg_bot_token, open_weather_token, unsplash_access_key
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.dispatcher.filters import Text
from aiogram.contrib.middlewares.i18n import I18nMiddleware
import datetime

bot = Bot(token=tg_bot_token)
dp = Dispatcher(bot)


i18n = I18nMiddleware("bot", "locales")
dp.middleware.setup(i18n)
_ = i18n.gettext


def keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    berlin_button = KeyboardButton("Berlin")
    london_button = KeyboardButton("London")
    kyiv_button = KeyboardButton("Kyiv")
    my_location_button = KeyboardButton("My Location", request_location=True)
    exit_button = KeyboardButton("👨‍💻 EXIT")
    markup.add(
        berlin_button, kyiv_button, london_button, my_location_button, exit_button
    )
    return markup


@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    markup = keyboard()
    await message.reply("Send a city name or share your location:", reply_markup=markup)


@dp.message_handler(Text(equals="👨‍💻 EXIT"))
async def exit_command(message: types.Message):
    await message.reply("Exiting...")
    await bot.session.close()


@dp.message_handler(content_types=["location"])
async def get_weather_by_location(message: types.Message):
    latitude = message.location.latitude
    longitude = message.location.longitude
    try:
        r = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={open_weather_token}&units=metric"
        )
        data = r.json()
        await send_weather_info(message, data)
    except Exception as e:
        print(f"Error getting weather by location: {e}")
        await message.reply("Failed to get weather for your location 🤷🏼‍♂️")


@dp.message_handler()
async def get_weather(message: types.Message):
    try:
        r = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={open_weather_token}&units=metric"
        )
        data = r.json()
        await send_weather_info(message, data)
    except Exception as e:
        print(f"Error getting weather by city name: {e}")
        await message.reply(f"I don't know a city {message.text} 🤷🏼‍♂️")


async def send_weather_info(message: types.Message, data):
    try:
        city = data["name"]
        cur_weather = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]
        sky = data["weather"][0]["description"]
        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        wind = data["wind"]["speed"]
        sunrise_time = datetime.datetime.fromtimestamp(data["sys"]["sunrise"]).strftime(
            "%H:%M:%S"
        )
        sunset_time = datetime.datetime.fromtimestamp(data["sys"]["sunset"]).strftime(
            "%H:%M:%S"
        )
        length_of_day = datetime.datetime.fromtimestamp(
            data["sys"]["sunset"]
        ) - datetime.datetime.fromtimestamp(data["sys"]["sunrise"])

        # Get city image from Unsplash
        image_url = get_city_image(city)

        await message.reply(
            f"Today is: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
            f"Weather in {city}\n"
            f"Temperature: {cur_weather}°C\nFeels like: {feels_like}\n"
            f"Sky is: {sky}\nHumidity: {humidity}%\nPressure: {pressure} mm\nWind speed: {wind} m/sec\n"
            f"Sunrise at {sunrise_time}\nSunset at {sunset_time}\nLength of day is: {length_of_day}\n"
            f"[City Image]({image_url})",
            parse_mode="Markdown",
        )
    except Exception as e:
        print(f"Error parsing weather data: {e}")
        await message.reply("Failed to parse weather data 🤷🏼‍♂️")


def get_city_image(city):
    try:
        response = requests.get(
            f"https://api.unsplash.com/search/photos?query={city}&client_id={unsplash_access_key}"
        )
        data = response.json()
        if data["results"]:
            return data["results"][0]["urls"]["small"]
        else:
            return "No image found"
    except Exception as e:
        print(f"Error getting city image: {e}")
        return "No image found"


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
