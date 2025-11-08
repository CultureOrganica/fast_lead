# Cal.com Integration Guide

Интеграция с Cal.com для автоматического букинга встреч с лидами.

## Что такое Cal.com

Cal.com - это открытая платформа для планирования встреч (альтернатива Calendly).

**Преимущества:**
- ✅ Open-source (можно self-host)
- ✅ RESTful API
- ✅ Webhooks для событий
- ✅ Поддержка различных календарей (Google, Outlook, etc.)
- ✅ Бесплатный план доступен

## Конфигурация

### 1. Регистрация на Cal.com

1. Создайте аккаунт на https://cal.com/
2. Настройте свой профиль и доступность
3. Создайте Event Type (например, "Консультация - 30 минут")

### 2. Получение API Key

1. Откройте https://cal.com/settings/developer/api-keys
2. Нажмите "Create API Key"
3. Скопируйте API ключ

### 3. Получение Event Type ID

1. Откройте https://cal.com/event-types
2. Нажмите на ваш Event Type
3. ID будет в URL: `https://cal.com/event-types/123` → ID = 123

### 4. Настройка Webhook

1. Откройте https://cal.com/settings/developer/webhooks
2. Нажмите "New Webhook"
3. Введите URL: `https://api.fast-lead.ru/webhooks/calcom`
4. Выберите события:
   - Booking created
   - Booking rescheduled
   - Booking cancelled
   - Booking completed
5. Скопируйте Webhook Secret

### 5. Настройка .env

Добавьте в `.env`:

```bash
CALCOM_API_KEY=cal_live_...
CALCOM_API_URL=https://api.cal.com/v1
CALCOM_EVENT_TYPE_ID=123
CALCOM_WEBHOOK_SECRET=your-webhook-secret
```

## API Endpoints

### POST /api/v1/bookings

Создать booking для лида.

**Request:**
```json
{
  "lead_id": 123,
  "name": "Иван Петров",
  "email": "ivan@example.com",
  "start_time": "2024-01-20T15:00:00Z",  // опционально
  "timezone": "Europe/Moscow",
  "metadata": {
    "source": "widget",
    "campaign": "spring2024"
  }
}
```

**Response:**
```json
{
  "booking_id": 456,
  "booking_uid": "abc123def",
  "booking_url": "https://cal.com/meet/abc123def",
  "start_time": "2024-01-20T15:00:00Z",
  "end_time": "2024-01-20T15:30:00Z",
  "status": "accepted",
  "lead_id": 123
}
```

**Curl example:**
```bash
curl -X POST "http://localhost:8000/api/v1/bookings" \
  -H "Content-Type: application/json" \
  -d '{
    "lead_id": 123,
    "name": "Иван Петров",
    "email": "ivan@example.com"
  }'
```

### GET /api/v1/bookings/availability

Получить доступные слоты.

**Query parameters:**
- `date_from`: Начальная дата (YYYY-MM-DD)
- `date_to`: Конечная дата (YYYY-MM-DD)

**Response:**
```json
[
  {
    "time": "2024-01-20T14:00:00Z",
    "available": true
  },
  {
    "time": "2024-01-20T15:00:00Z",
    "available": true
  }
]
```

**Curl example:**
```bash
curl "http://localhost:8000/api/v1/bookings/availability?date_from=2024-01-20&date_to=2024-01-27"
```

### DELETE /api/v1/bookings/{booking_id}

Отменить booking.

**Request:**
```json
{
  "booking_id": 456,
  "cancellation_reason": "Клиент перенес встречу"
}
```

**Curl example:**
```bash
curl -X DELETE "http://localhost:8000/api/v1/bookings/456" \
  -H "Content-Type: application/json" \
  -d '{
    "booking_id": 456,
    "cancellation_reason": "Клиент перенес встречу"
  }'
```

### PATCH /api/v1/bookings/{booking_id}

Перенести booking.

**Request:**
```json
{
  "booking_id": 456,
  "new_start_time": "2024-01-25T16:00:00Z",
  "reschedule_reason": "По просьбе клиента"
}
```

**Curl example:**
```bash
curl -X PATCH "http://localhost:8000/api/v1/bookings/456" \
  -H "Content-Type: application/json" \
  -d '{
    "booking_id": 456,
    "new_start_time": "2024-01-25T16:00:00Z",
    "reschedule_reason": "По просьбе клиента"
  }'
```

## Webhooks

Cal.com отправляет webhooks при изменении booking.

### Обрабатываемые события

**1. BOOKING_CREATED**
- Создан новый booking
- Lead status → `BOOKED`
- Обновляются `booking_id`, `booking_url`, `booked_at`

**2. BOOKING_RESCHEDULED**
- Booking перенесен
- Обновляется `booked_at`

**3. BOOKING_CANCELLED**
- Booking отменен
- Lead status → `QUALIFIED`
- Сохраняется история (booking_id остается)

**4. BOOKING_COMPLETED**
- Встреча завершена
- Lead status → `COMPLETED`

### Webhook URL

```
POST https://api.fast-lead.ru/webhooks/calcom
```

### Webhook Security

Webhook payload подписывается HMAC SHA256:

