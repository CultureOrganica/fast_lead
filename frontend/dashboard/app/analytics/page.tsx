'use client'

import { Sidebar } from '@/components/Sidebar'

export default function AnalyticsPage() {
  const metrics = [
    {
      channel: 'SMS',
      leads: 45,
      conversion: '68%',
      avgTime: '12 мин',
      color: 'bg-blue-500',
    },
    {
      channel: 'Email',
      leads: 32,
      conversion: '45%',
      avgTime: '24 мин',
      color: 'bg-purple-500',
    },
    {
      channel: 'WhatsApp',
      leads: 28,
      conversion: '72%',
      avgTime: '8 мин',
      color: 'bg-green-500',
    },
    {
      channel: 'Telegram',
      leads: 24,
      conversion: '64%',
      avgTime: '15 мин',
      color: 'bg-indigo-500',
    },
    {
      channel: 'VK',
      leads: 18,
      conversion: '58%',
      avgTime: '18 мин',
      color: 'bg-blue-700',
    },
    {
      channel: 'Web',
      leads: 9,
      conversion: '34%',
      avgTime: '45 мин',
      color: 'bg-gray-500',
    },
  ]

  return (
    <div className="flex">
      <Sidebar />

      <main className="flex-1 overflow-y-auto bg-gray-50">
        {/* Header */}
        <div className="bg-white shadow">
          <div className="px-8 py-6">
            <h1 className="text-2xl font-bold text-gray-900">Аналитика</h1>
            <p className="mt-1 text-sm text-gray-500">
              Статистика и эффективность каналов
            </p>
          </div>
        </div>

        {/* Content */}
        <div className="p-8">
          {/* Summary Cards */}
          <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4 mb-8">
            <div className="bg-white overflow-hidden shadow rounded-lg">
              <div className="p-5">
                <div className="flex items-center">
                  <div className="flex-shrink-0">
                    <span className="text-3xl">📊</span>
                  </div>
                  <div className="ml-5 w-0 flex-1">
                    <dl>
                      <dt className="text-sm font-medium text-gray-500 truncate">
                        Всего лидов
                      </dt>
                      <dd className="text-2xl font-semibold text-gray-900">
                        156
                      </dd>
                    </dl>
                  </div>
                </div>
              </div>
            </div>

            <div className="bg-white overflow-hidden shadow rounded-lg">
              <div className="p-5">
                <div className="flex items-center">
                  <div className="flex-shrink-0">
                    <span className="text-3xl">✅</span>
                  </div>
                  <div className="ml-5 w-0 flex-1">
                    <dl>
                      <dt className="text-sm font-medium text-gray-500 truncate">
                        Конверсия
                      </dt>
                      <dd className="text-2xl font-semibold text-gray-900">
                        58%
                      </dd>
                    </dl>
                  </div>
                </div>
              </div>
            </div>

            <div className="bg-white overflow-hidden shadow rounded-lg">
              <div className="p-5">
                <div className="flex items-center">
                  <div className="flex-shrink-0">
                    <span className="text-3xl">⏱️</span>
                  </div>
                  <div className="ml-5 w-0 flex-1">
                    <dl>
                      <dt className="text-sm font-medium text-gray-500 truncate">
                        Среднее время
                      </dt>
                      <dd className="text-2xl font-semibold text-gray-900">
                        18 мин
                      </dd>
                    </dl>
                  </div>
                </div>
              </div>
            </div>

            <div className="bg-white overflow-hidden shadow rounded-lg">
              <div className="p-5">
                <div className="flex items-center">
                  <div className="flex-shrink-0">
                    <span className="text-3xl">📈</span>
                  </div>
                  <div className="ml-5 w-0 flex-1">
                    <dl>
                      <dt className="text-sm font-medium text-gray-500 truncate">
                        Рост
                      </dt>
                      <dd className="text-2xl font-semibold text-gray-900">
                        +24%
                      </dd>
                    </dl>
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Channel Performance */}
          <div className="bg-white shadow rounded-lg overflow-hidden">
            <div className="px-6 py-4 border-b border-gray-200">
              <h2 className="text-lg font-medium text-gray-900">
                Эффективность каналов
              </h2>
            </div>
            <div className="p-6">
              <div className="space-y-4">
                {metrics.map((metric) => (
                  <div key={metric.channel} className="border-b border-gray-100 last:border-0 pb-4 last:pb-0">
                    <div className="flex items-center justify-between mb-2">
                      <div className="flex items-center space-x-3">
                        <div className={`w-3 h-3 rounded-full ${metric.color}`} />
                        <span className="font-medium text-gray-900">
                          {metric.channel}
                        </span>
                      </div>
                      <div className="text-sm text-gray-500">
                        {metric.leads} лидов
                      </div>
                    </div>
                    <div className="grid grid-cols-3 gap-4 text-sm">
                      <div>
                        <div className="text-gray-500">Конверсия</div>
                        <div className="font-semibold text-gray-900">
                          {metric.conversion}
                        </div>
                      </div>
                      <div>
                        <div className="text-gray-500">Среднее время</div>
                        <div className="font-semibold text-gray-900">
                          {metric.avgTime}
                        </div>
                      </div>
                      <div>
                        <div className="w-full bg-gray-200 rounded-full h-2 mt-2">
                          <div
                            className={`${metric.color} h-2 rounded-full`}
                            style={{
                              width: metric.conversion,
                            }}
                          />
                        </div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Note */}
          <div className="mt-8 bg-blue-50 border border-blue-200 rounded-lg p-4">
            <div className="flex">
              <div className="flex-shrink-0">
                <span className="text-2xl">ℹ️</span>
              </div>
              <div className="ml-3">
                <h3 className="text-sm font-medium text-blue-800">
                  Демо данные
                </h3>
                <div className="mt-2 text-sm text-blue-700">
                  <p>
                    Это демонстрационная страница с mock данными. В production
                    здесь будут реальные метрики из backend API.
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  )
}
