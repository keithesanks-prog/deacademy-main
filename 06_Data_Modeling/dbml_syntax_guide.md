# 🗄️ DBML - Database Markup Language Guide

**Learn data modeling syntax and best practices**

---

## 🎯 What is DBML?

**DBML (Database Markup Language)** is a simple, readable language to define database schemas.

**Think of it like:**
- SQL = Building the actual house
- DBML = Drawing the blueprint

**Why use DBML?**
- ✅ Easy to read and write
- ✅ Creates visual diagrams automatically
- ✅ Can convert to SQL
- ✅ Great for documentation
- ✅ Used by tools like dbdiagram.io

---

## 📝 Basic Syntax

### **1. Defining a Table**

```dbml
Table users {
  user_id int [pk, increment]           // Primary key, auto-increment
  email varchar(255) [unique, not null] // Unique email, required
  password_hash char(64) [not null]     // Required field
  first_name varchar(100)               // Optional field
  age tinyint                           // Small integer
  created_at timestamp [default: `now()`] // Default to current time
}
```

**Syntax Breakdown:**
```
Table table_name {
  column_name data_type [attributes]
}
```

---

## 🔑 Column Attributes

### **Primary Keys**

```dbml
Table products {
  product_id bigint [pk]              // Simple primary key
  // OR
  product_id bigint [primary key]     // Same thing
  // OR
  product_id bigint [pk, increment]   // Auto-incrementing
}
```

### **Composite Primary Keys** (Multiple columns)

```dbml
Table order_items {
  order_id bigint
  product_id bigint
  quantity int
  
  Indexes {
    (order_id, product_id) [pk]  // Both together = primary key
  }
}
```

### **Common Attributes**

```dbml
Table users {
  id int [pk, increment]              // Primary key, auto-increment
  email varchar [unique]              // Must be unique
  name varchar [not null]             // Cannot be NULL
  age int [default: 18]               // Default value
  status varchar [default: 'active']  // Default string
  created_at timestamp [default: `now()`] // Default function
  
  Note: 'This table stores user information' // Table note
}
```

**All Attributes:**
- `pk` or `primary key` - Primary key
- `increment` - Auto-increment
- `unique` - Must be unique
- `not null` - Cannot be NULL
- `default: value` - Default value
- `note: 'text'` - Add a note/comment

---

## 🔗 Relationships (Foreign Keys)

### **Basic Relationship Syntax**

```dbml
// One-to-Many: One user has many orders
Ref: orders.user_id > users.user_id

// Read as: "orders.user_id references users.user_id"
```

### **Relationship Types**

```dbml
// One-to-Many (most common)
Ref: orders.customer_id > customers.customer_id
// Many orders → One customer

// One-to-One
Ref: user_profiles.user_id - users.user_id
// One profile → One user

// Many-to-Many (through junction table)
Ref: user_roles.user_id > users.user_id
Ref: user_roles.role_id > roles.role_id
```

**Symbols:**
- `>` = One-to-Many (most common)
- `-` = One-to-One
- `<` = Many-to-One (same as >, just reversed)
- `<>` = Many-to-Many (rarely used, prefer junction tables)

---

## 📊 Indexes

```dbml
Table users {
  user_id int [pk]
  email varchar
  first_name varchar
  last_name varchar
  created_at timestamp
  
  Indexes {
    email [unique]                        // Unique index
    (first_name, last_name) [name: 'name_idx'] // Composite index
    created_at [name: 'created_idx']      // Regular index
  }
}
```

**Why Indexes?**
- Speed up queries on frequently searched columns
- Enforce uniqueness
- Improve JOIN performance

---

## 🎬 Real-World Example: Netflix