```python
import hmac
import hashlib

signature = hmac.new(
    webhook_secret.encode(),
    payload_bytes,
    hashlib.sha256
).hexdigest()
```

Signature передается в header `X-Cal-Signature`.

### Webhook Payload Example

```json
{
  "triggerEvent": "BOOKING_CREATED",
  "payload": {
    "id": 456,
    "uid": "abc123def",
    "title": "Консультация - 30 минут",
    "startTime": "2024-01-20T15:00:00Z",
    "endTime": "2024-01-20T15:30:00Z",
    "meetingUrl": "https://cal.com/meet/abc123def",
    "status": "accepted",
    "metadata": {
      "lead_id": 123,
      "tenant_id": 1
    }
  },
  "triggeredAt": "2024-01-15T12:00:00Z"
}
```

## Workflow

### Автоматический букинг qualified лида

```mermaid
1. Lead создан → status = NEW
2. SMS отправлен → status = CONTACTED
3. Клиент ответил → status = QUALIFIED
4. Celery создает booking:
   - Вызывает POST /api/v1/bookings
   - Cal.com создает встречу
   - Отправляет приглашение на email клиента
5. Lead обновлен → status = BOOKED
6. Webhook BOOKING_CREATED → подтверждение
7. Встреча прошла → Webhook BOOKING_COMPLETED
8. Lead → status = COMPLETED
```

### Ручной букинг через dashboard

```mermaid
1. Оператор открывает Lead в dashboard
2. Нажимает "Забронировать встречу"
3. Frontend вызывает POST /api/v1/bookings
4. Cal.com создает booking
5. Lead обновлен → status = BOOKED
6. Клиент получает email с ссылкой
```

## Тестирование

### 1. Тест создания booking

```bash
# Создайте тестовый lead
curl -X POST "http://localhost:8000/api/v1/leads" \
  -H "Content-Type: application/json" \
  -H "X-Tenant-Id: 1" \
  -d '{
    "name": "Тест Букинг",
    "email": "test@example.com",
    "phone": "+79991234567",
    "channel": "web",
    "consent": {"gdpr": true, "marketing": true}
  }'

# Запомните lead_id из ответа (например, 123)

# Создайте booking
curl -X POST "http://localhost:8000/api/v1/bookings" \
  -H "Content-Type: application/json" \
  -d '{
    "lead_id": 123,
    "name": "Тест Букинг",
    "email": "test@example.com"
  }'
```

### 2. Тест webhook

```bash
# Вручную отправьте webhook на ваш endpoint
curl -X POST "http://localhost:8000/webhooks/calcom" \
  -H "Content-Type: application/json" \
  -H "X-Cal-Signature: test-signature" \
  -d '{
    "triggerEvent": "BOOKING_CREATED",
    "payload": {
      "id": 456,
      "uid": "test123",
      "startTime": "2024-01-20T15:00:00Z",
      "endTime": "2024-01-20T15:30:00Z",
      "meetingUrl": "https://cal.com/meet/test123",
      "metadata": {"lead_id": 123}
    }
  }'
```

### 3. Проверка в базе

```sql
-- Проверьте Lead после booking
SELECT id, name, status, booking_id, booking_url, booked_at
FROM leads
WHERE id = 123;

-- Должно показать:
-- status = 'booked'
-- booking_id = '456'
-- booking_url = 'https://cal.com/meet/...'
```

## Troubleshooting

### Ошибка: Invalid API key

**Проблема:** Cal.com возвращает 401 Unauthorized

**Решение:**
1. Проверьте `CALCOM_API_KEY` в .env
2. Убедитесь, что API key начинается с `cal_live_` или `cal_test_`
3. Проверьте срок действия ключа в Cal.com settings

### Ошибка: Event type not found

**Проблема:** Cal.com возвращает 404

**Решение:**
1. Проверьте `CALCOM_EVENT_TYPE_ID` в .env
2. Убедитесь, что Event Type активен в Cal.com
3. Проверьте ID в URL event type

### Ошибка: No available slots

**Проблема:** Cal.com не может найти свободное время

**Решение:**
1. Проверьте вашу доступность в Cal.com
2. Убедитесь, что календарь подключен
3. Проверьте timezone

### Webhook не приходит

**Проблема:** События не обрабатываются

**Решение:**
1. Проверьте Webhook URL в Cal.com settings
2. Убедитесь, что URL доступен из интернета (ngrok для локальной разработки)
3. Проверьте логи webhook в Cal.com
4. Проверьте `CALCOM_WEBHOOK_SECRET`

## Production Deployment

### ngrok для локальной разработки

```bash
# Установите ngrok
brew install ngrok

# Запустите tunnel
ngrok http 8000

# Используйте ngrok URL в Cal.com webhook settings
https://abc123.ngrok.io/webhooks/calcom
```

### Production URL

В production используйте реальный домен:

```
https://api.fast-lead.ru/webhooks/calcom
```

Убедитесь, что:
- SSL certificate установлен
- URL доступен из интернета
- Firewall разрешает входящие запросы

## Ссылки

- Cal.com documentation: https://cal.com/docs
- Cal.com API reference: https://cal.com/docs/api-reference
- Cal.com webhook events: https://cal.com/docs/webhooks
- Fast Lead issues: https://github.com/CultureOrganica/fast_lead/issues
