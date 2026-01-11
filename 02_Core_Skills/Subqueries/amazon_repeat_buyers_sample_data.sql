-- ============================================
-- SAMPLE DATA: Amazon Repeat Buyers Problem
-- ============================================

-- Table: customers_amz
CREATE TABLE customers_amz (
    customer_id INT PRIMARY KEY,
    customer_name VARCHAR(100),
    email VARCHAR(100),
    registration_date DATE
);

INSERT INTO
    customers_amz (
        customer_id,
        customer_name,
        email,
        registration_date
    )
VALUES (
        1,
        'Alice Johnson',
        'alice.j@email.com',
        '2022-01-15'
    ),
    (
        2,
        'Bob Smith',
        'bob.smith@email.com',
        '2022-02-20'
    ),
    (
        3,
        'Carol White',
        'carol.w@email.com',
        '2022-03-10'
    ),
    (
        4,
        'David Brown',
        'david.b@email.com',
        '2022-04-05'
    ),
    (
        5,
        'Emma Davis',
        'emma.d@email.com',
        '2022-05-12'
    );

-- Table: products_amz
CREATE TABLE products_amz (
    product_id INT PRIMARY KEY,
    product_name VARCHAR(100),
    category VARCHAR(50),
    launch_date DATE,
    price DECIMAL(10, 2),
    stock_count INT
);

INSERT INTO
    products_amz (
        product_id,
        product_name,
        category,
        launch_date,
        price,
        stock_count
    )
VALUES (
        101,
        'Wireless Mouse',
        'Electronics',
        '2021-06-01',
        25.99,
        500
    ),
    (
        102,
        'USB-C Cable',
        'Electronics',
        '2021-07-15',
        12.99,
        1000
    ),
    (
        103,
        'Coffee Beans 1lb',
        'Grocery',
        '2021-08-20',
        15.99,
        300
    ),
    (
        104,
        'Yoga Mat',
        'Sports',
        '2021-09-10',
        29.99,
        200
    ),
    (
        105,
        'Water Bottle',
        'Sports',
        '2021-10-05',
        18.99,
        400
    ),
    (
        106,
        'Notebook Pack',
        'Office',
        '2021-11-12',
        9.99,
        600
    );

-- Table: orders_amz
CREATE TABLE orders_amz (
    order_id INT PRIMARY KEY,
    customer_id INT,
    order_date DATE,
    shipping_status VARCHAR(50),
    shipping_address VARCHAR(200)
);

INSERT INTO
    orders_amz (
        order_id,
        customer_id,
        order_date,
        shipping_status,
        shipping_address
    )
VALUES
    -- Alice's orders (she loves Coffee Beans!)
    (
        1001,
        1,
        '2023-01-10',
        'Delivered',
        '123 Main St'
    ),
    (
        1002,
        1,
        '2023-02-15',
        'Delivered',
        '123 Main St'
    ),
    (
        1003,
        1,
        '2023-03-20',
        'Delivered',
        '123 Main St'
    ),
    (
        1004,
        1,
        '2023-04-25',
        'Delivered',
        '123 Main St'
    ),
    (
        1005,
        1,
        '2023-05-30',
        'Delivered',
        '123 Main St'
    ),

-- Bob's orders (he's a Wireless Mouse collector!)
(
    2001,
    2,
    '2023-01-05',
    'Delivered',
    '456 Oak Ave'
),
(
    2002,
    2,
    '2023-02-10',
    'Delivered',
    '456 Oak Ave'
),
(
    2003,
    2,
    '2023-03-15',
    'Delivered',
    '456 Oak Ave'
),
(
    2004,
    2,
    '2023-04-20',
    'Delivered',
    '456 Oak Ave'
),

-- Carol's orders (USB-C Cable enthusiast)
(
    3001,
    3,
    '2023-01-12',
    'Delivered',
    '789 Pine Rd'
),
(
    3002,
    3,
    '2023-02-18',
    'Delivered',
    '789 Pine Rd'
),
(
    3003,
    3,
    '2023-03-22',
    'Delivered',
    '789 Pine Rd'
),

