import logging

from aiogram import Bot, Dispatcher

from config import settings
from handlers import start_handler, tasks_handler

logging.basicConfig(level=logging.INFO)


bot = Bot(
    token=settings.TELEGRAM_TOKEN,
)
dp = Dispatcher()


start_handler.register_dispatcher(dp)
tasks_handler.register_dispatcher(dp)

if __name__ == "__main__":
    dp.run_polling(bot)
