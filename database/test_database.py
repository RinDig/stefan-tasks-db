#!/usr/bin/env python3
"""
Test Database Connection and Display Tables
"""

import os
import sys
import psycopg2
from dotenv import load_dotenv
from tabulate import tabulate

# Fix Windows Unicode
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# Load environment variables
load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL_EXTERNAL')

def test_database():
    """Test database and show contents"""
    print("\n" + "=" * 60)
    print("🔍 DATABASE STATUS CHECK")
    print("=" * 60)
    
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()
        
        # Check what tables exist
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' 
            ORDER BY table_name;
        """)
        
        tables = cursor.fetchall()
        print(f"\n✅ Connected successfully!")
        print(f"\n📊 Found {len(tables)} tables:")
        for table in tables:
            cursor.execute(f"SELECT COUNT(*) FROM {table[0]}")
            count = cursor.fetchone()[0]
            print(f"   • {table[0]:20} ({count} rows)")
        
        # Show categories
        print("\n📁 CATEGORIES:")
        cursor.execute("SELECT name, slug, color_code, icon_emoji FROM categories ORDER BY sort_order")
        categories = cursor.fetchall()
        if categories:
            print(tabulate(categories, headers=['Name', 'Slug', 'Color', 'Icon'], tablefmt='simple'))
        else:
            print("   (empty)")
        
        # Show columns
        print("\n📋 COLUMNS:")
        cursor.execute("SELECT name, slug, color_code FROM columns ORDER BY sort_order")
        columns = cursor.fetchall()
        if columns:
            print(tabulate(columns, headers=['Name', 'Slug', 'Color'], tablefmt='simple'))
        else:
            print("   (empty)")
        
        # Show tasks
        print("\n✅ SAMPLE TASKS:")
        cursor.execute("""
            SELECT t.title, cat.name as category, col.name as column, t.priority
            FROM tasks t
            LEFT JOIN categories cat ON t.category_id = cat.id
            LEFT JOIN columns col ON t.column_id = col.id
            WHERE t.is_deleted = false
            ORDER BY t.created_at DESC
            LIMIT 5
        """)
        tasks = cursor.fetchall()
        if tasks:
            print(tabulate(tasks, headers=['Title', 'Category', 'Column', 'Priority'], tablefmt='simple'))
        else:
            print("   (no tasks yet)")
        
        cursor.close()
        conn.close()
        
        print("\n" + "=" * 60)
        print("✅ Database is working perfectly!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        print("\nTip: Check your .env file has the correct DATABASE_URL_EXTERNAL")

if __name__ == "__main__":
    test_database()