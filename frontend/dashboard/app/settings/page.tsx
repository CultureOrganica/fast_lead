'use client'

import { Sidebar } from '@/components/Sidebar'

export default function SettingsPage() {
  const channels = [
    { name: 'SMS (SMSC.ru)', status: 'Настроен', enabled: true, icon: '📱' },
    { name: 'Email (SMTP)', status: 'Настроен', enabled: true, icon: '📧' },
    { name: 'WhatsApp Business API', status: 'Настроен', enabled: true, icon: '💚' },
    { name: 'Telegram Bot', status: 'Требует настройки', enabled: false, icon: '✈️' },
    { name: 'VK Bots API', status: 'Требует настройки', enabled: false, icon: '💬' },
    { name: 'Cal.com', status: 'Настроен', enabled: true, icon: '📅' },
  ]

  return (
    <div className="flex">
      <Sidebar />

      <main className="flex-1 overflow-y-auto bg-gray-50">
        {/* Header */}
        <div className="bg-white shadow">
          <div className="px-8 py-6">
            <h1 className="text-2xl font-bold text-gray-900">Настройки</h1>
            <p className="mt-1 text-sm text-gray-500">
              Конфигурация каналов и интеграций
            </p>
          </div>
        </div>

        {/* Content */}
        <div className="p-8">
          {/* Channels */}
          <div className="bg-white shadow rounded-lg overflow-hidden mb-8">
            <div className="px-6 py-4 border-b border-gray-200">
              <h2 className="text-lg font-medium text-gray-900">
                Каналы коммуникации
              </h2>
            </div>
            <div className="divide-y divide-gray-200">
              {channels.map((channel) => (
                <div
                  key={channel.name}
                  className="px-6 py-4 flex items-center justify-between"
                >
                  <div className="flex items-center space-x-4">
                    <span className="text-2xl">{channel.icon}</span>
                    <div>
                      <p className="text-sm font-medium text-gray-900">
                        {channel.name}
                      </p>
                      <p
                        className={`text-sm ${
                          channel.enabled ? 'text-green-600' : 'text-orange-600'
                        }`}
                      >
                        {channel.status}
                      </p>
                    </div>
                  </div>
                  <button
                    className={`
                      relative inline-flex h-6 w-11 flex-shrink-0 cursor-pointer rounded-full border-2 border-transparent transition-colors duration-200 ease-in-out
                      ${channel.enabled ? 'bg-primary-600' : 'bg-gray-200'}
                    `}
                  >
                    <span
                      className={`
                        inline-block h-5 w-5 transform rounded-full bg-white shadow ring-0 transition duration-200 ease-in-out
                        ${channel.enabled ? 'translate-x-5' : 'translate-x-0'}
                      `}
                    />
                  </button>
                </div>
              ))}
            </div>
          </div>

          {/* Tenant Info */}
          <div className="bg-white shadow rounded-lg overflow-hidden">
            <div className="px-6 py-4 border-b border-gray-200">
              <h2 className="text-lg font-medium text-gray-900">
                Информация о tenant
              </h2>
            </div>
            <div className="px-6 py-4 space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700">
                  Tenant ID
                </label>
                <div className="mt-1">
                  <input
                    type="text"
                    value="1"
                    readOnly
                    className="shadow-sm focus:ring-primary-500 focus:border-primary-500 block w-full sm:text-sm border-gray-300 rounded-md bg-gray-50"
                  />
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700">
                  Название компании
                </label>
                <div className="mt-1">
                  <input
                    type="text"
                    defaultValue="Fast Lead Demo"
                    className="shadow-sm focus:ring-primary-500 focus:border-primary-500 block w-full sm:text-sm border-gray-300 rounded-md"
                  />
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700">
                  API URL
                </label>
                <div className="mt-1">
                  <input
                    type="text"
                    value="http://localhost:8000/api/v1"
                    readOnly
                    className="shadow-sm focus:ring-primary-500 focus:border-primary-500 block w-full sm:text-sm border-gray-300 rounded-md bg-gray-50"
                  />
                </div>
              </div>

              <div className="pt-4">
                <button
                  type="button"
                  className="inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
                >
                  Сохранить изменения
                </button>
              </div>
            </div>
          </div>

          {/* Documentation Links */}
          <div className="mt-8 bg-gray-100 rounded-lg p-6">
            <h3 className="text-sm font-medium text-gray-900 mb-4">
              📚 Документация по настройке
            </h3>
            <div className="space-y-2 text-sm">
              <a
                href="#"
                className="block text-primary-600 hover:text-primary-500"
              >
                → SMS Integration (SMSC.ru)
              </a>
              <a
                href="#"
                className="block text-primary-600 hover:text-primary-500"
              >
                → Email Setup (SMTP)
              </a>
              <a
                href="#"
                className="block text-primary-600 hover:text-primary-500"
              >
                → WhatsApp Business API
              </a>
              <a
                href="#"
                className="block text-primary-600 hover:text-primary-500"
              >
                → Telegram Bot Configuration
              </a>
              <a
                href="#"
                className="block text-primary-600 hover:text-primary-500"
              >
                → VK Bots API Setup
              </a>
              <a
                href="#"
                className="block text-primary-600 hover:text-primary-500"
              >
                → Cal.com Integration
              </a>
            </div>
          </div>
        </div>
      </main>
    </div>
  )
}
