from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router()


@router.message(Command(commands=["start", "help"]))
async def cmd_start(message: Message):
    text = (
        "👋 Привет!\n"
        "Тут вы можете вести свои задачи по времени (Europe/Minsk) - UTC+3\n\n"
        "Доступные команды:\n"
        "/add — создать новую задачу\n"
        "/mytasks — показать ваши задачи\n"
        "/view <id> — просмотреть подробно\n"
        "/done <id> — отметить задачу выполненной\n"
        "/undone <id> — отметить задачу невыполненой\n"
    )
    await message.answer(text)


def register_dispatcher(dp):
    dp.include_router(router)
