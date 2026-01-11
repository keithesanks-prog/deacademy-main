# 🎧 SQL Self Joins - Audio Lesson Companion

**This guide matches the audio lesson script. Follow along as you listen!**

---

## 🧩 The Concept: Joining a Table to Itself

**Why?** Hierarchical data (e.g., Employees & Managers).
**The Trick:** Pretend you have **TWO copies** of the same table.

---

## 📊 The Scenario

Imagine an `Employees` table:

| Employee_ID | Name | Manager_ID |
|-------------|------|------------|
| 101 | **Alice** | NULL |
| 102 | **Bob** | 101 |
| 103 | **Charlie** | 102 |

- **Bob's** Manager_ID is **101**.
- **101** is **Alice**.
- So, **Alice** is **Bob's** manager.

To get "Bob" and "Alice" in the same row, we join the table to itself.

---

## 🔨 The "Two Copies" Trick

We give the table two different **Aliases** (Nicknames):

1.  **Copy 1 (E):** Represents the **Employee**
2.  **Copy 2 (M):** Represents the **Manager**

### **The Query:**

```sql
SELECT 
    E.Name AS Employee_Name, 
    M.Name AS Manager_Name
FROM Employees E        -- Copy 1 (Employee)
JOIN Employees M        -- Copy 2 (Manager)
  ON E.Manager_ID = M.Employee_ID;
```

**The Logic:**
> "Take the **Manager ID** from the Employee's row (E), and find the matching **Employee ID** in the Manager's copy (M)."

---

## 🔗 Adding a Third Table

What if we also want the **Department Name**?

**New Table:** `Departments`
| Dept_ID | Dept_Name |
|---------|-----------|
| 1 | Sales |
| 2 | HR |

**The Query:**

```sql
SELECT 
    E.Name AS Employee, 
    M.Name AS Manager,
    D.Dept_Name
FROM Employees E
JOIN Employees M 
  ON E.Manager_ID = M.Employee_ID  -- Join 1: Self Join
JOIN Departments D 
  ON E.Dept_ID = D.Dept_ID;        -- Join 2: Standard Join
```

---

## 📝 Recipe for Self Joins

1.  **FROM/JOIN**: Use the same table twice.
2.  **Aliases**: Give them distinct names (e.g., `E` and `M`).
3.  **ON Clause**: Match the **Foreign Key** (Manager_ID) to the **Primary Key** (Employee_ID).

---

## 🚀 Visualizing the Join

```mermaid
graph LR
    subgraph "Employees Table (E)"
    E_Bob[Bob (Mgr: 101)]
    end

    subgraph "Employees Table (M)"
    M_Alice[Alice (ID: 101)]
    end

    E_Bob -- "E.Manager_ID = M.Employee_ID" --> M_Alice
```
