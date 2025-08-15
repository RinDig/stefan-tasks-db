#!/usr/bin/env python3
"""Simple database setup - just run the SQL"""

import os
import sys
import psycopg2
from dotenv import load_dotenv

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL_EXTERNAL')

print("🚀 Setting up database...")

try:
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    
    # Read and execute the create tables SQL
    with open('01_create_tables.sql', 'r', encoding='utf-8') as f:
        sql = f.read()
    
    cursor.execute(sql)
    conn.commit()
    print("✅ Tables created successfully!")
    
    # Now add the seed data (without the problematic trigger)
    # First, let's modify the seed data to work properly
    seed_sql = """
    -- Insert default categories
    INSERT INTO categories (name, slug, color_code, icon_emoji, sort_order) VALUES
    ('Concrete', 'concrete', '#FF6B6B', '🏗️', 1),
    ('Customer', 'customer', '#4ECDC4', '👥', 2),
    ('Crew', 'crew', '#45B7D1', '👷', 3),
    ('Personal', 'personal', '#96CEB4', '👤', 4)
    ON CONFLICT (slug) DO NOTHING;

    -- Insert default columns
    INSERT INTO columns (name, slug, color_code, sort_order) VALUES
    ('Backlog', 'backlog', '#6c757d', 1),
    ('This Week', 'this-week', '#ffc107', 2),
    ('In Progress', 'in-progress', '#17a2b8', 3),
    ('Done', 'done', '#28a745', 4)
    ON CONFLICT (slug) DO NOTHING;

    -- Insert test user
    INSERT INTO users (email, name) VALUES
    ('stefan@paintingbusiness.com', 'Stefan')
    ON CONFLICT (email) DO NOTHING;
    """
    
    cursor.execute(seed_sql)
    conn.commit()
    print("✅ Seed data added!")
    
    # Check what we created
    cursor.execute("SELECT COUNT(*) FROM categories")
    cat_count = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM columns")
    col_count = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM users")
    user_count = cursor.fetchone()[0]
    
    print(f"\n📊 Database ready:")
    print(f"   • {cat_count} categories")
    print(f"   • {col_count} columns") 
    print(f"   • {user_count} users")
    print(f"\n✅ Database setup complete!")
    
    cursor.close()
    conn.close()
    
except Exception as e:
    print(f"❌ Error: {e}")
    if conn:
        conn.rollback()
        conn.close()