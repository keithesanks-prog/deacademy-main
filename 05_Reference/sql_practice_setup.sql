-- ============================================
-- SQL PRACTICE ENVIRONMENT (RESTORED & UPDATED)
-- ============================================

-- Clean up if tables already exist
DROP TABLE IF EXISTS customers CASCADE;
DROP TABLE IF EXISTS orders CASCADE;
DROP TABLE IF EXISTS products CASCADE;
DROP TABLE IF EXISTS employees CASCADE;
DROP TABLE IF EXISTS dim_product_nike CASCADE;
DROP TABLE IF EXISTS dim_category_nike CASCADE;
DROP TABLE IF EXISTS sales_by_year CASCADE;
DROP TABLE IF EXISTS orders_new CASCADE;
DROP TABLE IF EXISTS customers_new CASCADE;

-- ============================================
-- TABLE 1: CUSTOMERS
-- ============================================
CREATE TABLE customers (
    customer_id INTEGER PRIMARY KEY,
    name TEXT,
    total_spent DECIMAL(10,2),
    last_purchase_date DATE,
    country TEXT
);

INSERT INTO customers VALUES
(1, 'John Smith', 1500.00, '2025-11-20', 'England'),
(2, 'Maria Garcia', 800.00, '2025-09-15', 'India'),
(3, 'Chen Wei', 2500.00, '2025-11-25', 'China'),
(4, 'Anna Kowalski', 450.00, '2025-10-10', 'Poland'),
(5, 'James Brown', 3200.00, '2025-11-22', 'Australia'),
(6, 'Sophie Martin', 950.00, '2025-08-05', 'France'),
(7, 'Lars Hansen', 1800.00, '2025-11-18', 'Finland'),
(8, 'Yuki Tanaka', 600.00, '2025-07-20', 'Japan');

-- ============================================
-- TABLE 2: PRODUCTS
-- ============================================
CREATE TABLE products (
    product_id INTEGER PRIMARY KEY,
    product_name TEXT,
    price DECIMAL(10,2),
    category TEXT,
    units_sold INTEGER
);

INSERT INTO products VALUES
(1, 'Laptop Pro', 1200.00, 'Electronics', 150),
(2, 'Wireless Mouse', 25.00, 'Electronics', 500),
(3, 'Office Chair', 350.00, 'Furniture', 80),
(4, 'Desk Lamp', 45.00, 'Furniture', 200),
(5, 'Coffee Maker', 89.00, 'Appliances', 120),
(6, 'Blender', 65.00, 'Appliances', 95),
(7, 'Monitor 27"', 450.00, 'Electronics', 180),
(8, 'Keyboard', 75.00, 'Electronics', 300);

-- ============================================
-- TABLE 3: ORDERS
-- ============================================
CREATE TABLE orders (
    order_id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    order_date DATE,
    amount DECIMAL(10,2),
    status TEXT
);

INSERT INTO orders VALUES
(101, 1, '2025-11-20', 1200.00, 'Completed'),
(102, 2, '2025-11-21', 450.00, 'Completed'),
(103, 3, '2025-11-22', 8500.00, 'Pending'),
(104, 1, '2025-11-23', 75.00, 'Completed'),
(105, 4, '2025-11-24', 12000.00, 'Pending'),
(106, 5, '2025-11-25', 350.00, 'Completed'),
(107, 3, '2025-11-26', 2500.00, 'Shipped'),
(108, 2, '2025-11-27', 15000.00, 'Pending');

-- ============================================
-- TABLE 4: EMPLOYEES
-- ============================================
CREATE TABLE employees (
    employee_id INTEGER PRIMARY KEY,
    name TEXT,
    department TEXT,
    salary DECIMAL(10,2),
    years_experience INTEGER,
    performance_score INTEGER
);

INSERT INTO employees VALUES
(1, 'Alice Johnson', 'Sales', 65000, 3, 92),
(2, 'Bob Williams', 'Engineering', 95000, 7, 88),
(3, 'Carol Davis', 'Marketing', 72000, 4, 75),
(4, 'David Miller', 'Sales', 58000, 2, 68),
(5, 'Eve Wilson', 'Engineering', 105000, 10, 95),
(6, 'Frank Moore', 'HR', 62000, 5, 82),
(7, 'Grace Taylor', 'Marketing', 68000, 3, 90),
(8, 'Henry Anderson', 'Engineering', 88000, 6, 85);

