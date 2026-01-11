# 🗄️ Real-World Data Modeling Examples

**Database schemas for real companies - Learn by example!**

---

## 📦 1. DROPBOX - File Storage System

### **Core Tables**

```sql
-- Users Table
CREATE TABLE users (
    user_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash CHAR(64) NOT NULL,              -- SHA-256 hash
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    storage_quota_gb INT DEFAULT 2,                -- Free tier: 2GB
    storage_used_bytes BIGINT DEFAULT 0,
    account_type ENUM('free', 'plus', 'professional', 'business'),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP,
    is_active TINYINT(1) DEFAULT 1
);

-- Files Table
CREATE TABLE files (
    file_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT NOT NULL,
    folder_id BIGINT,                              -- NULL = root folder
    file_name VARCHAR(255) NOT NULL,
    file_path VARCHAR(1000) NOT NULL,              -- /Photos/vacation.jpg
    file_size_bytes BIGINT NOT NULL,
    file_type VARCHAR(50),                         -- 'image/jpeg', 'application/pdf'
    mime_type VARCHAR(100),
    storage_location VARCHAR(500),                 -- S3 bucket path
    is_deleted TINYINT(1) DEFAULT 0,
    is_shared TINYINT(1) DEFAULT 0,
    version_number INT DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    modified_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP NULL,
    
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    INDEX idx_user_files (user_id, is_deleted),
    INDEX idx_folder (folder_id)
);

-- Folders Table
CREATE TABLE folders (
    folder_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT NOT NULL,
    parent_folder_id BIGINT,                       -- NULL = root
    folder_name VARCHAR(255) NOT NULL,
    folder_path VARCHAR(1000) NOT NULL,            -- /Photos/Vacation
    is_deleted TINYINT(1) DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (parent_folder_id) REFERENCES folders(folder_id)
);

-- Shared Links Table
CREATE TABLE shared_links (
    link_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    file_id BIGINT NOT NULL,
    shared_by_user_id BIGINT NOT NULL,
    share_token CHAR(32) UNIQUE NOT NULL,          -- Random token
    password_hash CHAR(64),                        -- Optional password
    expiration_date DATETIME,
    max_downloads INT,
    download_count INT DEFAULT 0,
    is_active TINYINT(1) DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (file_id) REFERENCES files(file_id),
    FOREIGN KEY (shared_by_user_id) REFERENCES users(user_id)
);

-- File Versions Table (Version History)
CREATE TABLE file_versions (
    version_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    file_id BIGINT NOT NULL,
    version_number INT NOT NULL,
    file_size_bytes BIGINT NOT NULL,
    storage_location VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (file_id) REFERENCES files(file_id),
    UNIQUE KEY unique_file_version (file_id, version_number)
);
```

**💡 Key Design Decisions:**
- `storage_used_bytes` as BIGINT (can handle TB of data)
- `file_path` for quick lookups
- `is_deleted` for soft deletes (trash/recovery)
- `share_token` CHAR(32) for secure sharing
- Version history in separate table

---

## 🎬 2. NETFLIX - Streaming Platform

### **Core Tables**

