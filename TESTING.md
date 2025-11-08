# Fast Lead - Testing Guide

Инструкция по тестированию Fast Lead после клонирования репозитория.

## Prerequisites

### Установка зависимостей (macOS)

```bash
# 1. PostgreSQL
brew install postgresql@14
brew services start postgresql@14

# 2. Redis
brew install redis
brew services start redis

# 3. Python 3.11
brew install pyenv
pyenv install 3.11.0
pyenv global 3.11.0

# 4. Node.js 20
brew install nvm
nvm install 20
nvm use 20
```

## Backend Setup

### 1. Клонирование и настройка

```bash
# Clone repository
git clone https://github.com/CultureOrganica/fast_lead.git
cd fast_lead

# Switch to development branch
git checkout claude/setup-repo-access-011CUuLgKyDBqkv4FYPgtUpp

# Setup backend
cd backend
```

### 2. Создание виртуального окружения

```bash
python -m venv venv
source venv/bin/activate  # Mac/Linux
# или
venv\Scripts\activate  # Windows

# Установка зависимостей
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

### 3. Настройка .env

```bash
# Скопируйте .env.example
cp .env.example .env

# Отредактируйте .env и установите минимум:
DATABASE_URL=postgresql+asyncpg://postgres@localhost:5432/fast_lead_dev
REDIS_URL=redis://localhost:6379/0
SECRET_KEY=$(python -c "import secrets; print(secrets.token_urlsafe(32))")
JWT_SECRET_KEY=$(python -c "import secrets; print(secrets.token_urlsafe(32))")
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0

# Для SMS (опционально - можно пропустить для начала)
SMSC_LOGIN=
SMSC_PASSWORD=
```

### 4. Создание базы данных

```bash
# Создайте базу данных
createdb fast_lead_dev

# Или через psql:
psql postgres
CREATE DATABASE fast_lead_dev;
\q
```

### 5. Проверка импортов

```bash
# Запустите проверку всех импортов
python check_imports.py

# Ожидаемый результат:
# ✅ All imports successful!
# ⚠️ WARNINGS (если не настроены SMSC credentials - это нормально)
```

### 6. Проверка database

```bash
# Проверьте подключение к БД
python check_database.py

# Если таблиц нет - это нормально, переходите к миграциям
```

### 7. Создание и применение миграций

```bash
# Создайте начальную миграцию
python create_migration.py

# Примените миграцию
alembic upgrade head

# Проверьте снова
python check_database.py

# Теперь должно показать:
# ✓ tenants
# ✓ users
# ✓ leads
```

### 8. Запуск всех проверок разом

```bash
./run_checks.sh
```

## Запуск Backend

### Терминал 1: FastAPI

```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Откройте http://localhost:8000/docs для Swagger UI.

### Терминал 2: Celery Worker

```bash
cd backend
source venv/bin/activate
./run_celery_worker.sh

# Или напрямую:
celery -A app.core.celery_app:celery_app worker --loglevel=info
```

### Терминал 3 (опционально): Celery Beat

```bash
cd backend
source venv/bin/activate
./run_celery_beat.sh
```

## Widget Setup

### 1. Установка зависимостей

```bash
cd widget
npm install
```

### 2. Запуск dev-сервера

```bash
npm run dev
```

Откройте http://localhost:5173 для тестовой страницы с виджетом.

### 3. Сборка production версии

```bash
npm run build

# Результат в widget/dist/:
# - fast-lead-widget.es.js
# - fast-lead-widget.umd.js
```

## Тестирование

### 1. Проверка Health Endpoint

```bash
curl http://localhost:8000/health

# Ожидаемый ответ:
# {"status":"healthy","timestamp":"2024-01-15T12:00:00Z"}
```

### 2. Создание тестового Tenant

```bash
# Откройте psql
psql fast_lead_dev

# Создайте тестовый tenant
INSERT INTO tenants (name, slug, is_active)
VALUES ('Test Company', 'test-company', true);

# Проверьте ID
SELECT id, name FROM tenants;
# Запомните tenant_id (например, 1)

\q
```

### 3. Создание Lead через API

