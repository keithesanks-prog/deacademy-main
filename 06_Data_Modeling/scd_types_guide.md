# Slowly Changing Dimensions (SCD) - Quick Reference

## 🔄 The Problem
Dimension attributes change over time! How do we handle these changes?

## Three Types of SCD:

### ✅ Type 1: Overwrite (No History)
**Strategy:** Just UPDATE the value, lose history

**Example:** Customer moves from NYC to LA
```
Before:  customer_key: 123, city: 'New York'
After:   customer_key: 123, city: 'Los Angeles'  ← NYC history LOST!
```

**When to use:**
- Corrections (typos, data errors)
- Unimportant changes (email address)
- No need for historical analysis

**Pros:** ✅ Simple, no extra storage  
**Cons:** ❌ Lose history, can't analyze trends

---

### ⭐ Type 2: Add New Row (Keep Full History) - **RECOMMENDED**
**Strategy:** Create new row with new surrogate key, keep old row

**Example:** Product price changes from $999 to $899
```
Old version (closed):
product_key: 123, product_id: 'IPHONE15', price: $999,
effective_date: 2024-01-01, expiration_date: 2024-06-30, is_current: 0

New version (active):
product_key: 124, product_id: 'IPHONE15', price: $899,
effective_date: 2024-07-01, expiration_date: NULL, is_current: 1
```

**Required fields:**
- `effective_date` - When this version became active
- `expiration_date` - When this version ended (NULL = current)
- `is_current` - Boolean flag (1 = current, 0 = historical)

**When to use:**
- Price changes (need to analyze impact)
- Customer segment changes (VIP → Regular)
- Any change you need to track over time

**Pros:** ✅ Full history, accurate reporting, trend analysis  
**Cons:** ❌ More storage, more complex queries

**⭐ MOST COMMON: Use Type 2 for important attributes!**

---

### ❌ Type 3: Add Column (Limited History) - **AVOID**
**Strategy:** Add columns for previous value (e.g., current_city, previous_city)

**Example:** Customer moves from NYC to LA to Chicago
```
After 1st move:
customer_key: 123, current_city: 'Los Angeles', previous_city: 'New York'

After 2nd move:
customer_key: 123, current_city: 'Chicago', previous_city: 'Los Angeles'
← NYC history LOST!
```

**When to use:**
- Only need to track ONE previous value
- Very rare changes
- Simple before/after comparison

**Pros:** ✅ Simple queries, one row per entity  
**Cons:** ❌ Limited history (only 1 previous), inflexible

**⚠️ AVOID TYPE 3: Use Type 2 instead!**

**Why avoid?**
- Loses history after 2 changes
- Hard to extend (need schema changes)
- Type 2 is more flexible and complete

---

## 📊 Comparison Table

| Type | Strategy | History | Recommendation |
|------|----------|---------|----------------|
| Type 1 | Overwrite | None | Use for corrections |
| Type 2 | Add row | Full | ✅ **BEST - Use this!** |
| Type 3 | Add column | Limited (1 previous) | ❌ Avoid |

---

## 💡 Best Practice
- **Default to Type 2** for any attribute that might change and you care about history
- **Use Type 1** only for corrections or truly unimportant changes
- **Avoid Type 3** - it's inflexible and Type 2 does the job better
