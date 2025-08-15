-- Stefan's Task Management System - Database Schema
-- PostgreSQL 14+ required
-- Run this script in your Render PostgreSQL database

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create update timestamp function
CREATE OR REPLACE FUNCTION trigger_set_timestamp()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- =====================================================
-- 1. USERS TABLE
-- =====================================================
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    google_id VARCHAR(255) UNIQUE,
    preferences JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_users_google_id ON users(google_id);

-- Add update trigger
CREATE TRIGGER update_users_timestamp
    BEFORE UPDATE ON users
    FOR EACH ROW
    EXECUTE FUNCTION trigger_set_timestamp();

-- =====================================================
-- 2. CATEGORIES TABLE
-- =====================================================
CREATE TABLE IF NOT EXISTS categories (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(100) NOT NULL,
    slug VARCHAR(100) UNIQUE NOT NULL,
    color_code VARCHAR(7) NOT NULL,
    icon_emoji VARCHAR(10),
    sort_order INTEGER DEFAULT 0,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_categories_slug ON categories(slug);
CREATE INDEX IF NOT EXISTS idx_categories_active ON categories(is_active) WHERE is_active = true;

CREATE TRIGGER update_categories_timestamp
    BEFORE UPDATE ON categories
    FOR EACH ROW
    EXECUTE FUNCTION trigger_set_timestamp();

-- =====================================================
-- 3. COLUMNS TABLE
-- =====================================================
CREATE TABLE IF NOT EXISTS columns (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(100) NOT NULL,
    slug VARCHAR(100) UNIQUE NOT NULL,
    color_code VARCHAR(7) NOT NULL,
    sort_order INTEGER DEFAULT 0,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_columns_slug ON columns(slug);
CREATE INDEX IF NOT EXISTS idx_columns_active ON columns(is_active) WHERE is_active = true;

CREATE TRIGGER update_columns_timestamp
    BEFORE UPDATE ON columns
    FOR EACH ROW
    EXECUTE FUNCTION trigger_set_timestamp();

-- =====================================================
-- 4. CLIENTS TABLE
-- =====================================================
CREATE TABLE IF NOT EXISTS clients (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255),
    phone VARCHAR(50),
    notes TEXT,
    contact_info JSONB DEFAULT '{}',
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_by UUID REFERENCES users(id)
);

CREATE INDEX IF NOT EXISTS idx_clients_name ON clients(name);
CREATE INDEX IF NOT EXISTS idx_clients_email ON clients(email);
CREATE INDEX IF NOT EXISTS idx_clients_active ON clients(is_active) WHERE is_active = true;

CREATE TRIGGER update_clients_timestamp
    BEFORE UPDATE ON clients
    FOR EACH ROW
    EXECUTE FUNCTION trigger_set_timestamp();

-- =====================================================
-- 5. TASKS TABLE (Core Entity)
-- =====================================================
CREATE TABLE IF NOT EXISTS tasks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title VARCHAR(500) NOT NULL,
    description TEXT,
    category_id UUID REFERENCES categories(id) ON DELETE RESTRICT,
    column_id UUID REFERENCES columns(id) ON DELETE RESTRICT,
    client_id UUID REFERENCES clients(id) ON DELETE SET NULL,
    priority VARCHAR(20) DEFAULT 'normal' CHECK (priority IN ('urgent', 'high', 'normal', 'low')),
    status VARCHAR(20) DEFAULT 'active' CHECK (status IN ('active', 'completed', 'cancelled')),
    due_date DATE,
    estimated_hours INTEGER,
    actual_hours INTEGER,
    metadata JSONB DEFAULT '{}',
    assigned_to UUID REFERENCES users(id) ON DELETE SET NULL,
    monday_com_id VARCHAR(100),
    google_calendar_id VARCHAR(255),
    version INTEGER DEFAULT 1,
    last_synced_at TIMESTAMP WITH TIME ZONE,
    is_deleted BOOLEAN DEFAULT false,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_by UUID REFERENCES users(id),
    updated_by UUID REFERENCES users(id)
);

-- Create all indexes for tasks table
CREATE INDEX IF NOT EXISTS idx_tasks_category ON tasks(category_id);
CREATE INDEX IF NOT EXISTS idx_tasks_column ON tasks(column_id);
CREATE INDEX IF NOT EXISTS idx_tasks_client ON tasks(client_id);
CREATE INDEX IF NOT EXISTS idx_tasks_priority ON tasks(priority);
CREATE INDEX IF NOT EXISTS idx_tasks_status ON tasks(status);
CREATE INDEX IF NOT EXISTS idx_tasks_due_date ON tasks(due_date);
CREATE INDEX IF NOT EXISTS idx_tasks_created_at ON tasks(created_at);
CREATE INDEX IF NOT EXISTS idx_tasks_updated_at ON tasks(updated_at);
CREATE INDEX IF NOT EXISTS idx_tasks_active ON tasks(is_deleted) WHERE is_deleted = false;
CREATE INDEX IF NOT EXISTS idx_tasks_monday_id ON tasks(monday_com_id) WHERE monday_com_id IS NOT NULL;
CREATE INDEX IF NOT EXISTS idx_tasks_sync_status ON tasks(last_synced_at, updated_at);

-- Composite indexes for common queries
CREATE INDEX IF NOT EXISTS idx_tasks_board_view ON tasks(column_id, category_id, created_at) WHERE is_deleted = false;
CREATE INDEX IF NOT EXISTS idx_tasks_user_active ON tasks(assigned_to, status, due_date) WHERE is_deleted = false;

