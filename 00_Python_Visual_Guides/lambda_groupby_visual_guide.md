# Pandas GroupBy & Lambda - A Visual Guide 🧠

You mentioned feeling confused about **"functions that have no output"** and how the **lambda** logic works.

This guide visualizes exactly what happens "under the hood" when you run that complex line of code.

---

## 1. The "Invisible" GroupBy Object

When you run `fog_df.groupby('road_traffic')`, it doesn't print a table. Instead, it creates a special **GroupBy Object**.

Think of this as **splitting your DataFrame into separate boxes**, one for each traffic type.

```
ORIGINAL DATAFRAME (fog_df):
┌──────────┬──────────────┬─────────────────────┐
│ order_id │ road_traffic │ total_delivery_time │
│ ...      │ ...          │ ...                 │
└──────────┴──────────────┴─────────────────────┘
             ↓
    .groupby('road_traffic')
             ↓
THE "INVISIBLE" GROUPBY OBJECT:
┌───────────────────────────────┐
│  📦 BOX 1: "High"             │
│  Contains only High traffic   │
│  rows.                        │
└───────────────────────────────┘
┌───────────────────────────────┐
│  📦 BOX 2: "Medium"           │
│  Contains only Medium traffic │
│  rows.                        │
└───────────────────────────────┘
┌───────────────────────────────┐
│  📦 BOX 3: "Low"              │
│  Contains only Low traffic    │
│  rows.                        │
└───────────────────────────────┘
```
This object waits for instructions. It holds the data but doesn't show it until you apply a function.

---

## 2. The `.apply(lambda x: ...)` Step

The `.apply()` function is like a **worker** that visits every box.
The **lambda function** is the **instruction sheet** the worker carries.

In `lambda x: ...`, **`x` IS THE BOX**.
`x` is a temporary variable name for "the DataFrame inside the current box".

```
        Worker enters BOX 1 ("High")
             │
             ▼
    ┌───────────────────────────────┐
    │  x = this sub-dataframe       │
    │  ┌──────────┬────────┬──────┐ │
    │  │ order_id │ traffic│ time │ │
    │  ├──────────┼────────┼──────┤ │
    │  │ 1        │ High   │ 52   │ │ ← x["total_delivery_time"][0]
    │  │ 2        │ High   │ 30   │ │ ← x["total_delivery_time"][1]
    │  │ 3        │ High   │ 60   │ │ ← x["total_delivery_time"][2]
    │  └──────────┴────────┴──────┘ │
    └───────────────────────────────┘
             │
             │ performs the calculation...
             ▼
```

---

## 3. Breaking Down The Calculation

The math happens inside the box (on `x`):

`f'{(x["total_delivery_time"] > 45).sum() / len(x):.2%}'`

Let's zoom into the "High" box (3 orders: 52, 30, 60 mins):

### Step A: `x["total_delivery_time"] > 45`
Checks each row.
- 52 > 45? **True**
- 30 > 45? **False**
- 60 > 45? **True**
result: `[True, False, True]`

### Step B: `.sum()`
Counts the True values.
- `True + False + True` = **2**
*(This is the number of Late Orders)*

### Step C: `/ len(x)`
Divides by total rows in the box.
- `len(x)` is 3
- `2 / 3` = **0.666...**

### Step D: `:.2%` (Formatting)
Turns the number into a percentage string.
- `0.666...` → **"66.67%"**

---

## 4. Stitching It Back Together

The worker leaves each box with a generic result (the string). Pandas stitches these back into a Series.

```
┌──────────────┐    Worker Results:
│ "High" Box   │ →  "66.67%"
└──────────────┘

┌──────────────┐
│ "Medium" Box │ →  "50.00%"
└──────────────┘

┌──────────────┐
│ "Low" Box    │ →  "0.00%"
└──────────────┘

       ↓ stitches together ↓

Result Series (indexed by road_traffic):
road_traffic
High      66.67%
Medium    50.00%
Low        0.00%
dtype: object
```

---

## 5. `reset_index(name='percent_orders_late')`

The `apply` result has `road_traffic` as the **Index** (the labels on the left), not a regular column. `reset_index` fixes this.

**Before reset_index:**
```
              <no name>
road_traffic           
High          66.67%
Medium        50.00%
Low            0.00%
```

**After `reset_index(name='percent_orders_late')`:**
```
  road_traffic  percent_orders_late
0 High          66.67%
1 Medium        50.00%
2 Low            0.00%
```

Now it's a proper DataFrame you can read efficiently!
