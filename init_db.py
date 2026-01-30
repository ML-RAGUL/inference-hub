"""
Initialize Database
===================
Run this script to create all tables in PostgreSQL.

Usage:
    python init_db.py
"""

import sys
sys.path.insert(0, ".")

from src.db.database import Base, engine
from src.db.models import Tenant, UsageLog

def init_database():
    print("🚀 Creating database tables...")
    
    # This creates all tables defined in models.py
    Base.metadata.create_all(bind=engine)
    
    print("✅ Tables created successfully!")
    print("")
    print("Tables created:")
    print("  - tenants")
    print("  - usage_logs")

if __name__ == "__main__":
    init_database()
