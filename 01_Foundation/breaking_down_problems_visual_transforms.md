# 🔄 SQL Data Transforms: Visualizing the Flow

**Problem:** "Find customers with **Total Orders** > **Global Average**."

---

## 📊 1. The Raw Data (Starting Point)

**Table: Orders**
| Order_ID  | Customer   | Amount |
|---------- |----------  |--------|
| 1         | **Alice**  | $100   |
| 2         | **Alice**  | $200   |
| 3         | **Bob**    | $900   |
| 4         | **Charlie**| $300   |
| 5         | **Charlie**| $100   |

---

## 📉 2. Step 1: The Benchmark (Subquery)

**Query:** `SELECT AVG(amount) FROM orders`

**Calculation:**
$(100 + 200 + 900 + 300 + 100) / 5 = 1600 / 5 = 320$

**Result (The Benchmark):**
| Global_Average |
|----------------|
| **$320**       |

---

## 📦 3. Step 2: The Grouping (Intermediate Table)

**Query:** `SELECT Customer, SUM(amount) FROM orders GROUP BY Customer`

**Transformation:**
- **Alice**: $100 + $200 = **$300**
- **Bob**: $900 = **$900**
- **Charlie**: $300 + $100 = **$400**

**Result (The Groups):**
| Customer   | Total_Amount |
|----------  |--------------|
| Alice      | $300         |
| Bob        | $900         |
| Charlie    | $400         |

---

## 🔍 4. Step 3: The Filter (HAVING)

**Query:** `HAVING Total_Amount > 320`

**Comparison:**
- **Alice**: $300 > $320? ❌ **NO** (Drop)
- **Bob**: $900 > $320? ✅ **YES** (Keep)
- **Charlie**: $400 > $320? ✅ **YES** (Keep)

---

## ✅ 5. Final Result

**Query:** `SELECT Customer FROM ...`

| Customer   |
|----------  |
| **Bob**    |
| **Charlie**|

---

## 🧠 Summary of Transforms

1.  **Collapse** all orders into one single number ($320).
2.  **Collapse** orders by customer into totals ($300, $900, $400).
3.  **Compare** the totals against the single number.