-- David's orders (only 2 of same product - won't qualify)
(
    4001,
    4,
    '2023-01-08',
    'Delivered',
    '321 Elm St'
),
(
    4002,
    4,
    '2023-02-12',
    'Delivered',
    '321 Elm St'
),

-- Emma's orders (buys multiple products but 3+ of Water Bottle)
(
    5001,
    5,
    '2023-01-20',
    'Delivered',
    '654 Maple Dr'
),
(
    5002,
    5,
    '2023-02-25',
    'Delivered',
    '654 Maple Dr'
),
(
    5003,
    5,
    '2023-03-28',
    'Delivered',
    '654 Maple Dr'
),
(
    5004,
    5,
    '2023-04-30',
    'Delivered',
    '654 Maple Dr'
);

-- Table: orderdetails
CREATE TABLE orderdetails (
    order_detail_id INT PRIMARY KEY,
    order_id INT,
    product_id INT,
    quantity INT,
    total_price DECIMAL(10, 2)
);

INSERT INTO
    orderdetails (
        order_detail_id,
        order_id,
        product_id,
        quantity,
        total_price
    )
VALUES
    -- Alice's purchases (Coffee Beans x5, Wireless Mouse x2)
    (10001, 1001, 103, 1, 15.99), -- Coffee Beans
    (10002, 1002, 103, 1, 15.99), -- Coffee Beans
    (10003, 1003, 103, 1, 15.99), -- Coffee Beans
    (10004, 1004, 103, 1, 15.99), -- Coffee Beans
    (10005, 1005, 103, 1, 15.99), -- Coffee Beans
    (10006, 1001, 101, 1, 25.99), -- Wireless Mouse
    (10007, 1003, 101, 1, 25.99), -- Wireless Mouse

-- Bob's purchases (Wireless Mouse x4, USB-C Cable x2)
(20001, 2001, 101, 1, 25.99), -- Wireless Mouse
(20002, 2002, 101, 1, 25.99), -- Wireless Mouse
(20003, 2003, 101, 1, 25.99), -- Wireless Mouse
(20004, 2004, 101, 1, 25.99), -- Wireless Mouse
(20005, 2001, 102, 1, 12.99), -- USB-C Cable
(20006, 2003, 102, 1, 12.99), -- USB-C Cable

-- Carol's purchases (USB-C Cable x3)
(30001, 3001, 102, 1, 12.99), -- USB-C Cable
(30002, 3002, 102, 1, 12.99), -- USB-C Cable
(30003, 3003, 102, 1, 12.99), -- USB-C Cable

-- David's purchases (Yoga Mat x2 - won't qualify)
(40001, 4001, 104, 1, 29.99), -- Yoga Mat
(40002, 4002, 104, 1, 29.99), -- Yoga Mat

-- Emma's purchases (Water Bottle x3, Notebook x2)
(50001, 5001, 105, 1, 18.99), -- Water Bottle
(50002, 5002, 105, 1, 18.99), -- Water Bottle
(50003, 5003, 105, 1, 18.99), -- Water Bottle
(50004, 5001, 106, 1, 9.99), -- Notebook
(50005, 5004, 106, 1, 9.99);
-- Notebook

-- ============================================
-- EXPECTED RESULTS
-- ============================================

/*
Customers who bought the same product 3+ times:

1. Alice Johnson - Coffee Beans (5 times) ✅ Most purchased
2. Bob Smith - Wireless Mouse (4 times) ✅ Most purchased
3. Carol White - USB-C Cable (3 times) ✅ Most purchased
4. Emma Davis - Water Bottle (3 times) ✅ Most purchased

David Brown - Only bought Yoga Mat 2 times (doesn't qualify)

Expected Output:
customer_name    | product_name      | times_purchased
-----------------+-------------------+----------------
Alice Johnson    | Coffee Beans 1lb  | 5
Bob Smith        | Wireless Mouse    | 4
Carol White      | USB-C Cable       | 3
Emma Davis       | Water Bottle      | 3
*/