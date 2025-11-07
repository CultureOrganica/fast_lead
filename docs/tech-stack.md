# Technology Stack - Fast Lead

Выбор технологического стека с фокусом на зрелые, надежные open source решения с коммерческими лицензиями.

## Критерии выбора

1. **Зрелость** - production-ready, проверенные решения
2. **Open Source** - коммерческие лицензии (MIT, Apache 2.0, BSD)
3. **Активное сообщество** - регулярные обновления, поддержка
4. **Документация** - качественная документация на английском/русском
5. **Производительность** - оптимизация для высоких нагрузок

## Backend Stack

### Core

| Технология | Версия | Лицензия | Назначение |
|------------|--------|----------|------------|
| **Python** | 3.11+ | PSF | Основной язык backend |
| **FastAPI** | 0.104+ | MIT | Web framework, REST API |
| **Uvicorn** | 0.24+ | BSD | ASGI сервер |
| **Pydantic** | 2.5+ | MIT | Валидация данных |

**Обоснование:**
- Python - зрелый язык с огромной экосистемой
- FastAPI - современный, быстрый, async, автодокументация (OpenAPI/Swagger)
- Uvicorn - производительный ASGI сервер
- Pydantic - type-safe валидация и сериализация

### Database

| Технология | Версия | Лицензия | Назначение |
|------------|--------|----------|------------|
| **PostgreSQL** | 14+ | PostgreSQL License (BSD-style) | Основная БД |
| **SQLAlchemy** | 2.0+ | MIT | ORM |
| **Alembic** | 1.12+ | MIT | Database миграции |
| **asyncpg** | 0.29+ | Apache 2.0 | Async PostgreSQL драйвер |
| **Redis** | 6+ | BSD 3-Clause | Cache, sessions, queues |
| **redis-py** | 5.0+ | MIT | Redis клиент |

**Обоснование:**
- PostgreSQL - самая надежная open source БД
- SQLAlchemy 2.0 - зрелая ORM с async support
- Alembic - стандарт для миграций
- asyncpg - самый быстрый async драйвер для Postgres
- Redis - проверенное решение для cache и queues

### Task Queue

| Технология | Версия | Лицензия | Назначение |
|------------|--------|----------|------------|
| **Celery** | 5.3+ | BSD | Распределенная очередь задач |
| **Redis** | 6+ | BSD 3-Clause | Broker для Celery |

**Альтернатива:**
- **Dramatiq** (LGPL 3.0) - более легковесный, но менее функциональный

**Обоснование:**
- Celery - индустриальный стандарт для Python
- Проверен временем, большое сообщество
- Поддержка retry, scheduling, monitoring

### Authentication

| Технология | Версия | Лицензия | Назначение |
|------------|--------|----------|------------|
| **PyJWT** | 2.8+ | MIT | JWT токены |
| **passlib** | 1.7+ | BSD | Хэширование паролей (bcrypt) |
| **python-jose** | 3.3+ | MIT | JWT/JWS/JWK |

**Обоснование:**
- PyJWT - стандарт для JWT в Python
- passlib - надежное хэширование паролей
- Все с MIT/BSD лицензиями

## Frontend Stack

### Core

| Технология | Версия | Лицензия | Назначение |
|------------|--------|----------|------------|
| **Next.js** | 14+ | MIT | React framework (SSR/SSG) |
| **React** | 18+ | MIT | UI library |
| **TypeScript** | 5+ | Apache 2.0 | Type safety |
| **Node.js** | 20 LTS | MIT | Runtime |

**Обоснование:**
- Next.js - лучший выбор для SEO (SSR/SSG)
- React - индустриальный стандарт
- TypeScript - type safety, лучший DX
- Node.js LTS - стабильность

### UI & Styling

| Технология | Версия | Лицензия | Назначение |
|------------|--------|----------|------------|
| **Tailwind CSS** | 3.4+ | MIT | Utility-first CSS |
| **shadcn/ui** | latest | MIT | Готовые компоненты |
| **Radix UI** | latest | MIT | Headless компоненты |
| **Lucide React** | latest | ISC | Иконки |

**Обоснование:**
- Tailwind - быстрая разработка, оптимизация размера
- shadcn/ui - качественные компоненты, можно кастомизировать
- Radix UI - accessibility из коробки
- Lucide - современные иконки

### State & Data Fetching

| Технология | Версия | Лицензия | Назначение |
|------------|--------|----------|------------|
| **Zustand** | 4.4+ | MIT | State management |
| **TanStack Query** | 5+ | MIT | Data fetching & caching |
| **Axios** | 1.6+ | MIT | HTTP клиент |

**Обоснование:**
- Zustand - простой, легковесный state manager
- TanStack Query (React Query) - лучшее решение для server state
- Axios - проверенный HTTP клиент

### Forms & Validation

| Технология | Версия | Лицензия | Назначение |
|------------|--------|----------|------------|
| **React Hook Form** | 7.48+ | MIT | Forms management |
| **Zod** | 3.22+ | MIT | Schema validation |

