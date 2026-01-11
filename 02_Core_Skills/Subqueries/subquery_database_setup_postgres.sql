-- ============================================
-- SUBQUERY PRACTICE DATABASE - POSTGRESQL VERSION
-- ============================================

-- Drop existing tables if they exist
DROP TABLE IF EXISTS order_items CASCADE;
DROP TABLE IF EXISTS orders CASCADE;
DROP TABLE IF EXISTS customers CASCADE;
DROP TABLE IF EXISTS products CASCADE;
DROP TABLE IF EXISTS employees CASCADE;
DROP TABLE IF EXISTS departments CASCADE;

-- ============================================
-- CUSTOMERS TABLE
-- ============================================
CREATE TABLE customers (
    customer_id SERIAL PRIMARY KEY,
    customer_name VARCHAR(100),
    email VARCHAR(100),
    city VARCHAR(50),
    state VARCHAR(2),
    signup_date DATE
);

INSERT INTO customers (customer_id, customer_name, email, city, state, signup_date) VALUES
(1, 'Alice Johnson', 'alice@email.com', 'New York', 'NY', '2023-01-15'),
(2, 'Bob Smith', 'bob@email.com', 'Los Angeles', 'CA', '2023-02-20'),
(3, 'Carol White', 'carol@email.com', 'Chicago', 'IL', '2023-01-10'),
(4, 'David Brown', 'david@email.com', 'Houston', 'TX', '2023-03-05'),
(5, 'Emma Davis', 'emma@email.com', 'Phoenix', 'AZ', '2023-02-28'),
(6, 'Frank Miller', 'frank@email.com', 'Philadelphia', 'PA', '2023-04-12'),
(7, 'Grace Lee', 'grace@email.com', 'San Antonio', 'TX', '2023-01-25'),
(8, 'Henry Wilson', 'henry@email.com', 'San Diego', 'CA', '2023-03-18'),
(9, 'Iris Martinez', 'iris@email.com', 'Dallas', 'TX', '2023-02-14'),
(10, 'Jack Taylor', 'jack@email.com', 'San Jose', 'CA', '2023-04-01');

-- ============================================
-- ORDERS TABLE
-- ============================================
CREATE TABLE orders (
    order_id SERIAL PRIMARY KEY,
    customer_id INTEGER REFERENCES customers(customer_id),
    order_date DATE,
    order_amount DECIMAL(10,2),
    order_status VARCHAR(20)
);

INSERT INTO orders (order_id, customer_id, order_date, order_amount, order_status) VALUES
-- Alice (customer 1) - High spender
(101, 1, '2024-01-15', 250.00, 'completed'),
(102, 1, '2024-02-20', 180.50, 'completed'),
(103, 1, '2024-03-10', 320.75, 'completed'),
(104, 1, '2024-04-05', 150.00, 'pending'),

-- Bob (customer 2) - Medium spender
(105, 2, '2024-01-22', 95.00, 'completed'),
(106, 2, '2024-03-15', 120.00, 'completed'),

-- Carol (customer 3) - High spender
(107, 3, '2024-02-10', 280.00, 'completed'),
(108, 3, '2024-03-25', 195.50, 'completed'),
(109, 3, '2024-04-18', 225.00, 'completed'),

-- David (customer 4) - Low spender
(110, 4, '2024-01-30', 45.00, 'completed'),

-- Emma (customer 5) - Medium spender
(111, 5, '2024-02-14', 160.00, 'completed'),
(112, 5, '2024-04-20', 85.00, 'pending'),

-- Frank (customer 6) - High spender
(113, 6, '2024-03-05', 310.00, 'completed'),
(114, 6, '2024-04-12', 275.50, 'completed'),

-- Grace (customer 7) - Low spender
(115, 7, '2024-03-20', 55.00, 'completed'),

-- Henry (customer 8) - Medium spender
(116, 8, '2024-02-28', 140.00, 'completed'),
(117, 8, '2024-04-10', 105.00, 'completed');

-- ============================================
-- PRODUCTS TABLE
-- ============================================
CREATE TABLE products (
    product_id SERIAL PRIMARY KEY,
    product_name VARCHAR(100),
    category VARCHAR(50),
    price DECIMAL(10,2),
    stock_quantity INTEGER
);

INSERT INTO products (product_id, product_name, category, price, stock_quantity) VALUES
(1, 'Laptop Pro 15', 'Electronics', 1299.99, 25),
(2, 'Wireless Mouse', 'Electronics', 29.99, 150),
(3, 'USB-C Cable', 'Electronics', 12.99, 200),
(4, 'Desk Chair', 'Furniture', 249.99, 40),
(5, 'Standing Desk', 'Furniture', 599.99, 15),
(6, 'Monitor 27"', 'Electronics', 349.99, 35),
(7, 'Keyboard Mechanical', 'Electronics', 89.99, 80),
(8, 'Desk Lamp', 'Furniture', 45.99, 60),
(9, 'Notebook Set', 'Office Supplies', 15.99, 300),
(10, 'Pen Pack', 'Office Supplies', 8.99, 500),
(11, 'Webcam HD', 'Electronics', 79.99, 45),
(12, 'Headphones', 'Electronics', 149.99, 70);

