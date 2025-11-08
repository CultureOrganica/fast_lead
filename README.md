# Fast Lead - Омниканальный Appointment Setter

SaaS-платформа для автоматизации записи клиентов через мессенджеры, SMS, Email и социальные сети.

## 🚀 Быстрый старт

### Текущее состояние проекта

**Реализовано (Week 1-2):**
- ✅ Backend FastAPI с async SQLAlchemy
- ✅ Public API для создания лидов
- ✅ Встраиваемый виджет (Vite + TypeScript)
- ✅ SMS интеграция через SMSC.ru
- ✅ Celery orchestrator для асинхронной обработки

**Полная инструкция по тестированию:** [TESTING.md](TESTING.md)

### Для разработчиков на Mac

**Prerequisites:**
- macOS 13+ (Ventura)
- PostgreSQL 14
- Redis 6
- Python 3.11+
- Node.js 20 LTS

**Quick Setup:**
```bash
# 1. Клонируем репозиторий
git clone https://github.com/CultureOrganica/fast_lead.git
cd fast_lead

# 2. Переключаемся на dev ветку
git checkout claude/setup-repo-access-011CUuLgKyDBqkv4FYPgtUpp

# 3. Backend setup
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Отредактируйте .env

# 4. Проверка
python check_imports.py
python create_migration.py
alembic upgrade head

# 5. Запуск
uvicorn app.main:app --reload  # Terminal 1
./run_celery_worker.sh         # Terminal 2

# 6. Widget (отдельный терминал)
cd widget
npm install
npm run dev
```

**Подробные инструкции:**
- [TESTING.md](TESTING.md) - Полное руководство по тестированию
- [docs/setup-mac.md](docs/setup-mac.md) - Setup для Mac
- [backend/docs/SMS_INTEGRATION.md](backend/docs/SMS_INTEGRATION.md) - SMS интеграция

## 📁 Структура проекта

```
fast_lead/
├── backend/          # Python FastAPI backend
│   ├── app/          # Код приложения
│   ├── tests/        # Тесты
│   └── alembic/      # Database миграции
├── frontend/         # Frontend приложения
│   ├── dashboard/    # Next.js dashboard (личный кабинет)
│   ├── marketing/    # Next.js marketing site (landing)
│   └── widget/       # Виджет (Vite + TS)
├── docker/           # Docker конфиги (только для production)
├── docs/             # Документация
└── scripts/          # Скрипты для разработки
```

## 🛠 Tech Stack

**Backend:**
- Python 3.11 + FastAPI
- PostgreSQL 14 + SQLAlchemy 2.0
- Redis 6 + Celery
- Pytest

**Frontend:**
- Next.js 14 + React 18 + TypeScript
- Tailwind CSS + shadcn/ui
- Zustand + TanStack Query

**Infrastructure:**
- Docker (production only)
- Nginx
- Cloudflare CDN

**Каналы:**
- SMS: SMSC.ru
- Email: SMTP/Postal
- VK: VK Bots API
- Telegram: Bot API
- WhatsApp: Business API
- MAX: Bot API

Полное описание: [docs/tech-stack.md](docs/tech-stack.md)

## 📋 Roadmap

**MVP Phase 1** (Week 1-3): Infrastructure + Basic Widget + SMS
**MVP Phase 2** (Week 4-6): Platform Frontend + More Channels + Billing
**Beta** (Week 7-10): Polish + Testing + Chatwoot
**GA** (Week 11-12): Launch + Marketing

Детальный roadmap: [docs/roadmap.md](docs/roadmap.md)

## 🏗 Development

### Backend

```bash
cd backend

# Активировать venv
source venv/bin/activate

# Установить зависимости
pip install -r requirements-dev.txt

# Запустить миграции
alembic upgrade head

# Запустить dev сервер
uvicorn app.main:app --reload --port 8000
```

### Frontend Dashboard

```bash
cd frontend/dashboard

# Установить зависимости
npm install

# Запустить dev сервер
npm run dev
```

### Widget

```bash
cd frontend/widget

# Установить зависимости
npm install

# Запустить dev сервер
npm run dev
```

## 🧪 Testing

```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend/dashboard
npm test
```

## 📚 Documentation

- [Tech Stack](docs/tech-stack.md) - выбор технологий
- [Roadmap](docs/roadmap.md) - план разработки
- [Setup Mac](docs/setup-mac.md) - настройка для Mac
- [Widget Implementation Plan](docs/backlog/current/01-FEAT-omnichannel-widget/impl/IP-01-omnichannel-widget.md)
- [Platform Implementation Plan](docs/backlog/current/02-FEAT-platform-frontend/impl/IP-01-platform-web-app.md)

## 🔐 Environment Variables

Скопируйте `.env.example` в `.env` и заполните:

```bash
cp .env.example .env
```

Требуемые переменные:
- `DATABASE_URL` - PostgreSQL connection string
- `REDIS_URL` - Redis connection string
- `SECRET_KEY` - для JWT токенов
- `SMSC_API_KEY` - для SMS
- `VK_ACCESS_TOKEN` - для VK API
- и другие (см. .env.example)

## 🤝 Contributing

1. Создайте feature branch (`git checkout -b feature/amazing-feature`)
2. Коммитьте изменения (`git commit -m 'Add amazing feature'`)
3. Пушьте в branch (`git push origin feature/amazing-feature`)
4. Откройте Pull Request

## 📄 License

Proprietary - Culture Organica © 2025

## 🆘 Support

- Email: support@fast-lead.ru
- Telegram: @fastlead_support
- Docs: https://docs.fast-lead.ru
