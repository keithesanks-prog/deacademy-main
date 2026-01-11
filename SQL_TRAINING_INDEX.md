# 📚 SQL Training Master Index

**Your complete SQL learning system with cross-references**

---

## 🎯 How to Use This Index

**Symbols:**
- **[A]** = Core concept (start here)
- **→ [B]** = See also (related topic)
- **📊** = Has visual diagrams
- **🎧** = Has audio lesson

---

## 📖 Table of Contents

### **Foundation Concepts**
1. [A] SQL Basics & Syntax
2. [B] Data Flow & Execution Order 📊
3. [C] WHERE vs HAVING
4. [D] Problem-Solving Methods

### **Core Skills**
5. [E] JOINs & Self Joins 📊 🎧
6. [F] Subqueries 🎧
7. [G] Window Functions 📊 🎧
8. [H] Aggregations (GROUP BY, COUNT, SUM)

### **Advanced Topics**
9. [I] Date Arithmetic 🎧
10. [J] String Functions & Splitting 📊
11. [K] Math Functions (POWER, TRUNCATE, ROUND)
12. [L] Function Chains 📊

### **Practice & Application**
13. [M] Compound Interest Queries 📊
14. [N] Top N per Group Problems
15. [O] Real-World Examples (Nike, Tesla, Walmart) 📊

---

## 📋 Detailed Index

### **[A] SQL Basics & Syntax**
**Files:**
- `sql training.md` (Lines 1-425)
- `sql_limit_guide.md`
- `sql_not_operator_guide.md` 🎧
- `sql_in_having_guide.md`

**Cross-References:**
- → [B] for execution order
- → [D] for problem-solving
- → [H] for aggregations

---

### **[B] Data Flow & Execution Order** 📊
**Files:**
- `sql_data_flow_guide.md` (Main reference)
- `sql_visual_transformations.md` (Visual diagrams)

**Key Concept:** FROM → WHERE → GROUP BY → HAVING → SELECT → ORDER BY

**Cross-References:**
- → [A] for basic syntax
- → [C] for WHERE vs HAVING
- → [H] for GROUP BY details

---

### **[C] WHERE vs HAVING**
**Files:**
- `having_explained_guide.md` 🎧
- `where_vs_having_examples_guide.md` 🎧
- `sql_data_flow_guide.md` (Section: WHERE vs HAVING)

**Key Concept:** WHERE filters rows, HAVING filters groups

**Cross-References:**
- → [B] for execution order
- → [H] for GROUP BY context

---

### **[D] Problem-Solving Methods**
**Files:**
- `problem_parsing_guide.md` 🎧 (3-Step Method)
- `one_step_at_a_time_guide.md` 🎧 (Drill)
- `how_to_break_down_sql_problems.md` (5-Question Framework)
- `breaking_down_problems_visual_transforms.md` 📊

**Key Concept:** Entity → Filters → Aggregates

**Cross-References:**
- → [A] for syntax
- → [B] for execution flow
- → [O] for real examples

---

### **[E] JOINs & Self Joins** 📊 🎧
**Files:**
- `self_joins_guide.md` 🎧
- `self_join_pairs_guide.md` 🎧
- `self_join_visual_walkthrough.md` 📊 (Employee-Manager example)

**Key Concept:** Self-referencing tables (manager_id → employee_id)

**Cross-References:**
- → [A] for JOIN syntax
- → [O] for real examples

---

### **[F] Subqueries** 🎧
**Files:**
- `subqueries_guide.md` 🎧
- `sql_problem_solving_worksheet.md` (Exercises 1-3)

**Key Concept:** Single Row, Multiple Row, Correlated, EXISTS

**Cross-References:**
- → [C] for HAVING vs subqueries
- → [N] for Top N problems

---

### **[G] Window Functions** 📊 🎧
**Files:**
- `window_functions_guide.md` 🎧 (Complete reference)
- `window_functions_walkthrough.md` 📊 (YouTuber example)

**Key Concept:** RANK() OVER (PARTITION BY ... ORDER BY ...)

**Cross-References:**
- → [N] for Top N per group
- → [O] for Tesla/YouTuber examples

---

### **[H] Aggregations (GROUP BY, COUNT, SUM)**
**Files:**
- `sql_data_flow_guide.md` (GROUP BY section)
- `nike_query_breakdown.md` 🎧 📊

**Key Concept:** Collapsing rows into groups

**Cross-References:**
- → [B] for execution order
- → [C] for HAVING clause
- → [D] for problem-solving

---

### **[I] Date Arithmetic** 🎧
**Files:**
- `date_arithmetic_guide.md` 🎧 (MySQL vs SQL Server vs PostgreSQL)
- `sql_datetime_practice_setup.sql` (Practice tables)
- `sql_datetime_exercises.md` (14 exercises)

**Key Concept:** DATE_ADD, DATEADD, DATEDIFF, EXTRACT