-- ============================================
-- ORDER_ITEMS TABLE
-- ============================================
CREATE TABLE order_items (
    order_item_id SERIAL PRIMARY KEY,
    order_id INTEGER REFERENCES orders(order_id),
    product_id INTEGER REFERENCES products(product_id),
    quantity INTEGER,
    item_price DECIMAL(10,2)
);

INSERT INTO order_items (order_item_id, order_id, product_id, quantity, item_price) VALUES
-- Order 101 (Alice)
(1, 101, 2, 2, 29.99),
(2, 101, 3, 3, 12.99),
(3, 101, 7, 1, 89.99),
-- Order 102 (Alice)
(4, 102, 11, 1, 79.99),
(5, 102, 9, 5, 15.99),
-- Order 103 (Alice)
(6, 103, 4, 1, 249.99),
(7, 103, 8, 1, 45.99),
-- Order 104 (Alice)
(8, 104, 12, 1, 149.99),
-- Order 105 (Bob)
(9, 105, 2, 1, 29.99),
(10, 105, 3, 5, 12.99),
-- Order 106 (Bob)
(11, 106, 7, 1, 89.99),
(12, 106, 9, 2, 15.99),
-- Order 107 (Carol)
(13, 107, 6, 1, 349.99),
-- Order 108 (Carol)
(14, 108, 11, 1, 79.99),
(15, 108, 12, 1, 149.99),
-- Order 109 (Carol)
(16, 109, 4, 1, 249.99),
-- Order 110 (David)
(17, 110, 10, 5, 8.99),
-- Order 111 (Emma)
(18, 111, 12, 1, 149.99),
-- Order 112 (Emma)
(19, 112, 2, 1, 29.99),
(20, 112, 3, 4, 12.99),
-- Order 113 (Frank)
(21, 113, 5, 1, 599.99),
-- Order 114 (Frank)
(22, 114, 6, 1, 349.99),
-- Order 115 (Grace)
(23, 115, 9, 3, 15.99),
-- Order 116 (Henry)
(24, 116, 7, 1, 89.99),
(25, 116, 2, 1, 29.99),
-- Order 117 (Henry)
(26, 117, 11, 1, 79.99);

-- ============================================
-- DEPARTMENTS TABLE
-- ============================================
CREATE TABLE departments (
    department_id SERIAL PRIMARY KEY,
    department_name VARCHAR(100),
    location VARCHAR(50)
);

INSERT INTO departments (department_id, department_name, location) VALUES
(1, 'Sales', 'New York'),
(2, 'Engineering', 'San Francisco'),
(3, 'Marketing', 'Chicago'),
(4, 'Customer Support', 'Austin'),
(5, 'HR', 'Boston');

-- ============================================
-- EMPLOYEES TABLE
-- ============================================
CREATE TABLE employees (
    employee_id SERIAL PRIMARY KEY,
    employee_name VARCHAR(100),
    department_id INTEGER REFERENCES departments(department_id),
    salary DECIMAL(10,2),
    hire_date DATE,
    manager_id INTEGER
);

INSERT INTO employees (employee_id, employee_name, department_id, salary, hire_date, manager_id) VALUES
-- Sales (dept 1)
(1, 'Sarah Johnson', 1, 75000.00, '2020-01-15', NULL),
(2, 'Mike Chen', 1, 65000.00, '2021-03-20', 1),
(3, 'Lisa Anderson', 1, 68000.00, '2021-06-10', 1),
(4, 'Tom Wilson', 1, 62000.00, '2022-02-14', 1),
-- Engineering (dept 2)
(5, 'David Kim', 2, 95000.00, '2019-05-01', NULL),
(6, 'Emily Rodriguez', 2, 88000.00, '2020-08-15', 5),
(7, 'James Lee', 2, 92000.00, '2020-11-20', 5),
(8, 'Anna Martinez', 2, 85000.00, '2021-04-12', 5),
(9, 'Chris Brown', 2, 90000.00, '2021-09-01', 5),
-- Marketing (dept 3)
(10, 'Jennifer Davis', 3, 72000.00, '2020-07-10', NULL),
(11, 'Robert Taylor', 3, 68000.00, '2021-01-25', 10),
(12, 'Michelle White', 3, 70000.00, '2021-10-05', 10),
-- Customer Support (dept 4)
(13, 'Kevin Garcia', 4, 55000.00, '2021-02-20', NULL),
(14, 'Amanda Lopez', 4, 52000.00, '2021-08-15', 13),
(15, 'Brian Miller', 4, 53000.00, '2022-01-10', 13),
(16, 'Jessica Moore', 4, 54000.00, '2022-03-22', 13),
-- HR (dept 5)
(17, 'Patricia Jackson', 5, 78000.00, '2019-09-12', NULL),
(18, 'Daniel Harris', 5, 65000.00, '2020-12-01', 17);

-- Verify the data loaded
SELECT 'Database setup complete!' as status;
SELECT 'Customers: ' || COUNT(*) as info FROM customers
UNION ALL SELECT 'Orders: ' || COUNT(*) FROM orders
UNION ALL SELECT 'Products: ' || COUNT(*) FROM products
UNION ALL SELECT 'Order Items: ' || COUNT(*) FROM order_items
UNION ALL SELECT 'Departments: ' || COUNT(*) FROM departments
UNION ALL SELECT 'Employees: ' || COUNT(*) FROM employees;
