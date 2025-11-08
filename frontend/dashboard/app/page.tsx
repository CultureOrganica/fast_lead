'use client'

import { Sidebar } from '@/components/Sidebar'
import Link from 'next/link'

export default function DashboardPage() {
  // Mock stats - in production these would come from API
  const stats = [
    { label: 'Новые лиды', value: '24', change: '+12%', icon: '📥' },
    { label: 'В обработке', value: '8', change: '+5%', icon: '⏳' },
    { label: 'Встречи', value: '15', change: '+8%', icon: '📅' },
    { label: 'Конверсия', value: '62%', change: '+3%', icon: '📈' },
  ]

  const recentLeads = [
    {
      id: 1,
      name: 'Иван Петров',
      channel: 'SMS',
      status: 'Новый',
      time: '5 мин назад',
    },
    {
      id: 2,
      name: 'Мария Смирнова',
      channel: 'Email',
      status: 'Контакт',
      time: '12 мин назад',
    },
    {
      id: 3,
      name: 'Дмитрий Иванов',
      channel: 'WhatsApp',
      status: 'Квалифицирован',
      time: '25 мин назад',
    },
  ]

  return (
    <div className="flex">
      <Sidebar />

      <main className="flex-1 overflow-y-auto bg-gray-50">
        {/* Header */}
        <div className="bg-white shadow">
          <div className="px-8 py-6">
            <h1 className="text-2xl font-bold text-gray-900">Dashboard</h1>
            <p className="mt-1 text-sm text-gray-500">
              Обзор активности и статистики
            </p>
          </div>
        </div>

        {/* Content */}
        <div className="p-8">
          {/* Stats Grid */}
          <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4 mb-8">
            {stats.map((stat) => (
              <div
                key={stat.label}
                className="bg-white overflow-hidden shadow rounded-lg"
              >
                <div className="p-5">
                  <div className="flex items-center">
                    <div className="flex-shrink-0">
                      <span className="text-3xl">{stat.icon}</span>
                    </div>
                    <div className="ml-5 w-0 flex-1">
                      <dl>
                        <dt className="text-sm font-medium text-gray-500 truncate">
                          {stat.label}
                        </dt>
                        <dd className="flex items-baseline">
                          <div className="text-2xl font-semibold text-gray-900">
                            {stat.value}
                          </div>
                          <div className="ml-2 flex items-baseline text-sm font-semibold text-green-600">
                            {stat.change}
                          </div>
                        </dd>
                      </dl>
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>

          {/* Recent Leads */}
          <div className="bg-white shadow rounded-lg">
            <div className="px-6 py-4 border-b border-gray-200">
              <div className="flex items-center justify-between">
                <h2 className="text-lg font-medium text-gray-900">
                  Последние лиды
                </h2>
                <Link
                  href="/leads"
                  className="text-sm font-medium text-primary-600 hover:text-primary-500"
                >
                  Посмотреть все
                </Link>
              </div>
            </div>
            <div className="divide-y divide-gray-200">
              {recentLeads.map((lead) => (
                <div
                  key={lead.id}
                  className="px-6 py-4 hover:bg-gray-50 transition"
                >
                  <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-4">
                      <div>
                        <p className="text-sm font-medium text-gray-900">
                          {lead.name}
                        </p>
                        <p className="text-sm text-gray-500">
                          {lead.channel} • {lead.time}
                        </p>
                      </div>
                    </div>
                    <div>
                      <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                        {lead.status}
                      </span>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Quick Actions */}
          <div className="mt-8 grid grid-cols-1 gap-6 sm:grid-cols-3">
            <Link
              href="/leads"
              className="bg-primary-600 hover:bg-primary-700 text-white rounded-lg p-6 shadow transition"
            >
              <div className="text-4xl mb-2">👥</div>
              <h3 className="text-lg font-medium">Управление лидами</h3>
              <p className="text-sm text-primary-100 mt-1">
                Просмотр и обработка лидов
              </p>
            </Link>

            <Link
              href="/analytics"
              className="bg-white hover:bg-gray-50 border-2 border-gray-200 rounded-lg p-6 shadow transition"
            >
              <div className="text-4xl mb-2">📊</div>
              <h3 className="text-lg font-medium text-gray-900">Аналитика</h3>
              <p className="text-sm text-gray-500 mt-1">
                Отчеты и статистика
              </p>
            </Link>

            <Link
              href="/settings"
              className="bg-white hover:bg-gray-50 border-2 border-gray-200 rounded-lg p-6 shadow transition"
            >
              <div className="text-4xl mb-2">⚙️</div>
              <h3 className="text-lg font-medium text-gray-900">Настройки</h3>
              <p className="text-sm text-gray-500 mt-1">
                Конфигурация каналов
              </p>
            </Link>
          </div>
        </div>
      </main>
    </div>
  )
}
