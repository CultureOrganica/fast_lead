#!/bin/bash

# Fast Lead - API Examples for All Channels
# This script demonstrates creating leads through different communication channels

API_URL="http://localhost:8000/api/v1"
TENANT_ID="1"

echo "=========================================="
echo "Fast Lead - All Channels Examples"
echo "=========================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}Prerequisites:${NC}"
echo "1. Backend running: uvicorn app.main:app --reload"
echo "2. Celery worker running: ./run_celery_worker.sh"
echo "3. Database has tenant with ID=$TENANT_ID"
echo ""
echo "Press Enter to continue..."
read

# ==========================================
# 1. SMS Channel
# ==========================================
echo -e "\n${GREEN}1. SMS Channel (SMSC.ru)${NC}"
echo "Creating lead with SMS channel..."

curl -X POST "$API_URL/leads" \
  -H "Content-Type: application/json" \
  -H "X-Tenant-Id: $TENANT_ID" \
  -d '{
    "name": "Алексей Смирнов",
    "phone": "+79991234567",
    "channel": "sms",
    "source": "https://example.com/landing",
    "utm": {
      "source": "google",
      "medium": "cpc",
      "campaign": "spring2024"
    },
    "consent": {
      "gdpr": true,
      "marketing": true
    }
  }' | python3 -m json.tool

echo ""
echo "✓ SMS will be sent to +79991234567"
echo "✓ Check Celery worker logs for SMS task"
echo ""
sleep 2

# ==========================================
# 2. Email Channel
# ==========================================
echo -e "\n${GREEN}2. Email Channel (SMTP)${NC}"
echo "Creating lead with Email channel..."

curl -X POST "$API_URL/leads" \
  -H "Content-Type: application/json" \
  -H "X-Tenant-Id: $TENANT_ID" \
  -d '{
    "name": "Мария Петрова",
    "email": "maria.petrova@example.com",
    "phone": "+79991234568",
    "channel": "email",
    "source": "https://example.com/blog",
    "utm": {
      "source": "yandex",
      "medium": "organic"
    },
    "consent": {
      "gdpr": true,
      "marketing": true
    }
  }' | python3 -m json.tool

echo ""
echo "✓ Welcome email will be sent to maria.petrova@example.com"
echo "✓ Check Celery worker logs for email task"
echo ""
sleep 2

# ==========================================
# 3. VK Channel
# ==========================================
echo -e "\n${GREEN}3. VK Channel (VKontakte)${NC}"
echo "Creating lead with VK channel..."

curl -X POST "$API_URL/leads" \
  -H "Content-Type: application/json" \
  -H "X-Tenant-Id: $TENANT_ID" \
  -d '{
    "name": "Дмитрий Иванов",
    "vk_id": "123456789",
    "phone": "+79991234569",
    "channel": "vk",
    "source": "https://vk.com/yourgroup",
    "consent": {
      "gdpr": true,
      "marketing": true
    }
  }' | python3 -m json.tool

echo ""
echo "✓ VK lead created (requires VK bot configuration for auto-messaging)"
echo "✓ Status: CONTACTED (ready for manual processing)"
echo ""
sleep 2

# ==========================================
# 4. Telegram Channel
# ==========================================
echo -e "\n${GREEN}4. Telegram Channel${NC}"
echo "Creating lead with Telegram channel..."

curl -X POST "$API_URL/leads" \
  -H "Content-Type: application/json" \
  -H "X-Tenant-Id: $TENANT_ID" \
  -d '{
    "name": "Елена Соколова",
    "phone": "+79991234570",
    "email": "elena@example.com",
    "channel": "telegram",
    "source": "https://t.me/yourchannel",
    "consent": {
      "gdpr": true,
      "marketing": true
    }
  }' | python3 -m json.tool

echo ""
echo "✓ Telegram lead created (requires Telegram bot configuration)"
echo "✓ Status: CONTACTED (ready for manual processing)"
echo ""
sleep 2

# ==========================================
# 5. Web Channel
# ==========================================
echo -e "\n${GREEN}5. Web Channel (Widget)${NC}"
echo "Creating lead from web widget..."

curl -X POST "$API_URL/leads" \
  -H "Content-Type: application/json" \
  -H "X-Tenant-Id: $TENANT_ID" \
  -d '{
    "name": "Сергей Волков",
    "phone": "+79991234571",
    "email": "sergey@example.com",
    "channel": "web",
    "source": "https://example.com/contact",
    "utm": {
      "source": "direct",
      "medium": "none"
    },
    "consent": {
      "gdpr": true,
      "marketing": false
    }
  }' | python3 -m json.tool

echo ""
echo "✓ Web lead created (no automatic message sent)"
echo "✓ Status: NEW (waiting for operator review)"
echo ""
sleep 2

# ==========================================
# 6. WhatsApp Channel (placeholder)
# ==========================================
echo -e "\n${GREEN}6. WhatsApp Channel${NC}"
echo "Creating lead with WhatsApp channel..."

curl -X POST "$API_URL/leads" \
  -H "Content-Type: application/json" \
  -H "X-Tenant-Id: $TENANT_ID" \
  -d '{
    "name": "Анна Козлова",
    "phone": "+79991234572",
    "channel": "whatsapp",
    "consent": {
      "gdpr": true,
      "marketing": true
    }
  }' | python3 -m json.tool

echo ""
echo "✓ WhatsApp lead created (requires WhatsApp Business API)"
echo "✓ Status: CONTACTED (manual processing)"
echo ""
sleep 2

# ==========================================
# Check created leads
# ==========================================
echo -e "\n${GREEN}Checking database...${NC}"
echo "Run this SQL to see all created leads:"
echo ""
echo "  SELECT id, name, channel, status, phone, email, created_at"
echo "  FROM leads"
echo "  ORDER BY created_at DESC"
echo "  LIMIT 10;"
echo ""

echo -e "${GREEN}All channels tested!${NC}"
echo ""
echo "Next steps:"
echo "1. Check leads in database"
echo "2. Check Celery worker logs for task execution"
echo "3. Check SMSC.ru for SMS delivery (if configured)"
echo "4. Check email inbox for welcome email (if SMTP configured)"
echo ""