```sql
-- Users/Accounts Table
CREATE TABLE accounts (
    account_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash CHAR(64) NOT NULL,
    subscription_plan ENUM('basic', 'standard', 'premium') NOT NULL,
    billing_date DATE NOT NULL,
    payment_method_id INT,
    is_active TINYINT(1) DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    subscription_end_date DATE
);

-- Profiles Table (Multiple profiles per account)
CREATE TABLE profiles (
    profile_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    account_id BIGINT NOT NULL,
    profile_name VARCHAR(100) NOT NULL,
    is_kids_profile TINYINT(1) DEFAULT 0,
    avatar_url VARCHAR(255),
    language_preference CHAR(2) DEFAULT 'en',      -- ISO language code
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (account_id) REFERENCES accounts(account_id),
    INDEX idx_account_profiles (account_id)
);

-- Movies/Shows Table
CREATE TABLE content (
    content_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(255) NOT NULL,
    content_type ENUM('movie', 'series') NOT NULL,
    description TEXT,
    release_year SMALLINT,
    duration_minutes SMALLINT,                     -- For movies
    rating VARCHAR(10),                            -- 'PG-13', 'R', 'TV-MA'
    imdb_rating DECIMAL(3,1),                      -- 8.5
    thumbnail_url VARCHAR(500),
    video_url VARCHAR(500),
    is_available TINYINT(1) DEFAULT 1,
    added_date DATE,
    removal_date DATE,
    
    INDEX idx_type (content_type),
    INDEX idx_available (is_available, added_date)
);

-- Series Episodes Table
CREATE TABLE episodes (
    episode_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    content_id BIGINT NOT NULL,                    -- Links to series
    season_number TINYINT NOT NULL,
    episode_number TINYINT NOT NULL,
    episode_title VARCHAR(255),
    description TEXT,
    duration_minutes SMALLINT,
    video_url VARCHAR(500),
    thumbnail_url VARCHAR(500),
    air_date DATE,
    
    FOREIGN KEY (content_id) REFERENCES content(content_id),
    UNIQUE KEY unique_episode (content_id, season_number, episode_number)
);

-- Genres Table
CREATE TABLE genres (
    genre_id INT PRIMARY KEY AUTO_INCREMENT,
    genre_name VARCHAR(50) UNIQUE NOT NULL         -- 'Action', 'Comedy', 'Drama'
);

-- Content-Genre Mapping (Many-to-Many)
CREATE TABLE content_genres (
    content_id BIGINT NOT NULL,
    genre_id INT NOT NULL,
    
    PRIMARY KEY (content_id, genre_id),
    FOREIGN KEY (content_id) REFERENCES content(content_id),
    FOREIGN KEY (genre_id) REFERENCES genres(genre_id)
);

-- Watch History Table
CREATE TABLE watch_history (
    watch_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    profile_id BIGINT NOT NULL,
    content_id BIGINT NOT NULL,
    episode_id BIGINT,                             -- NULL for movies
    watch_duration_seconds INT NOT NULL,
    total_duration_seconds INT NOT NULL,
    progress_percentage TINYINT,                   -- 0-100
    watched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed TINYINT(1) DEFAULT 0,
    
    FOREIGN KEY (profile_id) REFERENCES profiles(profile_id),
    FOREIGN KEY (content_id) REFERENCES content(content_id),
    FOREIGN KEY (episode_id) REFERENCES episodes(episode_id),
    INDEX idx_profile_history (profile_id, watched_at)
);

-- My List (Watchlist)
CREATE TABLE watchlist (
    watchlist_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    profile_id BIGINT NOT NULL,
    content_id BIGINT NOT NULL,
    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (profile_id) REFERENCES profiles(profile_id),
    FOREIGN KEY (content_id) REFERENCES content(content_id),
    UNIQUE KEY unique_watchlist (profile_id, content_id)
);

-- Ratings Table
CREATE TABLE ratings (
    rating_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    profile_id BIGINT NOT NULL,
    content_id BIGINT NOT NULL,
    rating TINYINT NOT NULL,                       -- 1-5 stars
    rated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (profile_id) REFERENCES profiles(profile_id),
    FOREIGN KEY (content_id) REFERENCES content(content_id),
    UNIQUE KEY unique_rating (profile_id, content_id)
);
```

**💡 Key Design Decisions:**
- Separate `accounts` and `profiles` (one account, many profiles)
- `content_type` ENUM for movies vs. series
- `episodes` table only for series
- `progress_percentage` for "Continue Watching"
- Many-to-many for genres (one movie, many genres)

---

## 🛒 3. WALMART - E-Commerce Platform

### **Core Tables**

