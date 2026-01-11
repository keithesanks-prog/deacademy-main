# 🎧 SQL HAVING Clause - Audio Lesson Companion

**This guide matches the audio lesson script. Follow along as you listen!**

---

## 🚪 The Analogy: The Two Bouncers

To understand `WHERE` vs `HAVING`, imagine a nightclub.

### **Bouncer 1: WHERE (The Front Door)**
- **Location:** Front Entrance.
- **Job:** Checks **individuals** before they enter.
- **Rule:** "No Sneakers!"
- **SQL:** `WHERE shoe_type != 'Sneakers'`
- **Timing:** Happens **BEFORE** the party (grouping) starts.

### **Bouncer 2: HAVING (The VIP Section)**
- **Location:** Inside, at the VIP tables.
- **Job:** Checks **groups** (tables) after they are seated.
- **Rule:** "Your table must spend $500 to stay!"
- **SQL:** `HAVING SUM(tab) > 500`
- **Timing:** Happens **AFTER** the party (grouping) has started.

---

## 🛑 The Golden Rule

| Clause | Filters What? | Can use Aggregates? | Example |
|--------|---------------|---------------------|---------|
| **WHERE** | **Rows** (Individuals) | ❌ NO | `WHERE amount > 10` |
| **HAVING** | **Groups** (Tables) | ✅ YES | `HAVING SUM(amount) > 500` |

---

## ❌ Common Mistake

```sql
-- WRONG!
SELECT customer, SUM(amount)
FROM orders
WHERE SUM(amount) > 500  -- ERROR!
GROUP BY customer;
```

**Why?**
Bouncer 1 (`WHERE`) is at the front door. He can't see the "Total Sum" because the groups haven't formed yet!

---

## ✅ Correct Usage

```sql
-- CORRECT!
SELECT customer, SUM(amount)
FROM orders
GROUP BY customer        -- Groups form here
HAVING SUM(amount) > 500; -- Bouncer 2 checks the totals
```

---

## 🧠 Visual Flow

1.  **Raw Data** (Rows)
    ⬇️
2.  **WHERE** (Filter Rows) -> *Kicks out bad rows*
    ⬇️
3.  **GROUP BY** (Make Groups) -> *Bundles rows together*
    ⬇️
4.  **HAVING** (Filter Groups) -> *Kicks out bad groups*
    ⬇️
5.  **SELECT** (Show Results)
