-- ============================================
-- WALMART LOYAL CUSTOMERS DATABASE SETUP
-- ============================================
-- This creates sample data for practicing the Walmart loyal customers problem

-- Drop existing tables if they exist
DROP TABLE IF EXISTS walmart_reviews;
DROP TABLE IF EXISTS walmart_orders;
DROP TABLE IF EXISTS walmart_customers;

-- ============================================
-- CUSTOMERS TABLE
-- ============================================
CREATE TABLE walmart_customers (
    customer_id INTEGER PRIMARY KEY,
    customer_name VARCHAR(100),
    email VARCHAR(100),
    signup_date DATE
);

INSERT INTO walmart_customers VALUES
(101, 'Alice Johnson', 'alice@email.com', '2022-01-15'),
(102, 'Bob Smith', 'bob@email.com', '2022-03-20'),
(103, 'Carol White', 'carol@email.com', '2022-02-10'),
(104, 'David Brown', 'david@email.com', '2022-05-05'),
(105, 'Emma Davis', 'emma@email.com', '2022-01-28'),
(106, 'Frank Miller', 'frank@email.com', '2022-04-12'),
(107, 'Grace Lee', 'grace@email.com', '2022-06-25'),
(108, 'Henry Wilson', 'henry@email.com', '2022-03-18'),
(109, 'Iris Martinez', 'iris@email.com', '2022-07-14'),
(110, 'Jack Taylor', 'jack@email.com', '2022-08-01');

-- ============================================
-- ORDERS TABLE
-- ============================================
CREATE TABLE walmart_orders (
    order_id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    order_date DATE,
    total_amount DECIMAL(10,2),
    FOREIGN KEY (customer_id) REFERENCES walmart_customers(customer_id)
);

INSERT INTO walmart_orders VALUES
-- Alice (101) - High spender in 2023: $2500 total
(1001, 101, '2023-01-15', 450.00),
(1002, 101, '2023-03-20', 380.00),
(1003, 101, '2023-05-10', 520.00),
(1004, 101, '2023-07-22', 650.00),
(1005, 101, '2023-09-15', 500.00),

-- Bob (102) - High spender in 2023: $1800 total (but no reviews!)
(1006, 102, '2023-02-14', 600.00),
(1007, 102, '2023-04-18', 450.00),
(1008, 102, '2023-06-25', 400.00),
(1009, 102, '2023-08-30', 350.00),

-- Carol (103) - Low spender but good reviewer: $800 total
(1010, 103, '2023-01-20', 200.00),
(1011, 103, '2023-03-15', 180.00),
(1012, 103, '2023-05-22', 220.00),
(1013, 103, '2023-07-10', 200.00),

-- David (104) - Low spender, few reviews: $450 total
(1014, 104, '2023-02-05', 150.00),
(1015, 104, '2023-06-12', 300.00),

-- Emma (105) - High spender AND good reviewer: $3200 total ✅
(1016, 105, '2023-01-10', 800.00),
(1017, 105, '2023-02-28', 650.00),
(1018, 105, '2023-04-15', 720.00),
(1019, 105, '2023-06-20', 580.00),
(1020, 105, '2023-08-25', 450.00),

-- Frank (106) - Medium spender: $1200 total
(1021, 106, '2023-03-05', 400.00),
(1022, 106, '2023-05-18', 450.00),
(1023, 106, '2023-07-30', 350.00),

-- Grace (107) - Low spender: $600 total
(1024, 107, '2023-02-20', 300.00),
(1025, 107, '2023-06-15', 300.00),

-- Henry (108) - Medium spender, no reviews: $1100 total
(1026, 108, '2023-01-25', 350.00),
(1027, 108, '2023-04-10', 400.00),
(1028, 108, '2023-07-05', 350.00),

-- Iris (109) - Low spender: $500 total
(1029, 109, '2023-03-12', 250.00),
(1030, 109, '2023-08-20', 250.00),

-- Jack (110) - No orders in 2023 (only 2022)
(1031, 110, '2022-11-15', 400.00);

-- ============================================
-- REVIEWS TABLE
-- ============================================
CREATE TABLE walmart_reviews (
    review_id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    product_name VARCHAR(100),
    rating INTEGER,
    review_date DATE,
    FOREIGN KEY (customer_id) REFERENCES walmart_customers(customer_id)
);

