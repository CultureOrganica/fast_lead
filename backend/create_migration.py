#!/usr/bin/env python3
"""
Create initial Alembic migration.

This script creates the initial database migration based on current models.
Run this before starting the application for the first time.
"""

import sys
import os

# Add backend directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from alembic import command
from alembic.config import Config

def create_migration():
    """Create initial migration."""

    print("Creating initial migration...")

    # Load alembic config
    alembic_cfg = Config("alembic.ini")

    # Generate migration
    command.revision(
        alembic_cfg,
        autogenerate=True,
        message="Initial migration: Tenant, User, Lead models"
    )

    print("✓ Migration created successfully!")
    print("\nNext steps:")
    print("1. Review the migration file in alembic/versions/")
    print("2. Run: alembic upgrade head")

if __name__ == "__main__":
    create_migration()
