# Setup Development Environment на Mac

Пошаговая инструкция для настройки окружения разработки на macOS 13+ (Ventura).

## Prerequisites

- macOS 13+ (Ventura или новее)
- Минимум 8 GB RAM (рекомендуется 16 GB)
- Минимум 20 GB свободного места на диске
- Интернет соединение

## Шаг 1: Установка Homebrew

Если Homebrew еще не установлен:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

Проверка:
```bash
brew --version
# Должно вывести версию, например: Homebrew 4.x.x
```

## Шаг 2: Установка Python 3.11

Используем pyenv для управления версиями Python:

```bash
# Установить pyenv
brew install pyenv

# Добавить в shell config (~/.zshrc для zsh или ~/.bash_profile для bash)
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.zshrc
echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.zshrc
echo 'eval "$(pyenv init --path)"' >> ~/.zshrc
echo 'eval "$(pyenv init -)"' >> ~/.zshrc

# Перезагрузить shell
source ~/.zshrc

# Установить Python 3.11
pyenv install 3.11.7

# Установить как global
pyenv global 3.11.7

# Проверка
python --version
# Должно вывести: Python 3.11.7
```

## Шаг 3: Установка PostgreSQL

```bash
# Установить PostgreSQL 14
brew install postgresql@14

# Добавить в PATH
echo 'export PATH="/opt/homebrew/opt/postgresql@14/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc

# Запустить PostgreSQL как сервис
brew services start postgresql@14

# Проверка
psql --version
# Должно вывести: psql (PostgreSQL) 14.x
```

### Создание базы данных для development

```bash
# Создать пользователя
createuser -s postgres

# Создать базу данных
createdb fast_lead_dev

# Проверить подключение
psql -U postgres -d fast_lead_dev -c "SELECT version();"
```

## Шаг 4: Установка Redis

```bash
# Установить Redis
brew install redis

# Запустить Redis как сервис
brew services start redis

# Проверка
redis-cli ping
# Должно вывести: PONG
```

## Шаг 5: Установка Node.js

Используем nvm для управления версиями Node.js:

```bash
# Установить nvm
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash

# Добавить в shell config
echo 'export NVM_DIR="$HOME/.nvm"' >> ~/.zshrc
echo '[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"' >> ~/.zshrc
source ~/.zshrc

# Установить Node.js 20 LTS
nvm install 20
nvm use 20
nvm alias default 20

# Проверка
node --version
# Должно вывести: v20.x.x

npm --version
# Должно вывести: 10.x.x
```

## Шаг 6: Клонирование репозитория

```bash
# Клонировать
git clone https://github.com/CultureOrganica/fast_lead.git
cd fast_lead
```

## Шаг 7: Backend Setup

### Создание virtual environment

```bash
cd backend

# Создать venv
python -m venv venv

# Активировать venv
source venv/bin/activate

# Обновить pip
pip install --upgrade pip

# Установить зависимости
pip install -r requirements-dev.txt
```

### Настройка environment variables

```bash
# Скопировать example
cp ../.env.example ../.env

# Отредактировать .env
nano ../.env
```

Заполните следующие переменные:
```env
# Database
DATABASE_URL=postgresql://postgres@localhost:5432/fast_lead_dev

# Redis
REDIS_URL=redis://localhost:6379/0

# Application
SECRET_KEY=your-secret-key-change-this-in-production
ENVIRONMENT=development
DEBUG=true

# API Keys (пока оставляем пустыми)
SMSC_API_KEY=
VK_ACCESS_TOKEN=
TELEGRAM_BOT_TOKEN=
```

### Запуск миграций

```bash
# Инициализация Alembic (первый раз)
alembic init alembic

# Создать первую миграцию
alembic revision -m "Initial schema"

# Применить миграции
alembic upgrade head
```

### Запуск dev сервера

```bash
# Запустить FastAPI
uvicorn app.main:app --reload --port 8000

# В браузере открыть:
# http://localhost:8000/docs - Swagger UI
# http://localhost:8000/redoc - ReDoc
```