```bash
# Создайте lead с web каналом
curl -X POST "http://localhost:8000/api/v1/leads" \
  -H "Content-Type: application/json" \
  -H "X-Tenant-Id: 1" \
  -d '{
    "name": "Иван Тестовый",
    "phone": "+79991234567",
    "email": "test@example.com",
    "channel": "web",
    "consent": {
      "gdpr": true,
      "marketing": false
    }
  }'

# Ожидаемый ответ:
# {
#   "lead": {
#     "id": 1,
#     "name": "Иван Тестовый",
#     "channel": "web",
#     "status": "new",
#     ...
#   },
#   "next_action": "manual_review"
# }
```

### 4. Проверка Lead в базе

```bash
psql fast_lead_dev
SELECT id, name, channel, status FROM leads;
\q
```

### 5. Тестирование SMS (если настроен SMSC)

```bash
# ВАЖНО: SMS будут отправлены на реальный номер!
# Для тестирования используйте свой номер

curl -X POST "http://localhost:8000/api/v1/leads" \
  -H "Content-Type: application/json" \
  -H "X-Tenant-Id: 1" \
  -d '{
    "name": "Тест SMS",
    "phone": "+79991234567",
    "channel": "sms",
    "consent": {
      "gdpr": true,
      "marketing": true
    }
  }'

# Проверьте логи Celery worker:
# [INFO] Processing new lead: 2
# [INFO] Processing SMS lead: 2
# [INFO] SMS sent successfully to +79991234567
```

### 6. Тестирование виджета

1. Откройте http://localhost:5173
2. Нажмите кнопку 💬 в правом нижнем углу
3. Заполните форму
4. Нажмите "Отправить"
5. Проверьте lead в базе данных

## Проверка Celery

### Статус worker

```bash
celery -A app.core.celery_app:celery_app inspect active

# Должен показать активные задачи
```

### Статистика

```bash
celery -A app.core.celery_app:celery_app inspect stats
```

### Зарегистрированные задачи

```bash
celery -A app.core.celery_app:celery_app inspect registered

# Должны быть видны:
# - send_sms
# - process_new_lead
# - send_verification_code
# - send_appointment_reminder
```

## Проверка SMS Service (если настроен SMSC)

```bash
# Откройте Python REPL
python

>>> import asyncio
>>> from app.services.sms_service import SMSService
>>>
>>> sms = SMSService()
>>> balance = asyncio.run(sms.get_balance())
>>> print(f"Balance: {balance} руб.")
```

## Troubleshooting

### Ошибка: Connection refused (PostgreSQL)

```bash
# Проверьте, запущен ли PostgreSQL
brew services list | grep postgresql

# Запустите, если не запущен
brew services start postgresql@14
```

### Ошибка: Connection refused (Redis)

```bash
# Проверьте Redis
brew services list | grep redis

# Запустите
brew services start redis
```

### Ошибка: ModuleNotFoundError

```bash
# Убедитесь, что виртуальное окружение активировано
source venv/bin/activate

# Переустановите зависимости
pip install -r requirements.txt
```

### Ошибка: Alembic can't find migration

```bash
# Удалите старые миграции
rm -rf alembic/versions/*.py

# Создайте новую
python create_migration.py

# Примените
alembic upgrade head
```

### SMS не отправляются

1. Проверьте SMSC credentials в .env
2. Проверьте баланс: `python check_database.py`
3. Проверьте логи Celery worker
4. Убедитесь, что номер телефона в формате +7XXXXXXXXXX

### Celery задачи не выполняются

1. Убедитесь, что Redis запущен
2. Убедитесь, что Celery worker запущен
3. Проверьте логи worker на ошибки
4. Проверьте, что CELERY_BROKER_URL правильный

## Логи

### Backend FastAPI

Логи выводятся в консоль где запущен `uvicorn`

### Celery Worker

Логи выводятся в консоль где запущен worker

Для сохранения в файл:

```bash
celery -A app.core.celery_app:celery_app worker --loglevel=info \
  --logfile=/tmp/celery_worker.log
```

### PostgreSQL

```bash
# macOS
tail -f /usr/local/var/log/postgresql@14.log
```

## Что дальше?

После успешного тестирования:

1. Протестируйте создание лидов через все каналы
2. Проверьте работу orchestrator (статусы лидов)
3. Проверьте работу SMS интеграции
4. Соберите widget для production: `npm run build`
5. Дайте feedback по багам/проблемам

## Need Help?

- Backend issues: https://github.com/CultureOrganica/fast_lead/issues
- SMSC.ru документация: https://smsc.ru/api/http/
- FastAPI docs: https://fastapi.tiangolo.com/
- Celery docs: https://docs.celeryq.dev/