INSERT INTO walmart_reviews VALUES
-- Alice (101) - 8 reviews, avg 4.5 stars ✅
(2001, 101, 'Laptop', 5, '2023-01-20'),
(2002, 101, 'Mouse', 4, '2023-02-15'),
(2003, 101, 'Keyboard', 5, '2023-03-25'),
(2004, 101, 'Monitor', 4, '2023-04-10'),
(2005, 101, 'Webcam', 5, '2023-05-18'),
(2006, 101, 'Headphones', 4, '2023-06-22'),
(2007, 101, 'Desk Chair', 5, '2023-07-30'),
(2008, 101, 'Desk Lamp', 4, '2023-08-15'),

-- Bob (102) - No reviews!

-- Carol (103) - 6 reviews, avg 4.2 stars (good reviewer but low spender)
(2009, 103, 'Phone Case', 4, '2023-01-25'),
(2010, 103, 'Charger', 4, '2023-02-10'),
(2011, 103, 'Screen Protector', 5, '2023-03-20'),
(2012, 103, 'Earbuds', 4, '2023-04-15'),
(2013, 103, 'Power Bank', 4, '2023-05-28'),
(2014, 103, 'USB Cable', 4, '2023-06-12'),

-- David (104) - Only 3 reviews (not enough!)
(2015, 104, 'Notebook', 5, '2023-02-10'),
(2016, 104, 'Pen Set', 4, '2023-03-15'),
(2017, 104, 'Backpack', 4, '2023-06-20'),

-- Emma (105) - 12 reviews, avg 4.8 stars ✅
(2018, 105, 'Smart Watch', 5, '2023-01-15'),
(2019, 105, 'Fitness Tracker', 5, '2023-01-28'),
(2020, 105, 'Yoga Mat', 5, '2023-02-12'),
(2021, 105, 'Water Bottle', 4, '2023-03-05'),
(2022, 105, 'Running Shoes', 5, '2023-03-22'),
(2023, 105, 'Gym Bag', 5, '2023-04-18'),
(2024, 105, 'Protein Powder', 5, '2023-05-10'),
(2025, 105, 'Resistance Bands', 5, '2023-06-02'),
(2026, 105, 'Dumbbells', 4, '2023-06-25'),
(2027, 105, 'Exercise Ball', 5, '2023-07-15'),
(2028, 105, 'Jump Rope', 5, '2023-08-08'),
(2029, 105, 'Foam Roller', 5, '2023-08-30'),

-- Frank (106) - 5 reviews, avg 3.8 stars (not high enough!)
(2030, 106, 'Coffee Maker', 4, '2023-03-10'),
(2031, 106, 'Blender', 3, '2023-04-05'),
(2032, 106, 'Toaster', 4, '2023-05-20'),
(2033, 106, 'Microwave', 4, '2023-06-15'),
(2034, 106, 'Air Fryer', 4, '2023-07-25'),

-- Grace (107) - 7 reviews, avg 4.3 stars (good reviews but low spending)
(2035, 107, 'Book', 4, '2023-02-25'),
(2036, 107, 'Bookmark', 5, '2023-03-10'),
(2037, 107, 'Reading Light', 4, '2023-04-15'),
(2038, 107, 'Journal', 4, '2023-05-20'),
(2039, 107, 'Planner', 5, '2023-06-18'),
(2040, 107, 'Sticky Notes', 4, '2023-07-22'),
(2041, 107, 'Highlighters', 4, '2023-08-10'),

-- Henry (108) - No reviews!

-- Iris (109) - Only 2 reviews (not enough!)
(2042, 109, 'Plant Pot', 5, '2023-03-18'),
(2043, 109, 'Garden Tools', 4, '2023-08-25'),

-- Jack (110) - Reviews from 2022 (not 2023!)
(2044, 110, 'Winter Coat', 5, '2022-11-20'),
(2045, 110, 'Gloves', 4, '2022-11-25'),
(2046, 110, 'Scarf', 5, '2022-12-01'),
(2047, 110, 'Boots', 4, '2022-12-10'),
(2048, 110, 'Hat', 5, '2022-12-15');

-- ============================================
-- DATABASE SETUP COMPLETE
-- ============================================
-- You can now run queries on the following tables:
-- - walmart_customers (10 rows)
-- - walmart_orders (31 rows)
-- - walmart_reviews (48 rows)

-- To verify the setup, run these queries separately:
-- SELECT COUNT(*) FROM walmart_customers;
-- SELECT COUNT(*) FROM walmart_orders;
-- SELECT COUNT(*) FROM walmart_reviews;
