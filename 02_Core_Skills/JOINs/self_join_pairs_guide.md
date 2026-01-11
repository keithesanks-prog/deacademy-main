# 🎧 Self Join Pairs: Code Walkthrough

**This guide matches the audio lesson script. Follow along as you listen!**

---

## 📝 The Code Snippet

```sql
SELECT
    e1.employee_id AS employee1_id,
    e1.first_name AS employee1_name,
    e2.employee_id AS employee2_id,
    e2.first_name AS employee2_name,
    e1.manager_id
FROM
    employees e1
JOIN
    employees e2
    ON e1.manager_id = e2.manager_id
    AND e1.employee_id < e2.employee_id -- avoids duplicates
WHERE
    e1.manager_id IS NOT NULL; -- filters out employees with no managers
```

---

## 🔍 Line-by-Line Breakdown

### **1. The SELECT Clause (Lines 1-6)**
We select columns from both "copies" of the table.
- `e1.first_name`: Name of the **First** Employee.
- `e2.first_name`: Name of the **Second** Employee.
- `e1.manager_id`: The Manager they share.

### **2. The FROM & JOIN (Lines 7-10)**
We create two aliases (nicknames):
- `employees e1`: The "First Employee" Table.
- `employees e2`: The "Second Employee" Table.

### **3. The ON Clause (Lines 12-13)**
`ON e1.manager_id = e2.manager_id`
- This is the bridge. It connects two rows that have the **same boss**.

### **4. The Duplicate Filter (Line 14)**
`AND e1.employee_id < e2.employee_id`
- **Why?** To avoid matching "John & John" (Self-match) and "Mike & John" (Duplicate pair).
- It forces a specific order: Small ID first, Big ID second.

### **5. The Null Filter (Line 15)**
`WHERE e1.manager_id IS NOT NULL`
- **Why?** The CEO usually has `NULL` as a manager.
- We don't want to match people just because they both have "No Manager".
- This ensures we only look at actual reporting lines.

---

## 🚀 Visualizing the Logic

**Manager (ID: 3)**
   /   \
**John (1)**   **Chris (5)**

1.  **e1 (John)** looks at Manager 3.
2.  **e2 (Chris)** looks at Manager 3.
3.  **Match!** They share Manager 3.
4.  **Check IDs:** 1 < 5? **Yes**.
5.  **Check Null:** Is Manager 3 NULL? **No**.
6.  **Result:** "John & Chris"
