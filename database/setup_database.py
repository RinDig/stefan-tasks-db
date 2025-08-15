#!/usr/bin/env python3
"""
Database Setup Script for Stefan's Task Manager
Connects to Render PostgreSQL and creates all tables
"""

import os
import sys
import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv
from pathlib import Path

# Fix Windows Unicode issues
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# Load environment variables
load_dotenv()

# Database connection from .env
DATABASE_URL = os.getenv('DATABASE_URL_EXTERNAL')

def run_sql_file(cursor, filepath):
    """Execute SQL file"""
    print(f"\n📄 Running {filepath}...")
    with open(filepath, 'r', encoding='utf-8') as file:
        sql_content = file.read()
        try:
            cursor.execute(sql_content)
            print(f"✅ {filepath} executed successfully!")
            return True
        except Exception as e:
            print(f"❌ Error in {filepath}: {str(e)}")
            return False

def check_connection():
    """Test database connection"""
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        record = cursor.fetchone()
        print(f"✅ Connected to PostgreSQL: {record[0][:30]}...")
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"❌ Connection failed: {str(e)}")
        return False

def setup_database():
    """Main setup function"""
    print("=" * 60)
    print("🚀 Stefan's Task Manager - Database Setup")
    print("=" * 60)
    
    # Check connection first
    if not check_connection():
        print("\n❌ Cannot connect to database. Check your .env file.")
        return False
    
    try:
        # Connect to database
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()
        conn.autocommit = False  # Use transactions
        
        # Run setup scripts in order
        scripts = [
            "01_create_tables.sql",
            "02_seed_data.sql"
        ]
        
        for script in scripts:
            filepath = Path(__file__).parent / script
            if not filepath.exists():
                print(f"⚠️  {script} not found, skipping...")
                continue
                
            if not run_sql_file(cursor, filepath):
                print(f"\n❌ Setup failed at {script}")
                conn.rollback()
                return False
        
        # Commit all changes
        conn.commit()
        print("\n✅ All changes committed successfully!")
        
        # Show table counts
        print("\n📊 Database Statistics:")
        print("-" * 40)
        
        tables = ['users', 'categories', 'columns', 'clients', 'tasks', 
                  'email_threads', 'sync_queue', 'audit_log', 'monday_sync_log']
        
        for table in tables:
            try:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = cursor.fetchone()[0]
                print(f"  {table:20} {count:5} rows")
            except:
                print(f"  {table:20} -")
        
        cursor.close()
        conn.close()
        
        print("\n" + "=" * 60)
        print("🎉 Database setup complete!")
        print("=" * 60)
        return True
        
    except Exception as e:
        print(f"\n❌ Setup error: {str(e)}")
        if conn:
            conn.rollback()
            conn.close()
        return False

def reset_database():
    """Drop all tables (use with caution!)"""
    response = input("\n⚠️  This will DELETE ALL DATA. Are you sure? (type 'yes' to confirm): ")
    if response.lower() != 'yes':
        print("Cancelled.")
        return
    
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()
        
        # Drop tables in reverse order (due to foreign keys)
        tables = [
            'monday_sync_log', 'audit_log', 'sync_queue', 'email_threads',
            'tasks', 'clients', 'columns', 'categories', 'users'
        ]
        
        print("\n🗑️  Dropping tables...")
        for table in tables:
            try:
                cursor.execute(f"DROP TABLE IF EXISTS {table} CASCADE")
                print(f"  Dropped {table}")
            except Exception as e:
                print(f"  Error dropping {table}: {e}")
        
        # Drop functions
        cursor.execute("DROP FUNCTION IF EXISTS trigger_set_timestamp() CASCADE")
        cursor.execute("DROP FUNCTION IF EXISTS log_task_changes() CASCADE")
        
        conn.commit()
        cursor.close()
        conn.close()
        
        print("\n✅ Database reset complete. Run setup again to recreate tables.")
        
    except Exception as e:
        print(f"❌ Reset error: {str(e)}")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == 'reset':
        reset_database()
    else:
        setup_database()
        print("\n💡 Tip: Run 'python setup_database.py reset' to drop all tables")