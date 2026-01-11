-- ============================================
-- APPLE PHONES PRACTICE - SETUP SCRIPT
-- ============================================
-- This creates the tables and sample data for the TRIM/delimiter practice

-- Drop tables if they exist (for clean setup)
DROP TABLE IF EXISTS dim_phoneOrders_apple;
DROP TABLE IF EXISTS dim_phones_apple;

-- ============================================
-- CREATE TABLES
-- ============================================

-- Table 1: Phone catalog
CREATE TABLE dim_phones_apple (
    phone_id VARCHAR(20) PRIMARY KEY,
    phone_names VARCHAR(100),
    price_usd DECIMAL(10, 2)
);

-- Table 2: Phone orders
CREATE TABLE dim_phoneOrders_apple (
    order_id VARCHAR(20) PRIMARY KEY,
    customer_id VARCHAR(20),
    phone_id VARCHAR(20),
    order_time TIMESTAMP,
    order_status VARCHAR(20)
);

-- ============================================
-- INSERT SAMPLE DATA
-- ============================================

-- Insert phones (some will have orders, some won't)
INSERT INTO dim_phones_apple (phone_id, phone_names, price_usd) VALUES
('2695bb9', 'Acer - Iconia Talk S', 759.91),
('76397', 'Acer - Liquid Z6 Plus', 899.99),
('abc123', 'Acer - Iconia Tab 10 A3-A40', 299.99),
('def456', 'Acer - Liquid X2', 549.99),
('ghi789', 'Samsung - Galaxy S21', 799.99),
('jkl012', 'Apple - iPhone 13', 999.99),
('mno345', 'Google - Pixel 6', 599.99);

-- Insert orders (only for SOME phones)
INSERT INTO dim_phoneOrders_apple (order_id, customer_id, phone_id, order_time, order_status) VALUES
('7dd8597', '009c4e', '2695bb9', '2020-10-18 06:45:22', 'Cancelled'),
('ord001', 'cust01', 'ghi789', '2021-01-15 10:30:00', 'Completed'),
('ord002', 'cust02', 'jkl012', '2021-02-20 14:15:00', 'Completed'),
('ord003', 'cust03', 'mno345', '2021-03-10 09:00:00', 'Shipped');

-- ============================================
-- VERIFY DATA
-- ============================================

-- Check phones table
SELECT 'Phones Table:' AS info;
SELECT * FROM dim_phones_apple ORDER BY phone_names;

-- Check orders table
SELECT 'Orders Table:' AS info;
SELECT * FROM dim_phoneOrders_apple ORDER BY order_time;

-- Quick check: Which phones have orders?
SELECT 'Phones WITH orders:' AS info;
SELECT DISTINCT p.phone_id, p.phone_names
FROM dim_phones_apple p
INNER JOIN dim_phoneOrders_apple o ON p.phone_id = o.phone_id
ORDER BY p.phone_names;

-- Quick check: Which phones DON'T have orders?
SELECT 'Phones WITHOUT orders (before splitting):' AS info;
SELECT p.phone_id, p.phone_names
FROM dim_phones_apple p
LEFT JOIN dim_phoneOrders_apple o ON p.phone_id = o.phone_id
WHERE o.order_id IS NULL
ORDER BY p.phone_names;