**Обоснование:**
- React Hook Form - производительный, минимум ререндеров
- Zod - type-safe валидация, интеграция с TypeScript

### Charts & Analytics

| Технология | Версия | Лицензия | Назначение |
|------------|--------|----------|------------|
| **Recharts** | 2.10+ | MIT | Charts library |

**Альтернатива:**
- **Apache ECharts** (Apache 2.0) - более мощный, но тяжелее

**Обоснование:**
- Recharts - простой API, React-friendly
- Легковесный, достаточно для MVP

## Widget (Frontend)

### Core

| Технология | Версия | Лицензия | Назначение |
|------------|--------|----------|------------|
| **Vanilla JS** или **Preact** | ES6+ / 10+ | - / MIT | Легковесный виджет |
| **TypeScript** | 5+ | Apache 2.0 | Type safety |
| **Vite** | 5+ | MIT | Build tool |

**Обоснование:**
- Vanilla JS - минимальный размер, нет зависимостей
- Preact - если нужен React-like, но в 3kb
- Vite - быстрый build, HMR
- TypeScript - для разработки, минифицируется в JS

## Infrastructure

### Containerization & Orchestration

| Технология | Версия | Лицензия | Назначение |
|------------|--------|----------|------------|
| **Docker** | 24+ | Apache 2.0 | Контейнеризация |
| **Docker Compose** | 2.23+ | Apache 2.0 | Local development |

**Опционально для production:**
- **Kubernetes** (Apache 2.0) - если нужна оркестрация

**Обоснование:**
- Docker - стандарт индустрии
- Docker Compose - простота для development и малых деплоев

### Web Server & Reverse Proxy

| Технология | Версия | Лицензия | Назначение |
|------------|--------|----------|------------|
| **Nginx** | 1.24+ | BSD-like | Reverse proxy, static files |

**Обоснование:**
- Nginx - проверенный временем, производительный
- BSD лицензия - коммерческое использование без проблем

### Storage

| Технология | Версия | Лицензия | Назначение |
|------------|--------|----------|------------|
| **MinIO** | latest | AGPL v3 / Commercial | S3-compatible object storage |

**Альтернатива:**
- Использовать через API (AGPL не проблема для API usage)
- Или облачные S3 (Selectel, VK Cloud, AWS S3)

**Обоснование:**
- MinIO - S3-compatible, можно self-host
- AGPL только для модификации кода, API usage ok

### CDN

| Технология | Лицензия | Назначение |
|------------|----------|------------|
| **Cloudflare** | Commercial | CDN, DDoS protection |

**Российские альтернативы:**
- **Selectel CDN** - российский провайдер
- **VK CDN** - от VK

**Обоснование:**
- Cloudflare - лидер рынка, бесплатный тариф
- Российские CDN - для локализации и соответствия требованиям

## Monitoring & Observability

### Metrics

| Технология | Версия | Лицензия | Назначение |
|------------|--------|----------|------------|
| **Prometheus** | 2.47+ | Apache 2.0 | Метрики |
| **Grafana** | 10+ | AGPL v3 / Commercial | Визуализация |

**Обоснование:**
- Prometheus - стандарт для метрик
- Grafana - лучшие дашборды (AGPL ok для usage)

### Logging

| Технология | Версия | Лицензия | Назначение |
|------------|--------|----------|------------|
| **structlog** | 23+ | MIT / Apache 2.0 | Structured logging |
| **Python logging** | stdlib | PSF | Базовое логирование |

**Обоснование:**
- structlog - structured logs, легко парсить
- Встроенное logging - для простых случаев

### Tracing (опционально)

| Технология | Версия | Лицензия | Назначение |
|------------|--------|----------|------------|
| **OpenTelemetry** | 1.21+ | Apache 2.0 | Distributed tracing |

**Обоснование:**
- OpenTelemetry - индустриальный стандарт
- Интеграция с Grafana/Jaeger

## Channels Integration

### Communication Providers

| Канал | Провайдер | API | Лицензия SDK |
|-------|-----------|-----|--------------|
| **SMS** | SMSC.ru | REST API | Proprietary (ok for API usage) |
| **Email** | SMTP / Postal | SMTP / REST | - / AGPL v3 |
| **VK** | VK API | REST API | Proprietary (ok for API usage) |
| **Telegram** | Telegram Bot API | REST API | - |
| **WhatsApp** | WhatsApp Business API | REST API | Proprietary (ok for API usage) |
| **MAX** | MAX API | REST API | Proprietary (ok for API usage) |

**Обоснование:**
- SMSC.ru - надежный российский SMS провайдер
- VK API - бесплатное API для ботов и сообщений
- Telegram Bot API - бесплатное, стабильное
- WhatsApp Business API - через партнеров (платно)

### Calendar & Booking

| Технология | API | Лицензия |
|------------|-----|----------|
| **Cal.com** | REST API | AGPLv3 / Commercial |

**Обоснование:**
- Cal.com - open source, можно self-host
- AGPL ok для API usage, или можно купить коммерческую лицензию

