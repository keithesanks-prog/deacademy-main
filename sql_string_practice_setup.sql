-- ============================================
-- SQL STRING FUNCTIONS PRACTICE ENVIRONMENT
-- ============================================
-- This file sets up sample tables for practicing string manipulation
-- Run this to create your practice database
-- ============================================

-- Clean up if tables already exist
DROP TABLE IF EXISTS phones;
DROP TABLE IF EXISTS emails;
DROP TABLE IF EXISTS addresses;
DROP TABLE IF EXISTS product_codes;

-- ============================================
-- TABLE 1: PHONES (String Splitting Practice)
-- ============================================
CREATE TABLE phones (
    phone_id TEXT PRIMARY KEY,
    phone_name TEXT,
    price DECIMAL(10,2)
);

INSERT INTO phones VALUES
('1', 'Apple - iPhone 14 Pro', 999.00),
('2', 'Samsung : Galaxy S23', 899.00),
('3', 'Google * Pixel 7', 599.00),
('4', 'OnePlus ~ 11', 699.00),
('5', 'Xiaomi - Redmi Note 12', 299.00),
('6', 'Motorola : Edge 40', 499.00),
('7', 'Nokia * G50', 249.00),
('8', 'Sony ~ Xperia 5', 799.00),
('9', 'Huawei - P60 Pro', 899.00),
('10', 'Oppo : Find X6', 749.00);

-- ============================================
-- TABLE 2: EMAILS (Pattern Extraction)
-- ============================================
CREATE TABLE emails (
    user_id INTEGER PRIMARY KEY,
    full_name TEXT,
    email TEXT,
    signup_date DATE
);

INSERT INTO emails VALUES
(1, 'John Smith', 'john.smith@gmail.com', '2023-01-15'),
(2, 'Maria Garcia', 'maria.garcia@yahoo.com', '2023-02-20'),
(3, 'Chen Wei', 'chen.wei@company.com', '2023-03-10'),
(4, 'Anna Kowalski', 'anna.k@outlook.com', '2023-04-05'),
(5, 'James Brown', 'jbrown@gmail.com', '2023-05-12'),
(6, 'Sophie Martin', 'sophie.martin@hotmail.com', '2023-06-18'),
(7, 'Lars Hansen', 'lars.hansen@company.com', '2023-07-22'),
(8, 'Yuki Tanaka', 'yuki.t@gmail.com', '2023-08-30');

-- ============================================
-- TABLE 3: ADDRESSES (Multi-part Splitting)
-- ============================================
CREATE TABLE addresses (
    address_id INTEGER PRIMARY KEY,
    customer_name TEXT,
    full_address TEXT
);

INSERT INTO addresses VALUES
(1, 'Alice Johnson', '123 Main St, New York, NY, 10001'),
(2, 'Bob Williams', '456 Oak Ave, Los Angeles, CA, 90001'),
(3, 'Carol Davis', '789 Pine Rd, Chicago, IL, 60601'),
(4, 'David Miller', '321 Elm St, Houston, TX, 77001'),
(5, 'Eve Wilson', '654 Maple Dr, Phoenix, AZ, 85001'),
(6, 'Frank Moore', '987 Cedar Ln, Philadelphia, PA, 19101'),
(7, 'Grace Taylor', '147 Birch Way, San Antonio, TX, 78201'),
(8, 'Henry Anderson', '258 Spruce Ct, San Diego, CA, 92101');

-- ============================================
-- TABLE 4: PRODUCT_CODES (Pattern Matching)
-- ============================================
CREATE TABLE product_codes (
    product_id INTEGER PRIMARY KEY,
    product_code TEXT,
    description TEXT,
    stock INTEGER
);

INSERT INTO product_codes VALUES
(1, 'ELEC-LAP-001', 'Laptop Computer', 45),
(2, 'FURN-CHA-023', 'Office Chair', 120),
(3, 'ELEC-MON-015', 'Monitor 27 inch', 67),
(4, 'APPL-COF-008', 'Coffee Maker', 89),
(5, 'FURN-DES-042', 'Standing Desk', 34),
(6, 'ELEC-KEY-019', 'Wireless Keyboard', 156),
(7, 'APPL-BLE-005', 'Blender', 78),
(8, 'ELEC-MOU-011', 'Gaming Mouse', 203);

-- ============================================
-- VERIFICATION QUERIES
-- ============================================

SELECT 'Phones Table:' as info;
SELECT * FROM phones;

SELECT 'Emails Table:' as info;
SELECT * FROM emails;

SELECT 'Addresses Table:' as info;
SELECT * FROM addresses;

SELECT 'Product Codes Table:' as info;
SELECT * FROM product_codes;
