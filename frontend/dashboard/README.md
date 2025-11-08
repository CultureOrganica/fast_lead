# Fast Lead Dashboard

Операторский интерфейс для управления лидами Fast Lead на Next.js 14 с TypeScript и Tailwind CSS.

## Возможности

- ✅ **Dashboard Overview** - статистика и последние лиды
- ✅ **Leads Management** - список лидов с фильтрацией по каналам
- ✅ **Analytics** - эффективность каналов и метрики
- ✅ **Settings** - конфигурация каналов
- ✅ **React Query** - кэширование и автообновление данных
- ✅ **Tailwind CSS** - адаптивный дизайн

## Tech Stack

- **Next.js 14.0.4** - App Router
- **React 18.2** - UI library
- **TypeScript 5.3.3** - type safety
- **Tailwind CSS 3.3.6** - styling
- **React Query (TanStack)** - data fetching
- **Axios** - HTTP client
- **date-fns** - date formatting

## Quick Start

### 1. Install dependencies

```bash
cd frontend/dashboard
npm install
```

### 2. Configure environment

```bash
cp .env.local.example .env.local
```

Edit `.env.local`:
```bash
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
NEXT_PUBLIC_TENANT_ID=1
```

### 3. Start development server

```bash
npm run dev
```

Dashboard will be available at **http://localhost:3000**

## Project Structure

```
frontend/dashboard/
├── app/                    # Next.js 14 App Router
│   ├── layout.tsx          # Root layout
│   ├── page.tsx            # Dashboard overview page
│   ├── providers.tsx       # React Query provider
│   ├── globals.css         # Global styles
│   ├── leads/
│   │   └── page.tsx        # Leads list page
│   ├── analytics/
│   │   └── page.tsx        # Analytics page
│   └── settings/
│       └── page.tsx        # Settings page
├── components/             # React components
│   ├── Sidebar.tsx         # Navigation sidebar
│   └── LeadsTable.tsx      # Leads table with filters
├── lib/                    # Utilities
│   ├── api.ts              # API client (axios)
│   ├── types.ts            # TypeScript types
│   └── utils.ts            # Helper functions
├── package.json            # Dependencies
├── tsconfig.json           # TypeScript config
├── tailwind.config.ts      # Tailwind config
└── next.config.js          # Next.js config
```

## API Integration

Dashboard интегрируется с Fast Lead backend API:

### Authentication

JWT токен сохраняется в `localStorage` и автоматически добавляется ко всем запросам:

```typescript
// Stored in localStorage
const token = localStorage.getItem('token')

// Automatically added to requests via axios interceptor
headers: {
  Authorization: `Bearer ${token}`
}
```

### API Endpoints Used

**Leads:**
- `GET /api/v1/leads` - получить список лидов
- `GET /api/v1/leads/{id}` - получить лид по ID
- `POST /api/v1/leads` - создать лид
- `PATCH /api/v1/leads/{id}/status` - обновить статус

**Bookings:**
- `POST /api/v1/bookings` - создать букинг
- `GET /api/v1/bookings/availability` - получить доступные слоты

### Example Usage

```typescript
import { leadsApi } from '@/lib/api'

// Get leads with pagination
const data = await leadsApi.getAll({
  skip: 0,
  limit: 20,
  channel: 'sms'
})

// Create new lead
const lead = await leadsApi.create({
  name: 'Иван Петров',
  phone: '+79991234567',
  channel: 'sms',
  consent: { gdpr: true, marketing: true }
})
```

## Pages

### 1. Dashboard Overview (`/`)

Главная страница с:
- 4 основные метрики (новые лиды, в обработке, встречи, конверсия)
- Последние лиды (10 шт)
- Quick actions (быстрые переходы)

### 2. Leads (`/leads`)

Управление лидами:
- Таблица со всеми лидами
- Фильтрация по каналам (SMS, Email, WhatsApp, Telegram, VK, Web)
- Пагинация (20 записей на страницу)
- Статусы (новый, контакт, квалифицирован, встреча, завершен и т.д.)
- Действия (открыть, редактировать)

### 3. Analytics (`/analytics`)

Статистика каналов:
- Общие метрики (всего лидов, конверсия, среднее время, рост)
- Эффективность каждого канала
- Визуализация данных

### 4. Settings (`/settings`)

Настройки:
- Конфигурация каналов (toggle вкл/выкл)
- Tenant информация
- Ссылки на документацию

## Development

### Type Safety

Все данные типизированы:

```typescript
// lib/types.ts
export interface Lead {
  id: number
  name: string
  phone?: string
  email?: string
  channel: Channel
  status: LeadStatus
  created_at: string
  // ...
}
```

### React Query

Автоматическое кэширование и refetch:

```typescript
const { data, isLoading, error } = useQuery({
  queryKey: ['leads', page, channel],
  queryFn: () => leadsApi.getAll({ skip: page * limit, limit, channel }),
})
```

### Tailwind CSS

Utility-first styling с кастомной темой:

```typescript
// tailwind.config.ts
theme: {
  extend: {
    colors: {
      primary: {
        500: '#0ea5e9',
        600: '#0284c7',
        // ...
      },
    },
  },
}
```

## Build & Deploy

### Production Build

```bash
npm run build
npm start
```

### Type Check

```bash
npm run type-check
```

### Lint

```bash
npm run lint
```

## Environment Variables

**Required:**
- `NEXT_PUBLIC_API_URL` - Backend API URL (default: `http://localhost:8000/api/v1`)

**Optional:**
- `NEXT_PUBLIC_TENANT_ID` - Tenant ID (default: `1`)
- `NEXT_PUBLIC_APP_NAME` - App name (default: `Fast Lead Dashboard`)

## Authentication

Текущая версия использует упрощенную схему:
- JWT токен из `localStorage`
- Auto-redirect на `/login` при 401

В production рекомендуется:
- Добавить страницу логина
- Implement refresh tokens
- Secure cookies вместо localStorage
- Role-based access control (RBAC)

## Future Enhancements

- [ ] Real-time updates (WebSocket/SSE)
- [ ] Lead detail page with full info
- [ ] Booking creation from dashboard
- [ ] Advanced filters и search
- [ ] Export to CSV/Excel
- [ ] Charts и visualizations (Chart.js/Recharts)
- [ ] Dark mode
- [ ] Multi-language support

## Troubleshooting

### Backend не отвечает

Убедитесь что backend запущен:
```bash
cd backend
uvicorn app.main:app --reload
```

### CORS errors

Проверьте CORS настройки в `backend/app/main.py`:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Данные не загружаются

1. Проверьте что backend запущен на `http://localhost:8000`
2. Проверьте `.env.local` - правильный `NEXT_PUBLIC_API_URL`
3. Откройте DevTools → Network и проверьте запросы
4. Убедитесь что в БД есть tenant с ID=1

## License

Proprietary - CultureOrganica