### Inbox

| Технология | API | Лицензия |
|------------|-----|----------|
| **Chatwoot** | REST API | MIT |

**Альтернатива:**
- **Rocket.Chat** (MIT)

**Обоснование:**
- Chatwoot - open source, MIT лицензия
- Self-host или cloud
- Хорошая интеграция с каналами

## Billing & Payments

### Payment Providers

| Провайдер | SDK | Лицензия |
|-----------|-----|----------|
| **ЮКасса** | Python SDK | Proprietary (ok for API usage) |
| **Тинькофф Acquiring** | REST API | Proprietary (ok for API usage) |

**Обоснование:**
- ЮКасса - популярный, надежный, работает с ИП
- Тинькофф - альтернатива, хорошее API
- Оба подходят для российского рынка

## Development Tools

### Code Quality

| Технология | Версия | Лицензия | Назначение |
|------------|--------|----------|------------|
| **Black** | 23+ | MIT | Code formatter (Python) |
| **Ruff** | 0.1+ | MIT | Linter (Python) |
| **mypy** | 1.7+ | MIT | Type checker (Python) |
| **ESLint** | 8+ | MIT | Linter (JS/TS) |
| **Prettier** | 3+ | MIT | Code formatter (JS/TS) |

**Обоснование:**
- Black - стандарт для Python форматирования
- Ruff - быстрый linter, заменяет flake8/isort
- mypy - type checking для Python
- ESLint + Prettier - стандарт для JS/TS

### Testing

| Технология | Версия | Лицензия | Назначение |
|------------|--------|----------|------------|
| **pytest** | 7+ | MIT | Testing framework (Python) |
| **pytest-asyncio** | 0.21+ | Apache 2.0 | Async tests |
| **httpx** | 0.25+ | BSD | HTTP client для тестов |
| **Vitest** | 1+ | MIT | Testing framework (JS/TS) |
| **Playwright** | 1.40+ | Apache 2.0 | E2E testing |

**Обоснование:**
- pytest - де-факто стандарт для Python
- Vitest - быстрый, Vite-native
- Playwright - лучший E2E фреймворк (от Microsoft)

### CI/CD

| Технология | Лицензия | Назначение |
|------------|----------|------------|
| **GitHub Actions** | - | CI/CD pipeline |

**Альтернатива:**
- **GitLab CI** - если используете GitLab

**Обоснование:**
- GitHub Actions - интеграция с репозиторием
- Бесплатно для open source и малых проектов

## Environment & Configuration

### Environment Management

| Технология | Версия | Лицензия | Назначение |
|------------|--------|----------|------------|
| **python-dotenv** | 1.0+ | BSD | .env файлы |
| **Pydantic Settings** | 2.1+ | MIT | Settings management |

**Обоснование:**
- python-dotenv - простое управление .env
- Pydantic Settings - type-safe конфигурация

## Security

### Secrets Management

**Production:**
- **HashiCorp Vault** (MPL 2.0) - для production
- Или облачные решения (AWS Secrets Manager, VK Cloud)

**Development:**
- .env файлы (не коммитить в git)

### SSL/TLS

- **Let's Encrypt** (бесплатные сертификаты)
- **Certbot** (Apache 2.0) - для автоматизации

## Deployment Architecture

### Recommended Setup

```
Cloudflare CDN
    |
    v
Nginx (reverse proxy)
    |
    +-- Static files (Next.js, Widget)
    +-- FastAPI (Uvicorn) x N (горизонтальное масштабирование)
    +-- Celery workers x M
    |
    v
PostgreSQL (primary + read replicas)
Redis (cache + queue)
MinIO / S3 (media storage)
```

## Summary

### Полный стек:

**Backend:**
- Python 3.11 + FastAPI + Uvicorn
- PostgreSQL + SQLAlchemy + Alembic
- Redis + Celery
- PyJWT + passlib

**Frontend:**
- Next.js 14 + React 18 + TypeScript
- Tailwind CSS + shadcn/ui
- Zustand + TanStack Query
- React Hook Form + Zod

**Widget:**
- Vanilla JS (или Preact) + TypeScript + Vite

**Infrastructure:**
- Docker + Docker Compose
- Nginx
- Prometheus + Grafana
- Cloudflare CDN

**Channels:**
- SMSC.ru (SMS)
- VK API
- Telegram Bot API
- WhatsApp Business API
- SMTP / Postal (Email)

**Billing:**
- ЮКасса + Тинькофф

**Tools:**
- pytest + Vitest + Playwright
- Black + Ruff + ESLint + Prettier
- GitHub Actions

### Все лицензии коммерчески friendly:
- MIT
- Apache 2.0
- BSD
- PostgreSQL License
- PSF (Python)
- AGPL (только для usage через API, не модификация)

### Общая оценка:
✅ Все решения зрелые и production-ready
✅ Активные сообщества и регулярные обновления
✅ Отличная документация
✅ Коммерческое использование без проблем
✅ Масштабируемость из коробки
✅ Подходят для российского рынка