```dbml
// Accounts Table
Table accounts {
  account_id bigint [pk, increment]
  email varchar(255) [unique, not null]
  password_hash char(64) [not null]
  subscription_plan varchar(20) [default: 'basic']
  created_at timestamp [default: `now()`]
  
  Note: 'Main account - one per subscription'
}

// Profiles Table (One account, many profiles)
Table profiles {
  profile_id bigint [pk, increment]
  account_id bigint [not null]
  profile_name varchar(100) [not null]
  is_kids_profile boolean [default: false]
  avatar_url varchar(255)
  created_at timestamp [default: `now()`]
  
  Note: 'Multiple profiles per account (Mom, Dad, Kids)'
}

// Content Table (Movies & Series)
Table content {
  content_id bigint [pk, increment]
  title varchar(255) [not null]
  content_type varchar(10) [not null] // 'movie' or 'series'
  description text
  release_year smallint
  rating varchar(10) // 'PG-13', 'R', 'TV-MA'
  imdb_rating decimal(3,1)
  added_date date
  
  Indexes {
    title [name: 'title_idx']
    content_type [name: 'type_idx']
  }
}

// Watch History Table
Table watch_history {
  watch_id bigint [pk, increment]
  profile_id bigint [not null]
  content_id bigint [not null]
  watch_duration_seconds int [not null]
  progress_percentage tinyint // 0-100
  watched_at timestamp [default: `now()`]
  completed boolean [default: false]
  
  Indexes {
    (profile_id, watched_at) [name: 'profile_history_idx']
  }
}

// Relationships
Ref: profiles.account_id > accounts.account_id
Ref: watch_history.profile_id > profiles.profile_id
Ref: watch_history.content_id > content.content_id
```

**Visual Representation:**
```
accounts (1) ──→ (many) profiles
                    │
                    │ (1)
                    ↓
                  (many) watch_history
                    │
                    │ (many)
                    ↓
                  (1) content
```

---

## 🛒 Real-World Example: E-Commerce

```dbml
// Customers
Table customers {
  customer_id bigint [pk, increment]
  email varchar(255) [unique, not null]
  first_name varchar(100)
  last_name varchar(100)
  created_at timestamp [default: `now()`]
}

// Products
Table products {
  product_id bigint [pk, increment]
  sku char(12) [unique, not null]
  product_name varchar(255) [not null]
  price decimal(10,2) [not null]
  stock_quantity int [default: 0]
  created_at timestamp [default: `now()`]
  
  Indexes {
    sku [unique, name: 'sku_idx']
    product_name [name: 'name_idx']
  }
}

// Orders
Table orders {
  order_id bigint [pk, increment]
  customer_id bigint [not null]
  order_number char(16) [unique, not null]
  order_status varchar(20) [default: 'pending']
  total_amount decimal(10,2) [not null]
  ordered_at timestamp [default: `now()`]
  
  Indexes {
    order_number [unique]
    (customer_id, ordered_at) [name: 'customer_orders_idx']
  }
}

// Order Items (Junction Table)
Table order_items {
  order_item_id bigint [pk, increment]
  order_id bigint [not null]
  product_id bigint [not null]
  quantity smallint [not null]
  unit_price decimal(10,2) [not null] // Price at time of order
  total_price decimal(10,2) [not null]
  
  Indexes {
    (order_id, product_id) [name: 'order_product_idx']
  }
}

// Relationships
Ref: orders.customer_id > customers.customer_id
Ref: order_items.order_id > orders.order_id
Ref: order_items.product_id > products.product_id
```

---

## 🎯 Best Practices

### **1. Naming Conventions**

```dbml
// ✅ GOOD: Clear, consistent names
Table users {
  user_id bigint [pk]      // Singular table name
  email varchar            // Lowercase, underscores
  created_at timestamp     // Descriptive
}

// ❌ BAD: Inconsistent, unclear
Table Users {
  ID bigint [pk]           // Inconsistent casing
  e varchar                // Too short
  dt timestamp             // Cryptic abbreviation
}
```

**Rules:**
- Table names: `singular` (user, not users)
- Column names: `lowercase_with_underscores`
- Primary keys: `table_name_id` (user_id, product_id)
- Timestamps: `created_at`, `updated_at`, `deleted_at`
- Booleans: `is_active`, `has_permission`

### **2. Always Use Primary Keys**

```dbml
// ✅ GOOD
Table products {
  product_id bigint [pk, increment]
  name varchar
}

// ❌ BAD: No primary key!
Table products {
  name varchar
  price decimal
}
```

### **3. Foreign Keys for Relationships**

```dbml
// ✅ GOOD: Explicit foreign key
Table orders {
  order_id bigint [pk]
  customer_id bigint [not null]  // Foreign key
}
Ref: orders.customer_id > customers.customer_id

// ❌ BAD: No relationship defined
Table orders {
  order_id bigint [pk]
  customer_id bigint  // What does this reference?
}
```

### **4. Use Appropriate Data Types**

```dbml
Table products {
  // ✅ GOOD
  price decimal(10,2)           // Exact for money
  stock_quantity int            // Whole numbers
  description text              // Long text
  sku char(12)                  // Fixed length
  
  // ❌ BAD
  price float                   // Rounding errors!
  stock_quantity varchar        // Should be number
  description varchar(50)       // Too short
  sku varchar(255)              // Wastes space
}
```

