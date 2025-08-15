-- Stefan's Task Management System - Seed Data
-- Run this after 01_create_tables.sql

-- =====================================================
-- INSERT DEFAULT CATEGORIES
-- =====================================================
INSERT INTO categories (name, slug, color_code, icon_emoji, sort_order) VALUES
('Concrete', 'concrete', '#FF6B6B', '🏗️', 1),
('Customer', 'customer', '#4ECDC4', '👥', 2),
('Crew', 'crew', '#45B7D1', '👷', 3),
('Personal', 'personal', '#96CEB4', '👤', 4)
ON CONFLICT (slug) DO NOTHING;

-- =====================================================
-- INSERT DEFAULT COLUMNS
-- =====================================================
INSERT INTO columns (name, slug, color_code, sort_order) VALUES
('Backlog', 'backlog', '#6c757d', 1),
('This Week', 'this-week', '#ffc107', 2),
('In Progress', 'in-progress', '#17a2b8', 3),
('Done', 'done', '#28a745', 4)
ON CONFLICT (slug) DO NOTHING;

-- =====================================================
-- INSERT TEST USER (Stefan)
-- =====================================================
INSERT INTO users (email, name, google_id) VALUES
('stefan@paintingbusiness.com', 'Stefan', 'google_test_id_stefan')
ON CONFLICT (email) DO NOTHING;

-- =====================================================
-- INSERT SAMPLE CLIENTS
-- =====================================================
WITH stefan_user AS (
  SELECT id FROM users WHERE email = 'stefan@paintingbusiness.com' LIMIT 1
)
INSERT INTO clients (name, email, phone, notes, created_by) 
SELECT 
  client.name,
  client.email,
  client.phone,
  client.notes,
  stefan_user.id
FROM stefan_user,
(VALUES
  ('DACG Concrete', 'contact@dacgconcrete.com', '555-0101', 'Primary concrete supplier, quick response needed'),
  ('Lifetime Fitness', 'facilities@lifetime.com', '555-0102', 'Commercial painting contract'),
  ('US Soccer Federation', 'facilities@ussoccer.org', '555-0103', 'Training facility maintenance'),
  ('Boston Construction', 'pm@bostonconst.com', '555-0104', 'General contractor partner'),
  ('Kentucky Development', 'info@kydev.com', '555-0105', 'New development projects')
) AS client(name, email, phone, notes)
ON CONFLICT DO NOTHING;

-- =====================================================
-- INSERT SAMPLE TASKS
-- =====================================================
WITH 
  stefan_user AS (SELECT id FROM users WHERE email = 'stefan@paintingbusiness.com' LIMIT 1),
  concrete_cat AS (SELECT id FROM categories WHERE slug = 'concrete' LIMIT 1),
  customer_cat AS (SELECT id FROM categories WHERE slug = 'customer' LIMIT 1),
  crew_cat AS (SELECT id FROM categories WHERE slug = 'crew' LIMIT 1),
  personal_cat AS (SELECT id FROM categories WHERE slug = 'personal' LIMIT 1),
  backlog_col AS (SELECT id FROM columns WHERE slug = 'backlog' LIMIT 1),
  this_week_col AS (SELECT id FROM columns WHERE slug = 'this-week' LIMIT 1),
  in_progress_col AS (SELECT id FROM columns WHERE slug = 'in-progress' LIMIT 1),
  done_col AS (SELECT id FROM columns WHERE slug = 'done' LIMIT 1),
  dacg_client AS (SELECT id FROM clients WHERE name = 'DACG Concrete' LIMIT 1),
  lifetime_client AS (SELECT id FROM clients WHERE name = 'Lifetime Fitness' LIMIT 1),
  us_soccer_client AS (SELECT id FROM clients WHERE name = 'US Soccer Federation' LIMIT 1)
INSERT INTO tasks (
  title, 
  description, 
  category_id, 
  column_id, 
  client_id, 
  priority, 
  status, 
  due_date, 
  created_by, 
  updated_by
)
SELECT 
  task.title,
  task.description,
  task.category_id,
  task.column_id,
  task.client_id,
  task.priority,
  task.status,
  task.due_date,
  stefan_user.id,
  stefan_user.id
