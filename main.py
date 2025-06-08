from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
import os

TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def welcome(msg: types.Message):
    await msg.answer("Salom! Men telefon orqali ishlayotgan Telegram botman 😊")

if __name__ == '__main__':
    executor.start_polling(dp)