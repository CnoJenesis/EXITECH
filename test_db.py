#!/usr/bin/env python
import os
import sys
import time

# Load environment variables from .env file if available
try:
    from dotenv import load_dotenv
    load_dotenv()
    print("Environment variables loaded from .env file")
except ImportError:
    print("python-dotenv not installed, using environment variables from the system")

# Import database config and Database class
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from config import DATABASE_CONFIG
from models.database import Database

def test_connection():
    """Test connection to the database"""
    print("Testing database connection...")
    print(f"Host: {DATABASE_CONFIG['host']}")
    print(f"User: {DATABASE_CONFIG['user']}")
    print(f"Database: {DATABASE_CONFIG['database']}")
    
    # Show PostgreSQL URL for Vercel deployment
    if 'pg_url' in DATABASE_CONFIG:
        print(f"PostgreSQL URL for Vercel: {DATABASE_CONFIG['pg_url']}")

    try:
        # Initialize database connection
        Database.initialize()
        
        # Test a simple query
        db = Database()
        result = db.fetch_one("SELECT 1 as test")
        
        if result and result.get('test') == 1:
            print("✅ Database connection successful!")
            
            # Try to query tables
            tables = db.fetch_all("SHOW TABLES")
            print(f"Found {len(tables)} tables:")
            for table in tables:
                table_name = list(table.values())[0]
                print(f"  - {table_name}")
                
            return True
        else:
            print("❌ Database query failed")
            return False
    except Exception as e:
        print(f"❌ Database connection error: {e}")
        return False
    finally:
        try:
            Database().close()
        except:
            pass

if __name__ == "__main__":
    success = test_connection()
    if not success:
        sys.exit(1) 