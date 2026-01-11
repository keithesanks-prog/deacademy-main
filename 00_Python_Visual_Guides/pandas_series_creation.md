# 🐼 Pandas Series Creation - Complete Guide

## 📋 Objective
By the end of this lesson, you will understand:
- What a Pandas Series is
- How to create a Series from different data structures
- The properties of a Series

---

## 🎯 What is a Series?

A **Series** in Pandas is a **one-dimensional labeled array** that can hold data of any type, such as:
- Integers
- Floats
- Strings
- Python objects

### Each element in a Series has:
- **Value** – The actual data element
- **Index** – The label associated with the element

A Series is similar to a list or a one-dimensional array but with an additional feature of **labeled indexing**.

---

## 📐 Syntax

```python
pd.Series(data, index=index)
```

- `data` – The data to store in the Series
- `index` – The labels for each data element (optional)

---

## 🔨 Creating a Series

### **1. From a List (Default Index)**

You can create a Series from a list without specifying an index:

```python
import pandas as pd

data = [10, 20, 30, 40]
series = pd.Series(data)
print(series)
```

**Output:**
```
0    10
1    20
2    30
3    40
dtype: int64
```

✅ The index is automatically assigned starting from 0.

---

### **2. From a List with Custom Index**

You can create a Series and define a custom index:

```python
data = [10, 20, 30, 40]
index = ['a', 'b', 'c', 'd']
series = pd.Series(data, index=index)
print(series)
```

**Output:**
```
a    10
b    20
c    30
d    40
dtype: int64
```

✅ The index is now defined as `['a', 'b', 'c', 'd']`.

---

### **3. From a Dictionary**

When creating a Series from a dictionary, **keys become the index**:

```python
data = {'Alice': 25, 'Bob': 30, 'Charlie': 35}
series = pd.Series(data)
print(series)
```

**Output:**
```
Alice      25
Bob        30
Charlie    35
dtype: int64
```

✅ The dictionary keys become the Series index.

---

### **4. From a Scalar Value**

A scalar value creates a Series with the **same value repeated** across the index:

```python
value = 5
index = ['a', 'b', 'c']
series = pd.Series(value, index=index)
print(series)
```

**Output:**
```
a    5
b    5
c    5
dtype: int64
```

✅ The scalar value `5` is repeated for each index label.

---

## 🔍 Accessing Series Properties

### **Key Properties:**

| Property | Description | Example |
|----------|-------------|---------|
| `series.index` | Returns the index of the Series | `Index(['a', 'b', 'c'])` |
| `series.values` | Returns the values as a NumPy array | `[5 5 5]` |
| `series.dtype` | Returns the data type of the Series | `int64` |
| `series.shape` | Returns the shape (number of elements) | `(3,)` |
| `series.size` | Returns the number of elements | `3` |

### **Example:**

```python
data = [10, 20, 30]
index = ['a', 'b', 'c']
series = pd.Series(data, index=index)

print("Index:", series.index)
print("Values:", series.values)
print("Data Type:", series.dtype)
print("Shape:", series.shape)
print("Size:", series.size)
```

**Output:**
```
Index: Index(['a', 'b', 'c'], dtype='object')
Values: [10 20 30]
Data Type: int64
Shape: (3,)
Size: 3
```

---

## 🏋️ Practice Exercises

### **Exercise 1: Create from a List**
Create a Pandas Series from the list `[100, 200, 300, 400]` and display it.

<details>
<summary>Click to see solution</summary>

```python
import pandas as pd

data = [100, 200, 300, 400]
series = pd.Series(data)
print(series)
```

**Output:**
```
0    100
1    200
2    300
3    400
dtype: int64
```

</details>

---

### **Exercise 2: Create from a Dictionary**
Create a Series using a dictionary with the following data:
- `'Math'` = 90
- `'Science'` = 85
- `'English'` = 88

<details>
<summary>Click to see solution</summary>

```python
import pandas as pd

grades = {'Math': 90, 'Science': 85, 'English': 88}
series = pd.Series(grades)
print(series)
```

**Output:**
```
Math       90
Science    85
English    88
dtype: int64
```

</details>

---

### **Exercise 3: Create from a Scalar**
Create a Series from a single scalar value of `10` with an index of `['a', 'b', 'c', 'd']`.

<details>
<summary>Click to see solution</summary>

```python
import pandas as pd

value = 10
index = ['a', 'b', 'c', 'd']
series = pd.Series(value, index=index)
print(series)
```

**Output:**
```
a    10
b    10
c    10
d    10
dtype: int64
```

</details>

---

## 🎨 Visual Comparison

```
List:           [10, 20, 30, 40]
                 ↓   ↓   ↓   ↓
Series:         0   1   2   3  (index)
                10  20  30  40 (values)

Dictionary:     {'a': 10, 'b': 20, 'c': 30}
                 ↓         ↓         ↓
Series:         a         b         c  (index)
                10        20        30 (values)
```

---

## 💡 Key Takeaways

1. ✅ A Series is a **one-dimensional labeled array**
2. ✅ You can create a Series from **lists, dictionaries, scalars, or arrays**
3. ✅ The **index** provides labels for each element
4. ✅ If no index is specified, it defaults to `0, 1, 2, ...`
5. ✅ Dictionary keys automatically become the index
6. ✅ Use `.index`, `.values`, `.dtype` to access properties

---

## 🚀 Next Steps

After mastering Series creation, you'll learn:
- Indexing and slicing Series
- Series operations (arithmetic, filtering)
- Combining multiple Series into DataFrames
- Advanced Series methods

---

## 📝 Quick Reference

```python
# Create from list
pd.Series([1, 2, 3])

# Create with custom index
pd.Series([1, 2, 3], index=['a', 'b', 'c'])

# Create from dictionary
pd.Series({'a': 1, 'b': 2, 'c': 3})

# Create from scalar
pd.Series(5, index=['a', 'b', 'c'])

# Access properties
series.index    # Get index
series.values   # Get values
series.dtype    # Get data type
```

---

Happy learning! 🐼
