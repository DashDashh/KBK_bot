# -*- coding: cp1251 -*-
import asyncio
import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram_dialog import setup_dialogs

from dialogs.main_menu import rt, main_menu_dialog
from dialogs.registration import registration_dialog


load_dotenv()
API_TOKEN = os.getenv("BOT_TOKEN")

async def my_bot():
    if not API_TOKEN:
        print("Ошибка: BOT_TOKEN не найден в .env файле")
        return
        
    bot = Bot(token=API_TOKEN)
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)
    
    dp.include_router(rt)
    dp.include_router(main_menu_dialog)
    dp.include_router(registration_dialog)
    
    setup_dialogs(dp)
    
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(my_bot())
    except KeyboardInterrupt:
        print('Бот выключен')