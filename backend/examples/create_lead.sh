#!/bin/bash

# Example: Create a lead via Public API
# This script demonstrates how to create a lead from the widget

# Base URL
BASE_URL="http://localhost:8000"

# Example 1: SMS channel lead
echo "Creating SMS lead..."
curl -X POST "${BASE_URL}/api/v1/leads" \
  -H "Content-Type: application/json" \
  -H "X-Tenant-Id: 1" \
  -d '{
    "name": "Иван Петров",
    "phone": "+79991234567",
    "channel": "sms",
    "source": "https://example.com/landing",
    "utm": {
      "source": "google",
      "medium": "cpc",
      "campaign": "spring_sale"
    },
    "consent": {
      "gdpr": true,
      "marketing": false
    }
  }' | jq

echo -e "\n---\n"

# Example 2: Email channel lead
echo "Creating Email lead..."
curl -X POST "${BASE_URL}/api/v1/leads" \
  -H "Content-Type: application/json" \
  -H "X-Tenant-Id: 1" \
  -d '{
    "name": "Мария Смирнова",
    "email": "maria@example.com",
    "channel": "email",
    "source": "https://example.com/pricing",
    "consent": {
      "gdpr": true,
      "marketing": true
    }
  }' | jq

echo -e "\n---\n"

# Example 3: VK channel lead
echo "Creating VK lead..."
curl -X POST "${BASE_URL}/api/v1/leads" \
  -H "Content-Type: application/json" \
  -H "X-Tenant-Id: 1" \
  -d '{
    "name": "Алексей Иванов",
    "vk_id": "id123456789",
    "channel": "vk",
    "source": "https://example.com/services",
    "consent": {
      "gdpr": true,
      "marketing": true
    }
  }' | jq

echo -e "\n---\n"

# Example 4: Web chat lead
echo "Creating Web chat lead..."
curl -X POST "${BASE_URL}/api/v1/leads" \
  -H "Content-Type: application/json" \
  -H "X-Tenant-Id: 1" \
  -d '{
    "name": "Елена Козлова",
    "phone": "+79267654321",
    "email": "elena@example.com",
    "channel": "web",
    "source": "https://example.com/contact",
    "payload": {
      "page_title": "Contact Us",
      "referrer": "https://google.com"
    },
    "consent": {
      "gdpr": true,
      "marketing": false
    }
  }' | jq

echo -e "\nDone! ✅"