CREATE TRIGGER update_tasks_timestamp
    BEFORE UPDATE ON tasks
    FOR EACH ROW
    EXECUTE FUNCTION trigger_set_timestamp();

-- =====================================================
-- 6. EMAIL THREADS TABLE
-- =====================================================
CREATE TABLE IF NOT EXISTS email_threads (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    gmail_thread_id VARCHAR(255) UNIQUE NOT NULL,
    gmail_message_id VARCHAR(255) NOT NULL,
    task_id UUID REFERENCES tasks(id) ON DELETE SET NULL,
    client_id UUID REFERENCES clients(id) ON DELETE SET NULL,
    subject VARCHAR(998) NOT NULL,
    content TEXT,
    sender_email VARCHAR(255) NOT NULL,
    sender_name VARCHAR(255),
    status VARCHAR(20) DEFAULT 'unprocessed' CHECK (status IN ('unprocessed', 'processed', 'ignored')),
    attachments JSONB DEFAULT '[]',
    is_processed BOOLEAN DEFAULT false,
    email_date TIMESTAMP WITH TIME ZONE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_email_gmail_thread ON email_threads(gmail_thread_id);
CREATE INDEX IF NOT EXISTS idx_email_task ON email_threads(task_id);
CREATE INDEX IF NOT EXISTS idx_email_client ON email_threads(client_id);
CREATE INDEX IF NOT EXISTS idx_email_sender ON email_threads(sender_email);
CREATE INDEX IF NOT EXISTS idx_email_date ON email_threads(email_date);
CREATE INDEX IF NOT EXISTS idx_email_unprocessed ON email_threads(is_processed) WHERE is_processed = false;

CREATE TRIGGER update_email_threads_timestamp
    BEFORE UPDATE ON email_threads
    FOR EACH ROW
    EXECUTE FUNCTION trigger_set_timestamp();

-- =====================================================
-- 7. SYNC QUEUE TABLE
-- =====================================================
CREATE TABLE IF NOT EXISTS sync_queue (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    task_id UUID REFERENCES tasks(id) ON DELETE CASCADE,
    operation VARCHAR(20) NOT NULL CHECK (operation IN ('create', 'update', 'delete', 'move')),
    payload JSONB NOT NULL,
    status VARCHAR(20) DEFAULT 'pending' CHECK (status IN ('pending', 'processing', 'completed', 'failed')),
    retry_count INTEGER DEFAULT 0,
    scheduled_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    processed_at TIMESTAMP WITH TIME ZONE,
    error_message TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_sync_queue_status ON sync_queue(status, scheduled_at);
CREATE INDEX IF NOT EXISTS idx_sync_queue_task ON sync_queue(task_id);
CREATE INDEX IF NOT EXISTS idx_sync_queue_retry ON sync_queue(retry_count, scheduled_at) WHERE status = 'failed';

-- =====================================================
-- 8. AUDIT LOG TABLE
-- =====================================================
CREATE TABLE IF NOT EXISTS audit_log (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    task_id UUID REFERENCES tasks(id) ON DELETE CASCADE,
    user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    action VARCHAR(50) NOT NULL,
    old_values JSONB,
    new_values JSONB,
    source VARCHAR(50) DEFAULT 'web' CHECK (source IN ('web', 'mobile', 'api', 'sync', 'email')),
    user_agent TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_audit_task ON audit_log(task_id);
CREATE INDEX IF NOT EXISTS idx_audit_user ON audit_log(user_id);
CREATE INDEX IF NOT EXISTS idx_audit_action ON audit_log(action);
CREATE INDEX IF NOT EXISTS idx_audit_created ON audit_log(created_at);

-- =====================================================
-- 9. MONDAY SYNC LOG TABLE
-- =====================================================
CREATE TABLE IF NOT EXISTS monday_sync_log (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    task_id UUID REFERENCES tasks(id) ON DELETE CASCADE,
    monday_item_id VARCHAR(100) NOT NULL,
    operation VARCHAR(20) NOT NULL CHECK (operation IN ('create', 'update', 'delete')),
    payload JSONB NOT NULL,
    status VARCHAR(20) DEFAULT 'success' CHECK (status IN ('success', 'failed')),
    synced_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    error_message TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_monday_sync_task ON monday_sync_log(task_id);
CREATE INDEX IF NOT EXISTS idx_monday_sync_item ON monday_sync_log(monday_item_id);
CREATE INDEX IF NOT EXISTS idx_monday_sync_status ON monday_sync_log(status, synced_at);

-- =====================================================
-- AUDIT TRIGGER FOR TASKS
-- =====================================================
CREATE OR REPLACE FUNCTION log_task_changes()
RETURNS TRIGGER AS $$
BEGIN
  INSERT INTO audit_log (
    task_id,
    user_id, 
    action,
    old_values,
    new_values,
    source
  ) VALUES (
    COALESCE(NEW.id, OLD.id),
    COALESCE(NEW.updated_by, OLD.updated_by),
    TG_OP,
    CASE WHEN TG_OP = 'DELETE' THEN row_to_json(OLD) ELSE NULL END,
    CASE WHEN TG_OP != 'DELETE' THEN row_to_json(NEW) ELSE NULL END,
    'database'
  );
  
  RETURN COALESCE(NEW, OLD);
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER task_audit_trigger
  AFTER INSERT OR UPDATE OR DELETE ON tasks
  FOR EACH ROW
  EXECUTE FUNCTION log_task_changes();

-- Success message
DO $$
BEGIN
  RAISE NOTICE 'All tables created successfully!';
END $$;