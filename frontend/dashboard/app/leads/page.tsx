'use client'

import { Sidebar } from '@/components/Sidebar'
import { LeadsTable } from '@/components/LeadsTable'
import { useState } from 'react'

export default function LeadsPage() {
  const [filter, setFilter] = useState<'all' | string>('all')

  const channels = [
    { value: 'all', label: 'Все каналы', count: 156 },
    { value: 'sms', label: 'SMS', count: 45 },
    { value: 'email', label: 'Email', count: 32 },
    { value: 'whatsapp', label: 'WhatsApp', count: 28 },
    { value: 'telegram', label: 'Telegram', count: 24 },
    { value: 'vk', label: 'VK', count: 18 },
    { value: 'web', label: 'Web', count: 9 },
  ]

  return (
    <div className="flex">
      <Sidebar />

      <main className="flex-1 overflow-y-auto bg-gray-50">
        {/* Header */}
        <div className="bg-white shadow">
          <div className="px-8 py-6">
            <div className="flex items-center justify-between">
              <div>
                <h1 className="text-2xl font-bold text-gray-900">Лиды</h1>
                <p className="mt-1 text-sm text-gray-500">
                  Управление входящими лидами из всех каналов
                </p>
              </div>
              <button className="inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500">
                <span className="mr-2">➕</span>
                Добавить лид
              </button>
            </div>
          </div>
        </div>

        {/* Filters */}
        <div className="bg-white border-b border-gray-200 px-8 py-4">
          <div className="flex space-x-2 overflow-x-auto">
            {channels.map((channel) => (
              <button
                key={channel.value}
                onClick={() => setFilter(channel.value)}
                className={`
                  inline-flex items-center px-4 py-2 rounded-full text-sm font-medium whitespace-nowrap
                  ${
                    filter === channel.value
                      ? 'bg-primary-100 text-primary-800'
                      : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                  }
                `}
              >
                {channel.label}
                <span className="ml-2 text-xs bg-white px-2 py-0.5 rounded-full">
                  {channel.count}
                </span>
              </button>
            ))}
          </div>
        </div>

        {/* Content */}
        <div className="p-8">
          <LeadsTable channel={filter === 'all' ? undefined : filter} />
        </div>
      </main>
    </div>
  )
}
