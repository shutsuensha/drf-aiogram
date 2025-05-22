from datetime import datetime

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from services.tasks_api import create_task, get_task_detail, list_tasks, mark_done, mark_undone
from states.tasks_states import AddTask

router = Router()


@router.message(F.text == "/add")
async def add_task(message: Message, state: FSMContext):
    await state.set_state(AddTask.waiting_for_title)
    await message.answer("Введите заголовок задачи:")


@router.message(AddTask.waiting_for_title)
async def get_title(message: Message, state: FSMContext):
    await state.update_data(title=message.text)
    await state.set_state(AddTask.waiting_for_description)
    await message.answer("Введите описание задачи:")


@router.message(AddTask.waiting_for_description)
async def get_description(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    await state.set_state(AddTask.waiting_for_deadline)
    await message.answer("Введите дату и время в формате: 22.05.2025 18:45 (Europe/Minsk)")


@router.message(AddTask.waiting_for_deadline)
async def get_deadline(message: Message, state: FSMContext):
    deadline_str = message.text.strip()

    try:
        datetime.strptime(deadline_str, "%d.%m.%Y %H:%M")
    except ValueError:
        return await message.answer(
            "❌ Неверный формат. Введите дату и время в формате: 22.05.2025 18:45"
        )

    await state.update_data(deadline=deadline_str)
    await finish_task_creation(message, state)


async def finish_task_creation(message: Message, state: FSMContext):
    data = await state.get_data()

    title = data.get("title")
    description = data.get("description")
    deadline = data.get("deadline")

    if not all([title, description, deadline]):
        return await message.answer("❌ Ошибка: Не все данные указаны.")

    task_data = {
        "title": title,
        "description": description,
        "deadline": deadline,
        "telegram_user_id": message.from_user.id,
    }

    try:
        task = await create_task(task_data)

        text = (
            f"✅ <b>Задача успешно создана!</b>\n\n"
            f"<b>ID:</b> {task['id']}\n"
            f"<b>Заголовок:</b> {task['title']}\n"
            f"<b>Описание:</b> {task['description']}\n"
            f"<b>Дедлайн:</b> ⏰ {task['deadline']} (Europe/Minsk)\n"
            f"<b>Статус:</b> 🕒 {task['status'].capitalize()}"
        )
        await message.answer(text, parse_mode="HTML")

    except Exception as e:
        await message.answer(f"❌ Не удалось создать задачу: {str(e)}")

    await state.clear()


@router.message(Command(commands=["mytasks"]))
async def cmd_list(message: Message):
    tasks = await list_tasks(message.from_user.id)

    if not tasks:
        return await message.answer("❌ У вас пока нет задач.")

    lines = ["🗂 <b>Ваши задачи:</b>\n"]
    for t in tasks:
        status_icon = "✅ Выполнена" if t["status"] == "done" else "🕒 В процессе"
        lines.append(
            f"<b>ID:</b> {t['id']}\n"
            f"<b>📌 Заголовок:</b> {t['title']}\n"
            f"<b>⏰ Дедлайн:</b> {t['deadline']} (Europe/Minsk)\n"
            f"<b>Статус:</b> {status_icon}\n"
            f"------------------------------"
        )

    await message.answer("\n".join(lines), parse_mode="HTML")


@router.message(Command(commands=["view"]))
async def cmd_view(message: Message):
    try:
        _, task_id_str = message.text.split(" ", 1)
        task_id = int(task_id_str.strip())
    except Exception:
        return await message.answer("❗ Укажите ID задачи корректно: /view <id>")

    task = await get_task_detail(task_id)

    status_icon = "✅ Выполнена" if task["status"] == "done" else "🕒 В процессе"

    text = (
        f"📝 <b>Детали задачи #{task['id']}</b>\n\n"
        f"<b>📌 Заголовок:</b> {task['title']}\n"
        f"<b>🧾 Описание:</b> {task['description']}\n"
        f"<b>⏰ Дедлайн:</b> {task['deadline']} (Europe/Minsk)\n"
        f"<b>📍 Статус:</b> {status_icon}"
    )

    await message.answer(text, parse_mode="HTML")


@router.message(Command(commands=["done"]))
async def cmd_done(message: Message):
    try:
        _, task_id_str = message.text.split(" ", 1)
        task_id = int(task_id_str.strip())
    except Exception:
        return await message.answer("❗ Укажите ID задачи: /done <id>")

    task = await mark_done(task_id)

    text = (
        f"✅ <b>Задача #{task['id']} помечена как выполненная!</b>\n\n"
        f"<b>📌 Заголовок:</b> {task['title']}\n"
        f"<b>🧾 Описание:</b> {task['description']}\n"
        f"<b>⏰ Дедлайн:</b> {task['deadline']} (Europe/Minsk)\n"
        f"<b>📍 Статус:</b> ✅ Выполнена"
    )

    await message.answer(text, parse_mode="HTML")


@router.message(Command(commands=["undone"]))
async def cmd_undone(message: Message):
    try:
        _, task_id_str = message.text.split(" ", 1)
        task_id = int(task_id_str.strip())
    except Exception:
        return await message.answer("❗ Укажите ID задачи: /undone <id>")

    task = await mark_undone(task_id)

    text = (
        f"↩️ <b>Задача #{task['id']} помечена как невыполненная!</b>\n\n"
        f"<b>📌 Заголовок:</b> {task['title']}\n"
        f"<b>🧾 Описание:</b> {task['description']}\n"
        f"<b>⏰ Дедлайн:</b> {task['deadline']} (Europe/Minsk)\n"
        f"<b>📍 Статус:</b> 🕒 Не выполнена"
    )

    await message.answer(text, parse_mode="HTML")


def register_dispatcher(dp):
    dp.include_router(router)
