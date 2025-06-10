## 📌 Horizont Job Task
- Начало: 21.05.2025
- Завершение: 22.05.2025

## ✅ Feedback
админку через nginx, сериализатор на post/put/get/delete

### ⚙️ Технологии
- Python
- Django
- Django REST Framework
- PostgreSQL
- Celery
- Redis
- Aiogram
- Docker
- Nginx


### 📁 Настройка окружения
Создай файл .env на основе .env.example и укажи следующие значения(пример):
```env
DB_NAME=task_managment
DB_USER=user
DB_PASS=password
DB_HOST=postgrte
DB_PORT=5432

REDIS_HOST=redis
REDIS_PORT=6379
REDIS_PASS=password
REDIS_DB_CELERY_BROKER=1
REDIS_DB_CELERY_RESULT=2
REDIS_DB_CELERY_REDBEAT=3

TELEGRAM_TOKEN=fxd7f871238f7d91289d7a98fxcv
```

### 🐳 Запуск
```bash
docker compose -f docker-compose-services.yml up -d
docker compose -f docker-compose.yml up -d
```

### 🤖 Telegram Bot

Список доступных команд:

| Команда        | Описание                             |
|----------------|--------------------------------------|
| /start         | Старт взаимодействия                 |
| /add           | Добавить задачу                      |
| /mytasks       | Список всех задач                    |
| /view <id>     | Просмотр задачи по ID                |
| /done <id>     | Отметить задачу как выполненную      |
| /undone <id>   | Отметить задачу как невыполненную    |

### 🔔 Уведомления
Если до дедлайна задачи осталось 10 минут или меньше, пользователю отправляется Telegram-уведомление.

### 📘 REST API
REST API документация: http://localhost:8080/docs/
