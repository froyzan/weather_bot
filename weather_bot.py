import asyncio
import aiohttp
import logging
import sys
from os import getenv

from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiocache import cached

# Токен Telegram-бота и API-ключ OpenWeather
OPENWEATHER_API_KEY = getenv("API_KEY")
TOKEN = getenv("BOT_TOKEN")

if not OPENWEATHER_API_KEY or not TOKEN:
    raise ValueError("Необходимо установить переменные окружения API_KEY и BOT_TOKEN.")

dp = Dispatcher()

# Функция для получения погоды через OpenWeather API
@cached(ttl=300)  # Кэш на 5 минут
async def get_weather(city: str) -> str:
  url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}&units=metric&lang=ru"
  try:
    async with aiohttp.ClientSession() as session:
      async with session.get(url) as response:
        if response.status == 200:
          data = await response.json()
          temp = data["main"]["temp"]
          feels_like = data['main']['feels_like']
          pressure = data["main"]["pressure"]
          weather_description = data["weather"][0]["main"]
          description = data["weather"][0]["description"]
          humidity = data["main"]["humidity"]
          wind_speed = data["wind"]["speed"]
                  
          code_to_smile = {
            "Clear": "\U00002600",
            "Clouds": "\U00002601",
            "Rain": "\U00002614",
            "Drizzle": "\U00002614",
            "Thunderstorm": "\U000026A1",
            "Snow": "\U0001F328",
            "Mist": "\U0001F32B"}                 
                  
          if weather_description in code_to_smile:
            wd = code_to_smile[weather_description]
          else:
            wd = "\U0001F52D"

          return (f"Погода в городе {city.capitalize()}:\n"
                  f"Температура: {temp:.0f}°C\n"
                  f"Ощущается как: {feels_like:.0f}°C\n"
                  f"Давление: {pressure/1.333:.0f} мм.рт.\n"
                  f"Описание: {description} {wd}\n"
                  f"Влажность: {humidity}%\n"
                  f"Скорость ветра: {wind_speed} м/с")
        elif response.status == 404:
          return "Город не найден. Проверьте название."
        else:
          return "Ошибка на стороне сервера. Попробуйте позже."
              
  except aiohttp.ClientError as e:
    logging.error(f"Ошибка при запросе к OpenWeather API: {e}")
    return "Не удалось получить данные о погоде. Проверьте подключение к интернету."
  except asyncio.TimeoutError:
    return "Превышено время ожидания ответа от сервера."

# Обработчик команды /start
@dp.message(CommandStart())
async def start_command(message: Message):
  keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Москва", callback_data="weather Москва")],
        [InlineKeyboardButton(text="Санкт-Петербург", callback_data="weather Санкт-Петербург")],
        [InlineKeyboardButton(text="Новосибирск", callback_data="weather Новосибирск")]
    ])
  await message.answer(
    f"Привет, {html.bold(message.from_user.first_name)}!\n"
    f"Введи название города или выбери из списка ниже:",
    reply_markup=keyboard,)

@dp.callback_query()
async def handle_callback(query):
  city = query.data.split()[1]
  weather_info = await get_weather(city)
  await query.message.edit_text(weather_info)

# Обработчик текстовых сообщений (название города)
@dp.message()
async def weather_handler(message: Message):
  city = message.text.strip()
  if not city.isalpha():
    await message.answer("Пожалуйста, введите корректное название города.")
  weather_info = await get_weather(city)
  logging.info(f"Запрос погоды для города: {city}")
  wait message.answer(weather_info)

# Основная функция для запуска бота
async def main() -> None:
  bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
  await dp.start_polling(bot)

if __name__ == "__main__":
  logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s", 
    stream=sys.stdout)  
  asyncio.run(main())