### Запуск Celery worker (в отдельном терминале)

```bash
cd backend
source venv/bin/activate

celery -A app.worker worker --loglevel=info
```

## Шаг 8: Frontend Dashboard Setup

```bash
cd frontend/dashboard

# Установить зависимости
npm install

# Создать .env.local
echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local

# Запустить dev сервер
npm run dev

# Открыть в браузере:
# http://localhost:3000
```

## Шаг 9: Frontend Marketing Site Setup

```bash
cd frontend/marketing

# Установить зависимости
npm install

# Создать .env.local
echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local

# Запустить dev сервер
npm run dev --port 3001

# Открыть в браузере:
# http://localhost:3001
```

## Шаг 10: Widget Setup

```bash
cd frontend/widget

# Установить зависимости
npm install

# Создать .env
echo "VITE_API_URL=http://localhost:8000" > .env

# Запустить dev сервер
npm run dev

# Открыть в браузере:
# http://localhost:5173
```

## Проверка установки

После всех шагов у вас должно быть запущено:

1. **PostgreSQL** - `brew services list | grep postgresql`
2. **Redis** - `brew services list | grep redis`
3. **Backend API** - http://localhost:8000/docs
4. **Dashboard** - http://localhost:3000
5. **Marketing** - http://localhost:3001
6. **Widget** - http://localhost:5173

### Health Check

```bash
# Проверка Backend API
curl http://localhost:8000/health

# Должно вернуть:
# {"status": "healthy", "database": "connected", "redis": "connected"}
```

## Troubleshooting

### PostgreSQL не запускается

```bash
# Остановить сервис
brew services stop postgresql@14

# Проверить логи
tail -f /opt/homebrew/var/log/postgresql@14.log

# Перезапустить
brew services restart postgresql@14
```

### Redis не запускается

```bash
# Остановить сервис
brew services stop redis

# Проверить конфиг
redis-cli config get dir

# Перезапустить
brew services restart redis
```

### Python version conflicts

```bash
# Проверить текущую версию
python --version

# Переустановить версию через pyenv
pyenv install 3.11.7
pyenv global 3.11.7
```

### Port already in use

```bash
# Найти процесс на порту 8000
lsof -i :8000

# Убить процесс
kill -9 <PID>
```

## Автоматический setup

Для автоматизации всех шагов используйте скрипт:

```bash
./scripts/setup-mac.sh
```

Скрипт автоматически:
- Проверит все prerequisites
- Установит недостающие компоненты
- Настроит базы данных
- Создаст .env файлы
- Установит зависимости

## Next Steps

После успешной установки:

1. Ознакомьтесь с [docs/roadmap.md](roadmap.md)
2. Изучите [docs/tech-stack.md](tech-stack.md)
3. Прочитайте implementation plans в `docs/backlog/current/`
4. Начните разработку с Week 1 задач!

## Полезные команды

### Остановка всех сервисов

```bash
# Остановить PostgreSQL
brew services stop postgresql@14

# Остановить Redis
brew services stop redis

# Остановить FastAPI (Ctrl+C в терминале)
# Остановить Next.js (Ctrl+C в терминале)
```

### Очистка баз данных

```bash
# Дропнуть БД
dropdb fast_lead_dev

# Создать заново
createdb fast_lead_dev

# Запустить миграции
cd backend
alembic upgrade head
```

### Обновление зависимостей

```bash
# Backend
cd backend
pip install --upgrade -r requirements-dev.txt

# Frontend
cd frontend/dashboard
npm update

cd ../marketing
npm update

cd ../widget
npm update
```

## Production Deployment

Для production используем Docker (на сервере Linux):

```bash
# На сервере
git clone https://github.com/CultureOrganica/fast_lead.git
cd fast_lead

# Запуск через Docker Compose
docker-compose -f docker/docker-compose.prod.yml up -d
```

Подробнее: [docs/deployment.md](deployment.md)