-- ============================================
-- TABLE 5: DIM_PRODUCT_NIKE (Updated with 3 Years of Data)
-- ============================================
CREATE TABLE dim_product_nike (
    entry_id INTEGER PRIMARY KEY,
    gender TEXT,
    product_name TEXT,
    category_id INTEGER,
    price DECIMAL(10,2),
    product_reviews INTEGER,
    comfort_score DECIMAL(3,1),
    product_rating DECIMAL(3,1),
    order_date DATE
);

INSERT INTO dim_product_nike VALUES
-- 2022 Data
(101, 'Male', 'Forward World', 9, 180, 500, 4.5, 4.5, '2022-01-21'),
(102, 'Female', 'Air Max 270', 1, 140, 600, 4.6, 4.5, '2022-05-15'),
(103, 'Male', 'React Infinity', 1, 150, 400, 4.7, 4.6, '2022-09-10'),

-- 2023 Data
(1, 'Male', 'Forward World', 9, 198, 985, 4.9, 4.8, '2023-01-21'),
(2, 'Female', 'Air Max 270', 1, 150, 1250, 4.7, 4.6, '2023-02-15'),
(3, 'Male', 'React Infinity', 1, 160, 890, 4.8, 4.7, '2023-03-10'),
(4, 'Female', 'Pegasus 39', 1, 130, 1100, 4.6, 4.5, '2023-04-05'),
(5, 'Male', 'ZoomX Vaporfly', 1, 250, 750, 4.9, 4.9, '2023-05-20'),
(6, 'Female', 'Metcon 8', 2, 140, 680, 4.5, 4.4, '2023-06-12'),
(7, 'Male', 'Air Jordan 1', 3, 170, 2100, 4.8, 4.8, '2023-07-08'),
(8, 'Female', 'Blazer Mid', 3, 100, 920, 4.4, 4.3, '2023-08-14'),

-- 2024 Data
(201, 'Male', 'Forward World', 9, 210, 1200, 4.9, 4.9, '2024-01-21'),
(202, 'Female', 'Air Max 270', 1, 160, 1500, 4.8, 4.7, '2024-03-15'),
(203, 'Male', 'React Infinity', 1, 170, 1000, 4.9, 4.8, '2024-06-10');

-- ============================================
-- TABLE 6: DIM_CATEGORY_NIKE
-- ============================================
CREATE TABLE dim_category_nike (
    category_id INTEGER PRIMARY KEY,
    category_name TEXT,
    available_color TEXT,
    available_stocks INTEGER
);

INSERT INTO dim_category_nike VALUES
(1, 'Running Shoes', 'Black', 141),
(2, 'Training Shoes', 'White', 98),
(3, 'Lifestyle Shoes', 'Red', 205),
(9, 'Special Edition', 'Multi', 45);

-- ============================================
-- TABLE 7: SALES_BY_YEAR
-- ============================================
CREATE TABLE sales_by_year (
    year INTEGER PRIMARY KEY,
    sales DECIMAL(12,2)
);

INSERT INTO sales_by_year VALUES
(2020, 1000000.00),
(2021, 1250000.00),
(2022, 1500000.00),
(2023, 1425000.00),
(2024, 1710000.00);

-- ============================================
-- TABLE 8: NEW PRACTICE - CUSTOMERS & ORDERS
-- ============================================
CREATE TABLE customers_new (
    customer_id INTEGER PRIMARY KEY,
    customer_name VARCHAR(100),
    age INTEGER,
    city VARCHAR(100),
    email VARCHAR(100),
    address VARCHAR(200)
);

CREATE TABLE orders_new (
    order_id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    order_date DATE,
    amount DECIMAL(10,2),
    FOREIGN KEY (customer_id) REFERENCES customers_new(customer_id)
);

INSERT INTO customers_new VALUES
(1, 'Alice Smith', 30, 'New York', 'alice@example.com', '123 Broadway'),
(2, 'Bob Jones', 45, 'Chicago', 'bob@example.com', '456 Michigan Ave'),
(3, 'Charlie Brown', 25, 'New York', 'charlie@example.com', '789 5th Ave'),
(4, 'Diana Prince', 35, 'Los Angeles', 'diana@example.com', '101 Hollywood Blvd');

INSERT INTO orders_new VALUES
(101, 1, '2025-01-10', 100.00),
(102, 1, '2025-01-15', 200.00),
(103, 2, '2025-01-12', 50.00),
(104, 3, '2025-01-20', 500.00),
(105, 4, '2025-01-25', 150.00);

-- ============================================
-- VERIFICATION
-- ============================================
SELECT 'Setup Complete! All tables restored.' as status;
