#!/usr/bin/env python3
"""
Check all imports and dependencies.

This script validates that all imports work correctly and there are no
circular dependencies or missing modules.
"""

import sys
import os

# Add backend directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def check_imports():
    """Check all critical imports."""

    errors = []
    warnings = []

    print("🔍 Checking imports...\n")

    # 1. Check core modules
    print("1. Core modules:")
    try:
        from app.core.config import settings
        print("  ✓ app.core.config")
    except Exception as e:
        errors.append(f"Failed to import app.core.config: {e}")
        print(f"  ✗ app.core.config: {e}")

    try:
        from app.core.database import Base, get_db
        print("  ✓ app.core.database")
    except Exception as e:
        errors.append(f"Failed to import app.core.database: {e}")
        print(f"  ✗ app.core.database: {e}")

    try:
        from app.core.celery_app import celery_app
        print("  ✓ app.core.celery_app")
    except Exception as e:
        errors.append(f"Failed to import app.core.celery_app: {e}")
        print(f"  ✗ app.core.celery_app: {e}")

    # 2. Check models
    print("\n2. Models:")
    try:
        from app.models import Tenant, User, Lead, LeadStatus, LeadChannel
        print("  ✓ app.models (Tenant, User, Lead)")
    except Exception as e:
        errors.append(f"Failed to import models: {e}")
        print(f"  ✗ app.models: {e}")

    # 3. Check services
    print("\n3. Services:")
    try:
        from app.services.lead_service import LeadService
        print("  ✓ app.services.lead_service")
    except Exception as e:
        errors.append(f"Failed to import lead_service: {e}")
        print(f"  ✗ app.services.lead_service: {e}")

    try:
        from app.services.sms_service import SMSService
        print("  ✓ app.services.sms_service")
    except Exception as e:
        errors.append(f"Failed to import sms_service: {e}")
        print(f"  ✗ app.services.sms_service: {e}")

    # 4. Check Celery tasks
    print("\n4. Celery tasks:")
    try:
        from app.tasks.sms_tasks import send_sms_task
        print("  ✓ app.tasks.sms_tasks")
    except Exception as e:
        errors.append(f"Failed to import sms_tasks: {e}")
        print(f"  ✗ app.tasks.sms_tasks: {e}")

    try:
        from app.tasks.lead_tasks import process_new_lead_task
        print("  ✓ app.tasks.lead_tasks")
    except Exception as e:
        errors.append(f"Failed to import lead_tasks: {e}")
        print(f"  ✗ app.tasks.lead_tasks: {e}")

    # 5. Check API routes
    print("\n5. API routes:")
    try:
        from app.api.v1.leads import router
        print("  ✓ app.api.v1.leads")
    except Exception as e:
        errors.append(f"Failed to import leads router: {e}")
        print(f"  ✗ app.api.v1.leads: {e}")

    try:
        from app.api.v1.health import router
        print("  ✓ app.api.v1.health")
    except Exception as e:
        errors.append(f"Failed to import health router: {e}")
        print(f"  ✗ app.api.v1.health: {e}")

    # 6. Check schemas
    print("\n6. Schemas:")
    try:
        from app.schemas.lead import CreateLeadRequest, LeadResponse
        print("  ✓ app.schemas.lead")
    except Exception as e:
        errors.append(f"Failed to import lead schemas: {e}")
        print(f"  ✗ app.schemas.lead: {e}")

    # 7. Check main app
    print("\n7. Main app:")
    try:
        from app.main import app
        print("  ✓ app.main")
    except Exception as e:
        errors.append(f"Failed to import main app: {e}")
        print(f"  ✗ app.main: {e}")

    # Check settings
    print("\n8. Configuration:")
    try:
        from app.core.config import settings

        # Check critical settings
        critical_settings = [
            'database_url',
            'redis_url',
            'secret_key',
            'jwt_secret_key',
        ]

        for setting_name in critical_settings:
            value = getattr(settings, setting_name, None)
            if value:
                print(f"  ✓ {setting_name}")
            else:
                warnings.append(f"{setting_name} not configured")
                print(f"  ⚠ {setting_name}: not set")

        # Check Celery settings
        celery_settings = ['celery_broker_url', 'celery_result_backend']
        for setting_name in celery_settings:
            value = getattr(settings, setting_name, None)
            if value:
                print(f"  ✓ {setting_name}")
            else:
                warnings.append(f"{setting_name} not configured")
                print(f"  ⚠ {setting_name}: not set")

        # Check SMSC settings (optional)
        smsc_settings = ['smsc_login', 'smsc_password']
        for setting_name in smsc_settings:
            value = getattr(settings, setting_name, None)
            if value and value != "":
                print(f"  ✓ {setting_name}")
            else:
                warnings.append(f"{setting_name} not configured (SMS will not work)")
                print(f"  ⚠ {setting_name}: not set (SMS disabled)")

    except Exception as e:
        errors.append(f"Failed to check settings: {e}")
        print(f"  ✗ Settings check failed: {e}")

    # Summary
    print("\n" + "=" * 60)
    if errors:
        print(f"❌ {len(errors)} ERROR(S) FOUND:")
        for error in errors:
            print(f"  - {error}")
    else:
        print("✅ All imports successful!")

    if warnings:
        print(f"\n⚠️  {len(warnings)} WARNING(S):")
        for warning in warnings:
            print(f"  - {warning}")

    print("=" * 60)

    return len(errors) == 0

if __name__ == "__main__":
    success = check_imports()
    sys.exit(0 if success else 1)