```sql
-- Customers Table
CREATE TABLE customers (
    customer_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash CHAR(64) NOT NULL,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    phone VARCHAR(20),
    date_of_birth DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP,
    is_active TINYINT(1) DEFAULT 1
);

-- Addresses Table
CREATE TABLE addresses (
    address_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    customer_id BIGINT NOT NULL,
    address_type ENUM('shipping', 'billing') NOT NULL,
    street_address VARCHAR(255) NOT NULL,
    city VARCHAR(100) NOT NULL,
    state CHAR(2) NOT NULL,                        -- 'CA', 'NY'
    zip_code CHAR(5) NOT NULL,
    country CHAR(2) DEFAULT 'US',
    is_default TINYINT(1) DEFAULT 0,
    
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    INDEX idx_customer_addresses (customer_id)
);

-- Products Table
CREATE TABLE products (
    product_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    sku CHAR(12) UNIQUE NOT NULL,                  -- 'PROD-1234567'
    product_name VARCHAR(255) NOT NULL,
    description TEXT,
    category_id INT NOT NULL,
    brand VARCHAR(100),
    price DECIMAL(10,2) NOT NULL,                  -- $9,999,999.99
    sale_price DECIMAL(10,2),
    cost DECIMAL(10,2),                            -- For profit calculation
    stock_quantity INT NOT NULL DEFAULT 0,
    reorder_level INT DEFAULT 10,
    weight_lbs DECIMAL(8,2),
    dimensions VARCHAR(50),                        -- '10x8x6 inches'
    is_active TINYINT(1) DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    INDEX idx_category (category_id),
    INDEX idx_sku (sku)
);

-- Categories Table
CREATE TABLE categories (
    category_id INT PRIMARY KEY AUTO_INCREMENT,
    category_name VARCHAR(100) NOT NULL,
    parent_category_id INT,                        -- For subcategories
    
    FOREIGN KEY (parent_category_id) REFERENCES categories(category_id)
);

-- Orders Table
CREATE TABLE orders (
    order_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    customer_id BIGINT NOT NULL,
    order_number CHAR(16) UNIQUE NOT NULL,         -- 'ORD-202412110001'
    order_status ENUM('pending', 'processing', 'shipped', 'delivered', 'cancelled') DEFAULT 'pending',
    subtotal DECIMAL(10,2) NOT NULL,
    tax DECIMAL(10,2) NOT NULL,
    shipping_cost DECIMAL(10,2) NOT NULL,
    total_amount DECIMAL(10,2) NOT NULL,
    payment_method ENUM('credit_card', 'debit_card', 'paypal', 'gift_card'),
    shipping_address_id BIGINT NOT NULL,
    billing_address_id BIGINT NOT NULL,
    tracking_number VARCHAR(50),
    ordered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    shipped_at TIMESTAMP NULL,
    delivered_at TIMESTAMP NULL,
    
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    FOREIGN KEY (shipping_address_id) REFERENCES addresses(address_id),
    FOREIGN KEY (billing_address_id) REFERENCES addresses(address_id),
    INDEX idx_customer_orders (customer_id, ordered_at),
    INDEX idx_status (order_status)
);

-- Order Items Table
CREATE TABLE order_items (
    order_item_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    order_id BIGINT NOT NULL,
    product_id BIGINT NOT NULL,
    quantity SMALLINT NOT NULL,
    unit_price DECIMAL(10,2) NOT NULL,             -- Price at time of order
    discount_amount DECIMAL(10,2) DEFAULT 0,
    total_price DECIMAL(10,2) NOT NULL,            -- quantity * unit_price - discount
    
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id),
    INDEX idx_order (order_id)
);

-- Shopping Cart Table
CREATE TABLE cart (
    cart_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    customer_id BIGINT NOT NULL,
    product_id BIGINT NOT NULL,
    quantity SMALLINT NOT NULL DEFAULT 1,
    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id),
    UNIQUE KEY unique_cart_item (customer_id, product_id)
);

-- Reviews Table
CREATE TABLE reviews (
    review_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    product_id BIGINT NOT NULL,
    customer_id BIGINT NOT NULL,
    rating TINYINT NOT NULL,                       -- 1-5 stars
    review_title VARCHAR(200),
    review_text TEXT,
    is_verified_purchase TINYINT(1) DEFAULT 0,
    helpful_count INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (product_id) REFERENCES products(product_id),
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    INDEX idx_product_reviews (product_id, created_at)
);

-- Inventory Table (Store-specific stock)
CREATE TABLE inventory (
    inventory_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    product_id BIGINT NOT NULL,
    store_id INT NOT NULL,
    quantity INT NOT NULL DEFAULT 0,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (product_id) REFERENCES products(product_id),
    UNIQUE KEY unique_store_product (store_id, product_id)
);
```

**💡 Key Design Decisions:**
- `price` as DECIMAL(10,2) for exact money values
- `order_number` separate from `order_id` (user-friendly)
- `unit_price` in order_items (price at time of purchase)
- Separate `cart` table for shopping cart
- `is_verified_purchase` for trusted reviews
- Store-specific inventory tracking

---

## 📊 Quick Comparison

| Feature | Dropbox | Netflix | Walmart |
|---------|---------|---------|---------|
| **Main Entity** | Files | Content | Products |
| **User Model** | Single user | Account → Profiles | Customers |
| **Storage Focus** | File metadata | Watch history | Orders & Inventory |
| **Key Metric** | Storage used | Watch time | Revenue |
| **Sharing** | File links | Profiles | N/A |
| **Versioning** | File versions | Seasons/Episodes | N/A |

---

## 🎯 Common Patterns Across All

### **1. Soft Deletes**
```sql
is_deleted TINYINT(1) DEFAULT 0
deleted_at TIMESTAMP NULL
```

### **2. Timestamps**
```sql
created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
```

### **3. Status Tracking**
```sql
status ENUM('active', 'inactive', 'pending', 'cancelled')
```

### **4. Money Fields**
```sql
price DECIMAL(10,2)  -- Always DECIMAL for money!
```

### **5. Foreign Keys & Indexes**
```sql
FOREIGN KEY (user_id) REFERENCES users(user_id)
INDEX idx_user_created (user_id, created_at)
```

---

## 💡 Key Takeaways

1. **Choose appropriate data types** - BIGINT for IDs, DECIMAL for money
2. **Use ENUMs** for fixed options (status, type)
3. **Index frequently queried columns** - user_id, created_at
4. **Separate tables for relationships** - Many-to-many (content_genres)
5. **Store historical data** - unit_price in order_items
6. **Use soft deletes** - is_deleted flag instead of DELETE
7. **Normalize when needed** - Separate addresses, profiles tables

---

**Next Steps:** Study these schemas, understand the relationships, and try designing your own!