**Cross-References:**
- → [K] for EXTRACT function
- → [M] for compound interest (uses dates)

---

### **[J] String Functions & Splitting** 📊
**Files:**
- `sql_string_splitting_guide.md` (Multiple delimiters)
- `string_splitting_visual_guide.md` 📊 (Character-by-character)
- `sql_string_splitting_visual.md` 📊 (SUBSTRING_INDEX)
- `sql_string_functions_exercises.md` (13 exercises)

**Key Concept:** SUBSTRING_INDEX, SPLIT_PART, CONCAT

**Cross-References:**
- → [K] for CONCAT
- → [L] for nested functions

---

### **[K] Math Functions (POWER, TRUNCATE, ROUND)**
**Files:**
- `sql_math_functions_reference.md` (Quick reference)
- `sql_function_chains_visual.md` 📊 (Nested examples)

**Key Concept:** POWER(base, exponent), TRUNCATE vs ROUND

**Cross-References:**
- → [L] for function chains
- → [M] for compound interest (uses POWER)

---

### **[L] Function Chains** 📊
**Files:**
- `sql_function_chains_visual.md` 📊 (Inside-out execution)
- `sql_function_chains_practice.md` (Practice problems)

**Key Concept:** Read from inside out (nested functions)

**Cross-References:**
- → [K] for individual functions
- → [M] for real examples

---

### **[M] Compound Interest Queries** 📊
**Files:**
- `compound_interest_query_guide.md` 🎧 (8-step walkthrough)
- `compound_interest_visual_breakdown.md` 📊 (Data transformations)

**Key Concept:** POWER(1 + rate/100, months)

**Cross-References:**
- → [K] for POWER function
- → [L] for function chains
- → [O] for Tesla example

---

### **[N] Top N per Group Problems**
**Files:**
- `window_functions_guide.md` (Use Case 1)
- `window_functions_walkthrough.md` 📊 (YouTuber example)
- `walmart_restock_visual_walkthrough.md` 📊 (HAVING vs Subquery)

**Key Concept:** ROW_NUMBER() OVER (PARTITION BY ... ORDER BY ...)

**Cross-References:**
- → [G] for window functions
- → [F] for subquery approach
- → [C] for HAVING approach

---

### **[O] Real-World Examples** 📊
**Files:**
- `nike_query_breakdown.md` 🎧 📊 (Products analysis)
- `compound_interest_visual_breakdown.md` 📊 (Tesla pricing)
- `walmart_restock_visual_walkthrough.md` 📊 (Inventory restocks)
- `airbnb_second_booking_explained.md` 📊 (ROW_NUMBER example)

**Cross-References:**
- → [D] for problem-solving approach
- → [G] for window functions (Airbnb)
- → [M] for compound interest (Tesla)

---

## 🎧 Audio Lessons Quick Reference

| Lesson                   | File                              | Topic              |
|--------------------------|--------------------------------   |----------------    |
| NOT Operator             | `not_operator.md`                 | Filtering with NOT |
| LIMIT & OFFSET           | `limit_offset.md`                 | Pagination         |
| WHERE vs HAVING          | `where_vs_having.md`              | [C]                |
| Nike Query               | `nike_query_breakdown.md`         | [O]                |
| Self Joins               | `self_joins.md`                   | [E]                |
| Self Join Pairs          | `self_join_pairs.md`              | [E]                |
| Self Join Visual         | `self_join_visual_walkthrough.md` | [E]                |
| Subqueries               | `subqueries.md`                   | [F]                |
| Breaking Down Problems   | `breaking_down_problems.md`       | [D]                |
| Visual Transforms        | `visual_transforms.md`            | [D]                |
| HAVING Explained         | `having_explained.md`             | [C]                |
| WHERE vs HAVING Examples | `where_vs_having_examples.md`     | [C]                |
| Problem Parsing Method   | `problem_parsing_method.md`       | [D]                |
| One Step at a Time       | `one_step_at_a_time.md`           | [D]                |
| Date Arithmetic          | `date_arithmetic.md`              | [I]                |
| Window Functions         | `window_functions.md`             | [G]                |
| Compound Interest        | `compound_interest_query.md`      | [M]                |

**To play:** `python play_lesson.py <lesson_name>`

---

## 🎯 Learning Paths

### **Path 1: Complete Beginner**
1. [A] SQL Basics
2. [B] Data Flow
3. [D] Problem-Solving Methods
4. [H] Aggregations
5. [C] WHERE vs HAVING

### **Path 2: Interview Prep**
1. [D] Problem-Solving Methods
2. [E] JOINs & Self Joins
3. [F] Subqueries
4. [G] Window Functions
5. [N] Top N per Group

### **Path 3: Data Engineering Focus**
1. [B] Data Flow & Execution
2. [L] Function Chains
3. [I] Date Arithmetic
4. [J] String Functions
5. [M] Compound Interest (complex transformations)
