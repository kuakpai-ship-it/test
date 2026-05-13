# weather_bot.py - ИСПРАВЛЕННАЯ ВЕРСИЯ

import asyncio
import logging
import aiohttp
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.enums import ParseMode

# ========== НАСТРОЙКИ ==========
BOT_TOKEN = "ВАШ_ТОКЕН"  # ← ВСТАВЬТЕ СВОЙ ТОКЕН!

# Включаем логирование
logging.basicConfig(level=logging.INFO)

# Создаем бота и диспетчер
bot = Bot(token="8709522192:AAHiLCwz-m1-MLnCmqwyXP5JO-0dNPgSw84")
dp = Dispatcher()


# ========== ФУНКЦИЯ ПОЛУЧЕНИЯ ПОГОДЫ ==========
async def get_weather(city: str) -> str:
    """Получает погоду с wttr.in"""
    
    city = city.strip()
    url = f"https://wttr.in/{city}?mM&format=%t|%h|%p|%w|%C"
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=10) as response:
                if response.status == 200:
                    data = await response.text()
                    parts = data.strip().split('|')
                    
                    if len(parts) >= 5:
                        temp = parts[0]
                        humidity = parts[1]
                        pressure = parts[2]
                        wind = parts[3]
                        condition = parts[4]
                        
                        message = f"""
🌍 Погода в городе: <b>{city.upper()}</b>
━━━━━━━━━━━━━━━━━━━━━
🌡️ Температура: <b>{temp}</b>
💧 Влажность: <b>{humidity}</b>
🔧 Давление: <b>{pressure}</b>
💨 Ветер: <b>{wind}</b>
☁️ Состояние: <b>{condition}</b>
━━━━━━━━━━━━━━━━━━━━━
📅 Данные: wttr.in
                        """
                        return message.strip()
                    else:
                        return f"❌ Не удалось получить данные для города <b>{city}</b>"
                else:
                    return f"❌ Ошибка сервера погоды. Код: {response.status}"
                    
    except asyncio.TimeoutError:
        return "⏰ Превышено время ожидания"
    except Exception as e:
        return f"⚠️ Ошибка: {str(e)}"


# ========== КОМАНДА /start ==========
@dp.message(Command("start"))
async def cmd_start(message: Message):
    welcome_text = """
🌤️ <b>Привет! Я бот погоды!</b>

Я помогу узнать погоду в любом городе.

<b>Как пользоваться:</b>
/weather <i>Название города</i>

<b>Примеры:</b>
/weather Москва
/weather Санкт-Петербург
/weather London
"""
    await message.answer(welcome_text, parse_mode=ParseMode.HTML)


# ========== КОМАНДА /weather ==========
@dp.message(Command("weather"))
async def cmd_weather(message: Message):
    parts = message.text.split(maxsplit=1)
    
    if len(parts) < 2:
        error_text = """
❌ <b>Вы не указали город!</b>

Правильный формат:
/weather <i>Название города</i>

<b>Пример:</b>
/weather Москва
        """
        await message.answer(error_text, parse_mode=ParseMode.HTML)
        return
    
    city = parts[1].strip()
    
    loading_msg = await message.answer(
        f"🔍 <b>Ищу погоду для {city}...</b>",
        parse_mode=ParseMode.HTML
    )
    
    weather_info = await get_weather(city)
    await loading_msg.delete()
    await message.answer(weather_info, parse_mode=ParseMode.HTML)


# ========== КОМАНДА /help ==========
@dp.message(Command("help"))
async def cmd_help(message: Message):
    help_text = """
❓ <b>Помощь по командам</b>

<b>Основные команды:</b>
/start - Начать работу
/help - Показать справку
/weather <i>город</i> - Узнать погоду

<b>Пример:</b>
/weather Москва
    """
    await message.answer(help_text, parse_mode=ParseMode.HTML)


# ========== ОБРАБОТКА ОБЫЧНЫХ СООБЩЕНИЙ ==========
@dp.message()
async def handle_any_message(message: Message):
    default_text = """
🤔 <b>Я не понимаю эту команду</b>

Вот что я умею:
/start - Приветствие
/help - Справка
/weather <i>город</i> - Погода

<b>Попробуйте:</b>
/weather Москва
    """
    await message.answer(default_text, parse_mode=ParseMode.HTML)


# ========== ЗАПУСК БОТА ==========
async def main():
    """Главная функция, которая запускает бота"""
    
    # 👇 ЭТА СТРОЧКА ОТКЛЮЧАЕТ WEBHOOK И РЕШАЕТ ПРОБЛЕМУ!
    await bot.delete_webhook()
    
    # Получаем информацию о боте
    bot_info = await bot.get_me()
    
    print("=" * 50)
    print("🤖 БОТ ПОГОДЫ ЗАПУЩЕН!")
    print("=" * 50)
    print(f"📱 Имя бота: {bot_info.first_name}")
    print(f"🔗 Username: @{bot_info.username}")
    print(f"🆔 ID бота: {bot_info.id}")
    print("=" * 50)
    print("✅ Бот готов к работе!")
    print("📨 Идите в Telegram и напишите /start")
    print("=" * 50)
    print("🛑 Для остановки нажмите Ctrl+C")
    print("=" * 50)
    
    # Запускаем бота
    await dp.start_polling(bot)


# ========== ТОЧКА ВХОДА ==========
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n" + "=" * 50)
        print("👋 Бот остановлен пользователем")
        print("=" * 50)
    except Exception as e:
        print(f"\n❌ Критическая ошибка: {e}")