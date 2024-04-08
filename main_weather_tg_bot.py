import requests
from datetime import datetime
from config import tg_bot_token, open_wether_token
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor 
import datetime

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton



bot = Bot(token=tg_bot_token)
dp = Dispatcher(bot)


def keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    berlin_button = KeyboardButton('Berlin')
    kyiv_button = KeyboardButton('Kyiv')
    exit_button = KeyboardButton('👨‍💻 EXIT')
    markup.add(exit_button, berlin_button, kyiv_button)
    return markup

# @dp.message_handler(lambda message: message.text == '🇩🇪 Berlin')
# async def berlin_weather(message: types.Message):
#     await get_weather(message, 'Berlin')

# @dp.message_handler(lambda message: message.text == '🇺🇦 Kyiv')
# async def kyiv_button(message: types.Message):
#     await get_weather(message, 'Kyiv')


@dp.message_handler(lambda message: message.text == '👨‍💻 EXIT')
async def exit_command(message: types.Message):
    await message.reply('Exiting...')
    await bot.close()
    

@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    markup = keyboard()
    await message.reply('Send a city name:', reply_markup=markup)



@dp.message_handler()
async def get_weather(message: types.Message):
    try:
        r = requests.get(
            f'https://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={open_wether_token}&units=metric')
        data = r.json()

        city = data['name']
        cur_weather = data['main']['temp']
        feels_like = data['main']['feels_like']
        sky = data['weather'][0]['description']
        humidity = data['main']['humidity']
        pressure = data['main']['pressure']
        wind = data['wind']['speed']
        sunrise_timestamp = datetime.datetime.fromtimestamp(
            data["sys"]["sunrise"])

        sunset_timestamp = datetime.datetime.fromtimestamp(
            data["sys"]["sunset"])
        lenght_of_day = datetime.datetime.fromtimestamp(
            data["sys"]["sunset"]) - datetime.datetime.fromtimestamp(
            data["sys"]["sunrise"])
        await message.reply(f"Today is: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
                            f'Weather in {city}\n'
                            f'Temperature: {cur_weather}°C\nFeels like: {feels_like}\n'
                            f'Sky is: {sky}\nHumidity: {humidity}%\nPressure: {pressure}mm\nWind speed: {wind}m/sec\n'
                            f'Sunrise at {sunrise_timestamp}\nSunset at {sunset_timestamp}\nLenght of day is:{lenght_of_day}')
    except Exception as e:
        await message.reply(f"I don't know  a city {message.text} 🤷🏼‍♂️")
   




if __name__ == '__main__':
    executor.start_polling(dp)
