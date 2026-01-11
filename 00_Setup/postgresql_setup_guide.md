# PostgreSQL & pgAdmin Setup Guide

## 🎯 First Time Setup

### Step 1: Launch pgAdmin
1. Open **pgAdmin 4** from Start Menu
2. It will open in your web browser
3. **Set a master password** when prompted (this is just for pgAdmin, not your database)
   - Example: `admin123` (just for practice)

---

### Step 2: Connect to PostgreSQL Server

1. In the left sidebar, look for **"Servers"**
2. Expand it by clicking the arrow
3. You should see **"PostgreSQL 17"** (or your version)
4. **Right-click** on it → **Connect Server**
5. Enter the password you set during PostgreSQL installation
   - If you don't remember, it's usually what you entered during install

---

### Step 3: Create Your Practice Database

1. Right-click **"Databases"** under your server
2. Select **Create → Database**
3. Name it: `practice_db`
4. Click **Save**

---

## 🚀 Running Your First Query

### Method 1: Query Tool (Recommended)

1. Right-click on **`practice_db`**
2. Select **Query Tool**
3. A new tab opens with a SQL editor
4. Paste your SQL code
5. Click the **▶ Execute** button (or press F5)

### Method 2: SQL Editor

1. Click **Tools** → **Query Tool** in the top menu
2. Make sure `practice_db` is selected in the dropdown
3. Write your queries!

---

## 📊 Loading Practice Databases

### Option 1: Copy-Paste Method (Easiest)

1. Open Query Tool on `practice_db`
2. Copy the entire contents of a setup file (e.g., `subquery_database_setup_postgres.sql`)
3. Paste into Query Tool
4. Click **Execute** (▶ button)
5. Check the **Messages** tab at bottom for success/errors

### Option 2: Run SQL File

1. Click **Tools** → **PSQL Tool**
2. Type: `\i 'C:/Users/ksank/training/02_Core_Skills/Subqueries/subquery_database_setup_postgres.sql'`
3. Press Enter

---

## 🔍 Viewing Your Data

### See All Tables
1. In left sidebar: **Databases → practice_db → Schemas → public → Tables**
2. Right-click a table → **View/Edit Data → All Rows**

### Quick Query
```sql
-- See all tables
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public';

-- Count rows in a table
SELECT COUNT(*) FROM customers;

-- View sample data
SELECT * FROM customers LIMIT 5;
```

---

## 💡 Useful pgAdmin Features

### Auto-Complete
- Start typing and press **Ctrl+Space** for suggestions
- Super helpful for table/column names!

### Format SQL
- Select your query
- Press **Shift+Ctrl+K** to auto-format
- Makes messy queries readable

### Explain Query
- Highlight your query
- Click **Explain** button (or F7)
- See how PostgreSQL executes it (like EXPLAIN in SQLite)

### Save Queries
- Click **File → Save** in Query Tool
- Save your practice queries for later!

---

## 🎨 Customize pgAdmin

### Dark Mode
1. **File → Preferences**
2. **Miscellaneous → Themes**
3. Select **"Dark"**
4. Restart pgAdmin

### Font Size
1. **File → Preferences**
2. **Query Tool → Display**
3. Adjust **Font Size**

---

## 🐛 Troubleshooting

### Can't Connect to Server
**Error:** "Could not connect to server"

**Fix:**
1. Make sure PostgreSQL service is running
   - Windows: Press **Win+R**, type `services.msc`
   - Find **"postgresql-x64-17"** (or your version)
   - Right-click → **Start** if it's stopped

### Wrong Password
**Error:** "password authentication failed"

**Fix:**
1. You need to reset the postgres user password
2. Open Command Prompt as Administrator
3. Type: `psql -U postgres`
4. If that doesn't work, you may need to reinstall PostgreSQL

### Port Already in Use
**Error:** "Port 5432 is already in use"

**Fix:**
- Another PostgreSQL instance is running
- Or another app is using port 5432
- Check Task Manager for postgres.exe processes

---

## 📚 Quick Reference

### Common Keyboard Shortcuts
| Action | Shortcut |
|--------|----------|
| Execute Query | **F5** |
| Execute Selection | **F5** (with text selected) |
| Auto-complete | **Ctrl+Space** |
| Format SQL | **Shift+Ctrl+K** |
| Comment Line | **Ctrl+/** |
| Save Query | **Ctrl+S** |

### PostgreSQL vs SQLite Syntax

| Feature | SQLite | PostgreSQL |
|---------|--------|------------|
| **Extract Year** | `strftime('%Y', date)` | `EXTRACT(YEAR FROM date)` or `DATE_PART('year', date)` |
| **Current Date** | `date('now')` | `CURRENT_DATE` |
| **String Concat** | `'a' || 'b'` | `'a' || 'b'` or `CONCAT('a', 'b')` |
| **Limit** | `LIMIT 10` | `LIMIT 10` |
| **Auto-increment** | `INTEGER PRIMARY KEY` | `SERIAL PRIMARY KEY` |

---

## ✅ You're Ready!

Once PostgreSQL finishes installing:
1. Open pgAdmin
2. Connect to your server
3. Create `practice_db`
4. Load your practice databases
5. Start querying!

**All your SQL knowledge transfers perfectly - just a few syntax tweaks!** 🚀
