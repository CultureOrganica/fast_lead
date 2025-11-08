# WhatsApp Business API Integration

Руководство по настройке WhatsApp Business Cloud API для Fast Lead.

## Обзор

Fast Lead интегрируется с **WhatsApp Business Cloud API** от Meta для автоматической отправки сообщений клиентам через WhatsApp.

**Возможности:**
- ✅ Автоматическая отправка приветственных сообщений
- ✅ Поддержка текстовых сообщений
- ✅ Поддержка шаблонных сообщений (templates)
- ✅ Retry logic с exponential backoff
- ✅ Асинхронная обработка через Celery

---

## Prerequisites

1. **Meta Business Account** - https://business.facebook.com
2. **WhatsApp Business App** в Meta Business Suite
3. **Verified Business** (для production использования)
4. **Phone Number** - номер телефона для WhatsApp Business

---

## Настройка WhatsApp Business API

### Шаг 1: Создание приложения в Meta для разработчиков

1. Перейдите на https://developers.facebook.com/apps
2. Нажмите **Create App**
3. Выберите тип **Business**
4. Заполните информацию о приложении:
   - **App Name:** Fast Lead WhatsApp
   - **App Contact Email:** ваш email
   - **Business Account:** выберите ваш Business Account

### Шаг 2: Добавление WhatsApp продукта

1. В разделе **Add Products to Your App** найдите **WhatsApp**
2. Нажмите **Set Up**
3. Выберите ваш Business Account

### Шаг 3: Получение токена доступа

1. Перейдите в **WhatsApp > Getting Started**
2. Скопируйте **Temporary Access Token** (действует 24 часа)
3. Для production создайте **System User** и получите постоянный токен:
   - Перейдите в **Business Settings > System Users**
   - Создайте нового System User
   - Назначьте роль **Admin**
   - Сгенерируйте токен с правами `whatsapp_business_messaging`

### Шаг 4: Получение Phone Number ID

1. В разделе **WhatsApp > API Setup**
2. Найдите **Phone Number ID** (начинается с цифр, например: `123456789012345`)
3. Скопируйте этот ID

### Шаг 5: Настройка номера телефона

1. В разделе **WhatsApp > Phone Numbers**
2. Добавьте номер телефона или используйте тестовый номер
3. Для production:
   - Верифицируйте ваш бизнес
   - Добавьте настоящий номер телефона
   - Пройдите процесс одобрения

---

## Конфигурация Fast Lead

### Environment Variables

Добавьте следующие переменные в `.env`:

```bash
# WhatsApp Business API
WHATSAPP_ACCESS_TOKEN=your-permanent-access-token
WHATSAPP_PHONE_NUMBER_ID=123456789012345
WHATSAPP_API_VERSION=v18.0
WHATSAPP_VERIFY_TOKEN=your-random-verify-token-for-webhooks

# Feature flag
FEATURE_WHATSAPP_ENABLED=true
```

**Важно:**
- `WHATSAPP_ACCESS_TOKEN` - постоянный токен от System User (не temporary!)
- `WHATSAPP_PHONE_NUMBER_ID` - ID номера телефона из API Setup
- `WHATSAPP_VERIFY_TOKEN` - случайная строка для верификации webhooks (минимум 20 символов)

### Генерация Verify Token

```bash
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

---

## Тестирование интеграции

### Тест 1: Отправка простого сообщения

```bash
curl -X POST http://localhost:8000/api/v1/leads \
  -H "Content-Type: application/json" \
  -H "X-Tenant-Id: 1" \
  -d '{
    "name": "Иван Петров",
    "phone": "+79991234567",
    "channel": "whatsapp",
    "consent": {
      "gdpr": true,
      "marketing": true
    }
  }'
```

**Что происходит:**
1. Lead создается в БД со статусом `NEW`
2. Celery task `process_new_lead` запускается
3. WhatsApp Service отправляет приветственное сообщение
4. Статус обновляется на `CONTACTED`

### Тест 2: Проверка Celery логов

```bash
# В терминале где запущен Celery worker
./run_celery_worker.sh
```

Вы должны увидеть:
```
[INFO] Processing WhatsApp lead: 123
[INFO] WhatsApp message sent to 79991234567: {'success': True, 'message_id': 'wamid.XXX'}
[INFO] Task process_new_lead succeeded
```

### Тест 3: Прямая отправка через Python

```python
import asyncio
from app.services.whatsapp_service import WhatsAppService

async def test_whatsapp():
    service = WhatsAppService()

    result = await service.send_message(
        to="79991234567",  # Без '+' в начале
        message="Тестовое сообщение из Fast Lead"
    )

    print(result)

# Запустить
asyncio.run(test_whatsapp())
```

---

## Шаблонные сообщения (Templates)

WhatsApp требует предварительного одобрения шаблонов для отправки сообщений.

### Создание шаблона

1. Перейдите в **WhatsApp > Message Templates**
2. Нажмите **Create Template**
3. Заполните:
   - **Name:** `welcome_message`
   - **Category:** `MARKETING` или `UTILITY`
   - **Language:** `Russian`
   - **Content:** Текст с переменными `{{1}}`, `{{2}}` и т.д.

Пример шаблона:
```
Здравствуйте, {{1}}!

Спасибо за обращение в Fast Lead. Мы получили ваш запрос и свяжемся с вами в ближайшее время.

С уважением,
Команда Fast Lead
```

### Отправка шаблонного сообщения

```python
from app.services.whatsapp_service import WhatsAppService

service = WhatsAppService()