FROM stefan_user,
(VALUES
  -- Urgent tasks in This Week
  ('Call DACG about Georgia pour schedule', 
   'Need to confirm dates for next week', 
   (SELECT id FROM categories WHERE slug = 'concrete' LIMIT 1),
   (SELECT id FROM columns WHERE slug = 'this-week' LIMIT 1),
   (SELECT id FROM clients WHERE name = 'DACG Concrete' LIMIT 1),
   'urgent', 'active', CURRENT_DATE + INTERVAL '2 days'),
   
  ('Lifetime Fitness - respond to change order',
   'They want to add 2 more rooms to the project',
   (SELECT id FROM categories WHERE slug = 'customer' LIMIT 1),
   (SELECT id FROM columns WHERE slug = 'this-week' LIMIT 1),
   (SELECT id FROM clients WHERE name = 'Lifetime Fitness' LIMIT 1),
   'high', 'active', CURRENT_DATE + INTERVAL '3 days'),
   
  -- In Progress tasks
  ('Schedule crew for Boston project',
   'Need 4 painters for Thursday',
   (SELECT id FROM categories WHERE slug = 'crew' LIMIT 1),
   (SELECT id FROM columns WHERE slug = 'in-progress' LIMIT 1),
   NULL,
   'high', 'active', CURRENT_DATE + INTERVAL '1 day'),
   
  ('US Soccer facility walkthrough',
   'Site visit at 2pm Wednesday',
   (SELECT id FROM categories WHERE slug = 'customer' LIMIT 1),
   (SELECT id FROM columns WHERE slug = 'in-progress' LIMIT 1),
   (SELECT id FROM clients WHERE name = 'US Soccer Federation' LIMIT 1),
   'normal', 'active', CURRENT_DATE + INTERVAL '3 days'),
   
  -- Backlog tasks
  ('Review Kentucky project proposal',
   'New 50-unit development opportunity',
   (SELECT id FROM categories WHERE slug = 'customer' LIMIT 1),
   (SELECT id FROM columns WHERE slug = 'backlog' LIMIT 1),
   (SELECT id FROM clients WHERE name = 'Kentucky Development' LIMIT 1),
   'normal', 'active', CURRENT_DATE + INTERVAL '7 days'),
   
  ('Update insurance certificates',
   'Annual renewal due next month',
   (SELECT id FROM categories WHERE slug = 'personal' LIMIT 1),
   (SELECT id FROM columns WHERE slug = 'backlog' LIMIT 1),
   NULL,
   'low', 'active', CURRENT_DATE + INTERVAL '30 days'),
   
  ('Order paint supplies for spring',
   'Bulk order to save costs',
   (SELECT id FROM categories WHERE slug = 'crew' LIMIT 1),
   (SELECT id FROM columns WHERE slug = 'backlog' LIMIT 1),
   NULL,
   'low', 'active', CURRENT_DATE + INTERVAL '14 days'),
   
  -- Done tasks
  ('Submit invoice to Boston Construction',
   'Phase 1 complete - $45,000',
   (SELECT id FROM categories WHERE slug = 'customer' LIMIT 1),
   (SELECT id FROM columns WHERE slug = 'done' LIMIT 1),
   (SELECT id FROM clients WHERE name = 'Boston Construction' LIMIT 1),
   'normal', 'completed', CURRENT_DATE - INTERVAL '1 day'),
   
  ('Crew safety meeting',
   'Monthly safety review completed',
   (SELECT id FROM categories WHERE slug = 'crew' LIMIT 1),
   (SELECT id FROM columns WHERE slug = 'done' LIMIT 1),
   NULL,
   'normal', 'completed', CURRENT_DATE - INTERVAL '2 days')
) AS task(title, description, category_id, column_id, client_id, priority, status, due_date)
ON CONFLICT DO NOTHING;

-- =====================================================
-- VERIFY DATA WAS INSERTED
-- =====================================================
DO $$
DECLARE
  user_count INTEGER;
  category_count INTEGER;
  column_count INTEGER;
  client_count INTEGER;
  task_count INTEGER;
BEGIN
  SELECT COUNT(*) INTO user_count FROM users;
  SELECT COUNT(*) INTO category_count FROM categories;
  SELECT COUNT(*) INTO column_count FROM columns;
  SELECT COUNT(*) INTO client_count FROM clients;
  SELECT COUNT(*) INTO task_count FROM tasks;
  
  RAISE NOTICE 'Data seeded successfully:';
  RAISE NOTICE '  Users: %', user_count;
  RAISE NOTICE '  Categories: %', category_count;
  RAISE NOTICE '  Columns: %', column_count;
  RAISE NOTICE '  Clients: %', client_count;
  RAISE NOTICE '  Tasks: %', task_count;
END $$;