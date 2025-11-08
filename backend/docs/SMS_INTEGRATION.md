# SMS Integration Guide

SMS интеграция через SMSC.ru для отправки сообщений лидам.

## Конфигурация

### 1. Получение учетных данных SMSC.ru

1. Зарегистрируйтесь на https://smsc.ru/
2. Пополните баланс
3. Получите логин и пароль из личного кабинета

### 2. Настройка переменных окружения

Добавьте в `.env`:

```bash
SMSC_LOGIN=your_login
SMSC_PASSWORD=your_password
SMSC_SENDER=FastLead
SMSC_API_URL=https://smsc.ru/sys/send.php
```

### 3. Настройка Celery

Убедитесь, что Redis запущен:

```bash
redis-server
```

Добавьте в `.env`:

```bash
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0
```

## Запуск

### 1. Запустите FastAPI backend

```bash
cd backend
uvicorn app.main:app --reload
```

### 2. Запустите Celery worker

В отдельном терминале:

```bash
cd backend
chmod +x run_celery_worker.sh
./run_celery_worker.sh
```

Или напрямую:

```bash
celery -A app.core.celery_app:celery_app worker --loglevel=info
```

### 3. (Опционально) Запустите Celery beat

Для периодических задач:

```bash
chmod +x run_celery_beat.sh
./run_celery_beat.sh
```

## Использование

### Автоматическая отправка SMS при создании лида

Когда создается лид с каналом `sms`, автоматически:

1. Lead сохраняется в базу данных
2. Запускается Celery задача `process_new_lead_task`
3. Задача отправляет приветственное SMS через SMSC.ru
4. Статус лида обновляется на `CONTACTED`

### Ручная отправка SMS

Вызовите Celery задачу напрямую:

```python
from app.tasks.sms_tasks import send_sms_task

# Отправить SMS
result = send_sms_task.delay(
    phone="+79991234567",
    message="Ваше сообщение",
    lead_id=123  # опционально
)

# Проверить результат
print(result.get())
```

### Отправка кода подтверждения

```python
from app.tasks.sms_tasks import send_verification_code_task

result = send_verification_code_task.delay(
    phone="+79991234567",
    code="1234",
    lead_id=123
)
```

### Отправка напоминания о встрече

```python
from app.tasks.sms_tasks import send_appointment_reminder_task

result = send_appointment_reminder_task.delay(
    phone="+79991234567",
    appointment_time="15 января в 14:00",
    lead_id=123
)
```

## API Endpoints

### Создать лид с SMS каналом

```bash
curl -X POST "http://localhost:8000/api/v1/leads" \
  -H "Content-Type: application/json" \
  -H "X-Tenant-Id: 1" \
  -d '{
    "name": "Иван Петров",
    "phone": "+79991234567",
    "channel": "sms",
    "consent": {
      "gdpr": true,
      "marketing": false
    }
  }'
```

Ответ:

```json
{
  "lead": {
    "id": 123,
    "name": "Иван Петров",
    "phone": "+79991234567",
    "channel": "sms",
    "status": "new",
    "created_at": "2024-01-15T12:00:00Z",
    "tenant_id": 1
  },
  "next_action": "send_sms"
}
```

После создания лида автоматически отправляется SMS.

## Мониторинг

### Проверка очереди Celery

```bash
# Проверить активные задачи
celery -A app.core.celery_app:celery_app inspect active

# Проверить зарегистрированные задачи
celery -A app.core.celery_app:celery_app inspect registered

# Проверить статистику
celery -A app.core.celery_app:celery_app inspect stats
```

### Проверка баланса SMSC.ru

```python
from app.services.sms_service import SMSService

sms_service = SMSService()
balance = await sms_service.get_balance()
print(f"Баланс: {balance} руб.")
```

### Проверка статуса доставки SMS

```python
from app.services.sms_service import SMSService

sms_service = SMSService()
status = await sms_service.get_status(
    message_id=12345,
    phone="+79991234567"
)
print(status)
```

## Обработка ошибок

### Retry логика

Celery автоматически повторяет неудачные задачи:

- Максимум 3 попытки
- Exponential backoff (2s, 4s, 8s, ...)
- Максимальная задержка: 10 минут

### Типичные ошибки

**1. Invalid phone number**

```
SMSServiceError: Invalid phone number: 1234567
```

Решение: Используйте международный формат `+79991234567`

**2. SMSC API error**

```
SMSServiceError: SMSC API error 2: Неправильный логин или пароль
```

Решение: Проверьте `SMSC_LOGIN` и `SMSC_PASSWORD` в `.env`

**3. Insufficient balance**

```
SMSServiceError: SMSC API error 6: Недостаточно средств
```

Решение: Пополните баланс на https://smsc.ru/

## Тестирование

### Unit тесты

```bash
cd backend
pytest tests/test_sms_service.py
```

### Интеграционный тест

```bash
# Установите тестовые credentials в .env
SMSC_LOGIN=test
SMSC_PASSWORD=test

# Запустите тест
python -m pytest tests/integration/test_sms_integration.py
```

## Production Deployment

### Supervisor конфигурация

```ini
[program:fast_lead_celery]
command=/path/to/venv/bin/celery -A app.core.celery_app:celery_app worker --loglevel=info
directory=/path/to/fast_lead/backend
user=www-data
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/celery/fast_lead_worker.log
```

### Systemd service

```ini
[Unit]
Description=Fast Lead Celery Worker
After=network.target redis.target

[Service]
Type=forking
User=www-data
WorkingDirectory=/path/to/fast_lead/backend
ExecStart=/path/to/venv/bin/celery -A app.core.celery_app:celery_app worker --loglevel=info --pidfile=/var/run/celery/fast_lead.pid
Restart=always

[Install]
WantedBy=multi-user.target
```

## Стоимость

SMSC.ru тарифы (примерно):

- Регистрация: бесплатно
- SMS по России: ~1-3 руб/сообщение
- Минимальное пополнение: 500 руб

Рекомендуется:
- Для тестирования: 500 руб (~200 SMS)
- Для production: от 5000 руб

## Поддержка

- SMSC.ru документация: https://smsc.ru/api/http/
- SMSC.ru поддержка: support@smsc.ru
- Fast Lead issues: https://github.com/CultureOrganica/fast_lead/issues