result = await service.send_template_message(
    to="79991234567",
    template_name="welcome_message",
    language_code="ru",
    components=[
        {
            "type": "body",
            "parameters": [
                {
                    "type": "text",
                    "text": "Иван Петров"  # Значение для {{1}}
                }
            ]
        }
    ]
)
```

---

## Webhooks (опционально)

Для получения входящих сообщений и статусов доставки.

### Настройка Webhook URL

1. В разделе **WhatsApp > Configuration**
2. Добавьте **Callback URL:**
   ```
   https://yourdomain.com/webhooks/whatsapp
   ```
3. **Verify Token:** используйте значение из `WHATSAPP_VERIFY_TOKEN`
4. Подпишитесь на события:
   - `messages` - входящие сообщения
   - `message_status` - статусы доставки

### Endpoint для webhooks (уже реализован)

```python
# backend/app/api/v1/webhooks.py
@router.post("/webhooks/whatsapp")
async def whatsapp_webhook(request: Request):
    """Handle WhatsApp webhook events."""
    # Обработка входящих сообщений
    pass

@router.get("/webhooks/whatsapp")
async def whatsapp_webhook_verify(
    hub_mode: str = Query(..., alias="hub.mode"),
    hub_verify_token: str = Query(..., alias="hub.verify_token"),
    hub_challenge: str = Query(..., alias="hub.challenge"),
):
    """Verify webhook URL with Meta."""
    if hub_mode == "subscribe" and hub_verify_token == settings.whatsapp_verify_token:
        return PlainTextResponse(hub_challenge)
    raise HTTPException(status_code=403, detail="Invalid verify token")
```

---

## Ограничения и лимиты

### Tier System (уровни доступа)

Meta использует систему Tier для ограничения количества сообщений:

| Tier | Conversations/Day | Требования |
|------|-------------------|----------|
| Tier 1 | 1,000 | По умолчанию |
| Tier 2 | 10,000 | Хорошая история отправок |
| Tier 3 | 100,000 | Верифицированный бизнес |
| Unlimited | Без лимита | Official Business Account |

### Rate Limits

- **80 сообщений в секунду** (на Phone Number ID)
- **40 API вызовов в секунду** (на приложение)

### Ограничения контента

- Максимум **4096 символов** в сообщении
- Поддерживаемые типы: text, image, audio, video, document, location
- Emojis поддерживаются ✅

---

## Стоимость

### Business-Initiated Conversations

- **Первые 1,000 разговоров/месяц:** Бесплатно
- **Далее:** ~$0.04 - $0.10 за разговор (зависит от страны)

### User-Initiated Conversations

- **Бесплатно** (если клиент написал первым)
- **24-часовое окно** для бесплатных ответов

**Россия:** ~$0.08 за business-initiated conversation

---

## Troubleshooting

### Ошибка: "Access token is invalid"

**Решение:**
1. Проверьте что используете **постоянный токен** (от System User)
2. Убедитесь что токен имеет права `whatsapp_business_messaging`
3. Сгенерируйте новый токен если истёк срок

### Ошибка: "Phone number not found"

**Решение:**
1. Проверьте `WHATSAPP_PHONE_NUMBER_ID` (должен быть ID, не номер телефона!)
2. Убедитесь что номер добавлен в WhatsApp Business App
3. Номер должен быть верифицирован

### Ошибка: "Recipient phone number not valid"

**Решение:**
1. Используйте формат **без '+'**: `79991234567`
2. Номер должен быть в международном формате
3. Для тестирования добавьте номер в список тестовых номеров

### Сообщения не доставляются

**Проверьте:**
1. Celery worker запущен и работает
2. В логах нет ошибок WhatsApp API
3. Номер получателя добавлен в тестовые (для development)
4. Ваш Tier не исчерпан (проверьте Business Manager)

---

## Production Checklist

Перед запуском в production:

- [ ] Business Account верифицирован в Meta
- [ ] Создан System User с постоянным токеном
- [ ] Настроен реальный номер телефона (не тестовый)
- [ ] Все шаблоны сообщений одобрены Meta
- [ ] Webhooks настроены и работают
- [ ] SSL сертификат настроен для webhook URL
- [ ] Мониторинг настроен (логи, метрики)
- [ ] Rate limiting учтен в коде
- [ ] Проверен Tier и лимиты отправок

---

## Полезные ссылки

- **Official Docs:** https://developers.facebook.com/docs/whatsapp/cloud-api
- **API Reference:** https://developers.facebook.com/docs/whatsapp/cloud-api/reference
- **Message Templates:** https://developers.facebook.com/docs/whatsapp/business-management-api/message-templates
- **Pricing:** https://developers.facebook.com/docs/whatsapp/pricing
- **Support:** https://developers.facebook.com/support/

---

## Пример полного workflow

```bash
# 1. Клиент заполняет форму на сайте
# 2. Widget отправляет POST /api/v1/leads
curl -X POST http://localhost:8000/api/v1/leads \
  -H "Content-Type: application/json" \
  -H "X-Tenant-Id: 1" \
  -d '{
    "name": "Анна Козлова",
    "phone": "+79991234572",
    "channel": "whatsapp",
    "source": "https://example.com/landing",
    "consent": {"gdpr": true, "marketing": true}
  }'

# 3. Lead создается в БД
# 4. Celery task process_new_lead запускается
# 5. WhatsApp Service отправляет приветствие
# 6. Клиент получает сообщение в WhatsApp
# 7. Оператор видит лида в Dashboard
# 8. Оператор квалифицирует и бронирует встречу
```

Готово! 🎉
