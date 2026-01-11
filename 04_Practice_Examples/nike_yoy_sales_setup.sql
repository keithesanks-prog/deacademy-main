-- ============================================
-- NIKE YEAR-OVER-YEAR SALES DATABASE
-- ============================================
-- Practice calculating YoY percent change in sales

-- Drop existing tables if they exist
DROP TABLE IF EXISTS dim_product_nike CASCADE;
DROP TABLE IF EXISTS dim_category_nike CASCADE;

-- ============================================
-- CATEGORY DIMENSION TABLE
-- ============================================
CREATE TABLE dim_category_nike (
    category_id SERIAL PRIMARY KEY,
    category_name VARCHAR(100),
    available_color VARCHAR(50),
    available_stock INTEGER
);

INSERT INTO dim_category_nike (category_id, category_name, available_color, available_stock) VALUES
(1, 'Running Shoes', 'Black', 141),
(2, 'Basketball Shoes', 'White', 89),
(3, 'Training Shoes', 'Blue', 112),
(4, 'Lifestyle Sneakers', 'Red', 156),
(5, 'Soccer Cleats', 'Green', 78);

-- ============================================
-- PRODUCT DIMENSION TABLE
-- ============================================
CREATE TABLE dim_product_nike (
    entry_id SERIAL PRIMARY KEY,
    gender VARCHAR(10),
    product_name VARCHAR(100),
    category_id INTEGER REFERENCES dim_category_nike(category_id),
    price DECIMAL(10,2),
    product_reviews INTEGER,
    comfort_score DECIMAL(3,1),
    product_rating DECIMAL(3,1)
);

INSERT INTO dim_product_nike (entry_id, gender, product_name, category_id, price, product_reviews, comfort_score, product_rating) VALUES
(1, 'Male', 'Forward world 9', 1, 198, 985, 4.9, 1),
(2, 'Female', 'Air Zoom Pegasus', 1, 120, 1250, 4.7, 4.5),
(3, 'Male', 'LeBron 20', 2, 200, 890, 4.8, 4.8),
(4, 'Female', 'Metcon 8', 3, 150, 670, 4.6, 4.6),
(5, 'Male', 'Air Force 1', 4, 110, 2100, 4.5, 4.9),
(6, 'Female', 'Blazer Mid', 4, 100, 1450, 4.4, 4.7),
(7, 'Male', 'Mercurial Vapor', 5, 250, 540, 4.9, 4.8),
(8, 'Female', 'React Infinity', 1, 160, 980, 4.8, 4.7),
(9, 'Male', 'Kyrie 8', 2, 140, 720, 4.6, 4.5),
(10, 'Female', 'Free RN', 3, 100, 890, 4.5, 4.6);

-- ============================================
-- SALES FACT TABLE
-- ============================================
CREATE TABLE sales (
    sale_id SERIAL PRIMARY KEY,
    order_date DATE,
    entry_id INTEGER REFERENCES dim_product_nike(entry_id),
    quantity INTEGER,
    total_sales DECIMAL(10,2)
);

-- Insert sales data for 2022 and 2023
INSERT INTO sales (order_date, entry_id, quantity, total_sales) VALUES
-- 2022 Sales
('2022-01-15', 1, 10, 1980.00),
('2022-02-20', 2, 15, 1800.00),
('2022-03-10', 3, 8, 1600.00),
('2022-04-05', 4, 12, 1800.00),
('2022-05-18', 5, 20, 2200.00),
('2022-06-22', 6, 18, 1800.00),
('2022-07-30', 7, 5, 1250.00),
('2022-08-15', 8, 14, 2240.00),
('2022-09-10', 9, 11, 1540.00),
('2022-10-25', 10, 16, 1600.00),
('2022-11-12', 1, 12, 2376.00),
('2022-12-05', 2, 20, 2400.00),

-- More 2022 sales
('2022-01-25', 3, 7, 1400.00),
('2022-02-14', 4, 9, 1350.00),
('2022-03-20', 5, 25, 2750.00),
('2022-04-18', 6, 22, 2200.00),
('2022-05-08', 7, 6, 1500.00),
('2022-06-15', 8, 13, 2080.00),
('2022-07-22', 9, 10, 1400.00),
('2022-08-30', 10, 15, 1500.00),

-- 2023 Sales (with growth)
('2023-01-12', 1, 15, 2970.00),  -- 50% increase
('2023-02-18', 2, 20, 2400.00),  -- 33% increase
('2023-03-08', 3, 10, 2000.00),  -- 25% increase
('2023-04-10', 4, 15, 2250.00),  -- 25% increase
('2023-05-15', 5, 28, 3080.00),  -- 40% increase
('2023-06-20', 6, 25, 2500.00),  -- 39% increase
('2023-07-25', 7, 8, 2000.00),   -- 60% increase
('2023-08-12', 8, 18, 2880.00),  -- 29% increase
('2023-09-15', 9, 14, 1960.00),  -- 27% increase
('2023-10-22', 10, 20, 2000.00), -- 25% increase
('2023-11-10', 1, 18, 3564.00),  -- 50% increase
('2023-12-08', 2, 28, 3360.00),  -- 40% increase

-- More 2023 sales
('2023-01-28', 3, 11, 2200.00),
('2023-02-16', 4, 12, 1800.00),
('2023-03-22', 5, 35, 3850.00),
('2023-04-20', 6, 30, 3000.00),
('2023-05-10', 7, 9, 2250.00),
('2023-06-18', 8, 17, 2720.00),
('2023-07-28', 9, 13, 1820.00),
('2023-08-25', 10, 19, 1900.00),

-- 2024 Sales (some products, for testing NULL handling)
('2024-01-10', 1, 20, 3960.00),
('2024-02-15', 2, 25, 3000.00),
('2024-03-12', 5, 40, 4400.00);

-- ============================================
-- VERIFICATION QUERIES
-- ============================================

-- Check the data
SELECT 'Database setup complete!' as status;

-- Show sales by year
SELECT 
    EXTRACT(YEAR FROM order_date) as year,
    COUNT(*) as order_count,
    SUM(total_sales) as total_sales
FROM sales
GROUP BY EXTRACT(YEAR FROM order_date)
ORDER BY year;

-- Show product details
SELECT 
    p.entry_id,
    p.product_name,
    c.category_name,
    p.price
FROM dim_product_nike p
JOIN dim_category_nike c ON p.category_id = c.category_id
ORDER BY p.entry_id;
