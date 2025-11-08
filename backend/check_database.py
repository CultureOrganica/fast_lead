#!/usr/bin/env python3
"""
Check database connectivity and schema.

This script validates database connection and checks if all tables exist.
"""

import sys
import os
import asyncio

# Add backend directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

async def check_database():
    """Check database connectivity and schema."""

    print("🔍 Checking database...\n")

    errors = []
    warnings = []

    # 1. Check database connection
    print("1. Database connection:")
    try:
        from app.core.config import settings
        from app.core.database import async_session_maker
        from sqlalchemy import text

        async with async_session_maker() as session:
            result = await session.execute(text("SELECT 1"))
            print(f"  ✓ Connected to: {settings.database_url_str.split('@')[1] if '@' in settings.database_url_str else 'database'}")

    except Exception as e:
        errors.append(f"Database connection failed: {e}")
        print(f"  ✗ Connection failed: {e}")
        print("\n💡 Make sure:")
        print("  - PostgreSQL is running")
        print("  - DATABASE_URL is set correctly in .env")
        print("  - Database 'fast_lead_dev' exists")
        return False

    # 2. Check if tables exist
    print("\n2. Database tables:")
    try:
        from sqlalchemy import inspect

        async with async_session_maker() as session:
            # Get connection
            connection = await session.connection()

            # Inspect database
            inspector = inspect(connection.sync_connection)
            tables = inspector.get_table_names()

            required_tables = ['tenants', 'users', 'leads']

            if not tables:
                warnings.append("No tables found - run migrations first")
                print("  ⚠ No tables found")
                print("\n💡 Run migrations:")
                print("  python create_migration.py")
                print("  alembic upgrade head")
            else:
                print(f"  ✓ Found {len(tables)} table(s)")
                for table_name in required_tables:
                    if table_name in tables:
                        print(f"    ✓ {table_name}")
                    else:
                        warnings.append(f"Table '{table_name}' not found")
                        print(f"    ⚠ {table_name} - missing")

    except Exception as e:
        errors.append(f"Failed to inspect tables: {e}")
        print(f"  ✗ Table inspection failed: {e}")

    # 3. Check Redis connection (for Celery)
    print("\n3. Redis connection:")
    try:
        from app.core.config import settings
        import redis

        # Parse Redis URL
        redis_url = str(settings.redis_url)
        redis_client = redis.from_url(redis_url)

        # Test connection
        redis_client.ping()
        print(f"  ✓ Connected to Redis")
        redis_client.close()

    except Exception as e:
        warnings.append(f"Redis connection failed: {e}")
        print(f"  ⚠ Redis not available: {e}")
        print("    (Celery tasks will not work)")

    # Summary
    print("\n" + "=" * 60)
    if errors:
        print(f"❌ {len(errors)} ERROR(S):")
        for error in errors:
            print(f"  - {error}")
    else:
        print("✅ Database checks passed!")

    if warnings:
        print(f"\n⚠️  {len(warnings)} WARNING(S):")
        for warning in warnings:
            print(f"  - {warning}")

    print("=" * 60)

    return len(errors) == 0

if __name__ == "__main__":
    success = asyncio.run(check_database())
    sys.exit(0 if success else 1)
