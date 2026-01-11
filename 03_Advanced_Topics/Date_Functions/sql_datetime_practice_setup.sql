-- ============================================
-- SQL DATE/TIME FUNCTIONS PRACTICE ENVIRONMENT
-- ============================================
-- This file sets up sample tables for practicing date/time calculations
-- Run this to create your practice database
-- ============================================

-- Clean up if tables already exist
DROP TABLE IF EXISTS video_views;
DROP TABLE IF EXISTS subscriptions;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS events;

-- ============================================
-- TABLE 1: VIDEO_VIEWS (Watch Time Calculations)
-- ============================================
CREATE TABLE video_views (
    view_id INTEGER PRIMARY KEY,
    user_name TEXT,
    video_title TEXT,
    start_time DATETIME,
    end_time DATETIME
);

INSERT INTO video_views VALUES
(1, 'Alice', 'SQL Tutorial Part 1', '2021-01-15 14:30:00', '2021-01-15 15:45:00'),
(2, 'Bob', 'Python Basics', '2021-02-20 09:00:00', '2021-02-20 11:30:00'),
(3, 'Alice', 'SQL Tutorial Part 2', '2021-03-10 16:00:00', '2021-03-10 17:15:00'),
(4, 'Carol', 'Data Science 101', '2021-04-05 10:30:00', '2021-04-05 13:00:00'),
(5, 'Bob', 'Advanced SQL', '2021-05-12 08:00:00', '2021-05-12 10:45:00'),
(6, 'Alice', 'Machine Learning', '2021-06-18 14:00:00', '2021-06-18 18:30:00'),
(7, 'David', 'Web Development', '2021-07-22 11:00:00', '2021-07-22 12:20:00'),
(8, 'Carol', 'Database Design', '2021-08-30 15:30:00', '2021-08-30 17:00:00');

-- ============================================
-- TABLE 2: SUBSCRIPTIONS (Duration Calculations)
-- ============================================
CREATE TABLE subscriptions (
    subscription_id INTEGER PRIMARY KEY,
    user_name TEXT,
    plan_type TEXT,
    start_date DATE,
    end_date DATE,
    monthly_price DECIMAL(10,2)
);

INSERT INTO subscriptions VALUES
(1, 'Alice Johnson', 'Premium', '2021-01-01', '2021-12-31', 19.99),
(2, 'Bob Williams', 'Basic', '2021-03-15', '2021-09-15', 9.99),
(3, 'Carol Davis', 'Premium', '2021-06-01', '2021-11-30', 19.99),
(4, 'David Miller', 'Basic', '2021-02-01', '2021-08-01', 9.99),
(5, 'Eve Wilson', 'Premium', '2021-04-10', '2022-04-10', 19.99),
(6, 'Frank Moore', 'Basic', '2021-07-01', '2021-12-31', 9.99),
(7, 'Grace Taylor', 'Premium', '2021-05-15', '2022-05-15', 19.99),
(8, 'Henry Anderson', 'Basic', '2021-08-20', '2022-02-20', 9.99);

-- ============================================
-- TABLE 3: ORDERS (Time Between Events)
-- ============================================
CREATE TABLE orders (
    order_id INTEGER PRIMARY KEY,
    customer_name TEXT,
    order_date DATETIME,
    shipped_date DATETIME,
    delivered_date DATETIME,
    order_amount DECIMAL(10,2)
);

INSERT INTO orders VALUES
(1, 'Alice', '2021-01-10 10:00:00', '2021-01-11 14:30:00', '2021-01-15 16:20:00', 150.00),
(2, 'Bob', '2021-02-15 09:30:00', '2021-02-16 11:00:00', '2021-02-20 10:15:00', 89.99),
(3, 'Carol', '2021-03-20 14:15:00', '2021-03-21 09:45:00', '2021-03-25 13:30:00', 220.50),
(4, 'David', '2021-04-05 11:20:00', '2021-04-06 15:10:00', '2021-04-10 12:00:00', 175.25),
(5, 'Eve', '2021-05-12 16:45:00', '2021-05-13 10:30:00', '2021-05-18 14:45:00', 99.99),
(6, 'Frank', '2021-06-18 08:00:00', '2021-06-19 12:20:00', '2021-06-23 09:30:00', 310.00),
(7, 'Grace', '2021-07-22 13:30:00', '2021-07-23 16:00:00', '2021-07-28 11:15:00', 145.75),
(8, 'Henry', '2021-08-30 10:15:00', '2021-08-31 14:45:00', '2021-09-05 15:30:00', 199.99);

-- ============================================
-- TABLE 4: EVENTS (Age Calculations)
-- ============================================
CREATE TABLE events (
    event_id INTEGER PRIMARY KEY,
    event_name TEXT,
    event_date DATE,
    attendees INTEGER,
    location TEXT
);

INSERT INTO events VALUES
(1, 'Tech Conference 2021', '2021-03-15', 500, 'San Francisco'),
(2, 'Data Summit', '2021-06-20', 300, 'New York'),
(3, 'AI Workshop', '2021-09-10', 150, 'Boston'),
(4, 'Cloud Computing Expo', '2021-12-05', 750, 'Seattle'),
(5, 'Startup Meetup', '2021-02-28', 100, 'Austin'),
(6, 'DevOps Days', '2021-07-14', 400, 'Chicago'),
(7, 'Security Conference', '2021-10-22', 600, 'Denver'),
(8, 'Mobile Dev Summit', '2021-11-30', 350, 'Portland');

-- ============================================
-- VERIFICATION QUERIES
-- ============================================

SELECT 'Video Views Table:' as info;
SELECT * FROM video_views;

SELECT 'Subscriptions Table:' as info;
SELECT * FROM subscriptions;

SELECT 'Orders Table:' as info;
SELECT * FROM orders;

SELECT 'Events Table:' as info;
SELECT * FROM events;