### **5. Add Indexes for Performance**

```dbml
Table users {
  user_id bigint [pk]
  email varchar [unique]
  first_name varchar
  last_name varchar
  created_at timestamp
  
  Indexes {
    email [unique]                    // Fast lookups
    (first_name, last_name)           // Search by name
    created_at                        // Sort by date
  }
}
```

**When to Index:**
- Primary keys (automatic)
- Foreign keys
- Columns used in WHERE clauses
- Columns used in ORDER BY
- Columns used in JOINs

### **6. Use Timestamps**

```dbml
Table products {
  product_id bigint [pk]
  name varchar
  created_at timestamp [default: `now()`]
  updated_at timestamp [default: `now()`]
  
  Note: 'Track when records are created and modified'
}
```

### **7. Soft Deletes**

```dbml
Table users {
  user_id bigint [pk]
  email varchar
  is_deleted boolean [default: false]
  deleted_at timestamp [null]
  
  Note: 'Use soft deletes for data recovery'
}
```

---

## 🔄 Complete Example: Blog Platform

```dbml
// Users
Table users {
  user_id bigint [pk, increment]
  username varchar(50) [unique, not null]
  email varchar(255) [unique, not null]
  password_hash char(64) [not null]
  is_active boolean [default: true]
  created_at timestamp [default: `now()`]
  
  Indexes {
    username [unique]
    email [unique]
  }
}

// Posts
Table posts {
  post_id bigint [pk, increment]
  user_id bigint [not null]
  title varchar(255) [not null]
  content text [not null]
  slug varchar(255) [unique, not null]
  status varchar(20) [default: 'draft'] // 'draft', 'published'
  view_count int [default: 0]
  created_at timestamp [default: `now()`]
  updated_at timestamp [default: `now()`]
  published_at timestamp [null]
  
  Indexes {
    slug [unique]
    (user_id, created_at)
    status
  }
}

// Comments
Table comments {
  comment_id bigint [pk, increment]
  post_id bigint [not null]
  user_id bigint [not null]
  content text [not null]
  is_approved boolean [default: false]
  created_at timestamp [default: `now()`]
  
  Indexes {
    (post_id, created_at)
  }
}

// Tags
Table tags {
  tag_id int [pk, increment]
  tag_name varchar(50) [unique, not null]
}

// Post-Tag Junction (Many-to-Many)
Table post_tags {
  post_id bigint [not null]
  tag_id int [not null]
  
  Indexes {
    (post_id, tag_id) [pk]
  }
}

// Relationships
Ref: posts.user_id > users.user_id
Ref: comments.post_id > posts.post_id
Ref: comments.user_id > users.user_id
Ref: post_tags.post_id > posts.post_id
Ref: post_tags.tag_id > tags.tag_id
```

---

## 🛠️ Tools to Use DBML

### **1. dbdiagram.io** (Recommended!)
- Paste DBML code
- Get instant visual diagram
- Export to SQL, PDF, PNG

### **2. VS Code Extension**
- Install "DBML Language" extension
- Syntax highlighting
- Auto-completion

### **3. CLI Tools**
```bash
npm install -g @dbml/cli

# Convert DBML to SQL
dbml2sql schema.dbml --mysql > schema.sql

# Convert SQL to DBML
sql2dbml schema.sql --mysql > schema.dbml
```

---

## 📚 Quick Reference

### **Table Definition**
```dbml
Table table_name {
  column_name data_type [attributes]
}
```

### **Attributes**
- `[pk]` - Primary key
- `[increment]` - Auto-increment
- `[unique]` - Unique constraint
- `[not null]` - Required field
- `[default: value]` - Default value

### **Relationships**
```dbml
Ref: table1.column > table2.column  // One-to-Many
Ref: table1.column - table2.column  // One-to-One
```

### **Indexes**
```dbml
Indexes {
  column_name [unique]
  (col1, col2) [name: 'idx_name']
}
```

---

## 💡 Key Takeaways

1. **DBML is for planning** - Design before coding
2. **Use clear names** - Future you will thank you
3. **Always define relationships** - Foreign keys are crucial
4. **Index wisely** - Speed up queries, but don't overdo it
5. **Use appropriate types** - DECIMAL for money, BIGINT for IDs
6. **Add timestamps** - Track when things happen
7. **Document with notes** - Explain complex logic

---

**Try it yourself at [dbdiagram.io](https://dbdiagram.io)!**
