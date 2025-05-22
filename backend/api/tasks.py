from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo

import requests
from celery import shared_task

from api.models import Task
from config import settings

API_URL = f"https://api.telegram.org/bot{settings.TELEGRAM_TOKEN}/sendMessage"


@shared_task
def check_tasks_deadline():
    current_time = datetime.now(timezone.utc)
    window_end = current_time + timedelta(minutes=10)
    user_tz = ZoneInfo("Europe/Minsk")

    tasks = Task.objects.filter(status="undone")

    for task in tasks:
        try:
            local_deadline = datetime.strptime(task.deadline, "%d.%m.%Y %H:%M")
            local_deadline = local_deadline.replace(tzinfo=user_tz)
            deadline_utc = local_deadline.astimezone(timezone.utc)
        except Exception as e:
            print(f"Ошибка парсинга deadline для задачи {task.id}: {e}")
            continue

        if current_time <= deadline_utc <= window_end:
            text = (
                f"⚠️ <b>Напоминание!</b>\n"
                f"⏳ Время для выполнения задачи подходит к концу:\n\n"
                f"<b>📝 Задача #{task.id}</b>\n"
                f"<b>📌 Заголовок:</b> {task.title}\n"
                f"<b>🧾 Описание:</b> {task.description}\n"
                f"<b>⏰ Дедлайн:</b> {task.deadline} (Europe/Minsk)\n"
                f"<b>📍 Статус:</b> 🕒 Не выполнена"
            )
            resp = requests.post(
                API_URL,
                data={
                    "chat_id": task.telegram_user_id,
                    "text": text,
                    "parse_mode": "HTML",
                },
                timeout=10,
            )
            if not resp.ok:
                print(f"Ошибка отправки Telegram ({resp.status_code}): {resp.text}")
