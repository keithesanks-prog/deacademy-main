# 📊 Snowflake JSON Project Guide: Customer Data Analysis

This guide walks you through the end-to-end process of ingesting, flattening, and analyzing semi-structured JSON data (`customer_data.json`) in Snowflake.

## 📂 Project Structure

- **Database**: `CUSTOMER_DATA`
- **Schemas**:
    - `RAW_DATA`: For staging and storing the raw JSON.
    - `FLATTEN_DATA`: For the clean, structured table ready for analysis.

---

## 🚀 Phase 1: Environment & Staging

### 1. Create the Environment
Run the setup commands in the SQL script to create your Database and Schemas.

```sql
CREATE DATABASE IF NOT EXISTS CUSTOMER_DATA;
CREATE SCHEMA RAW_DATA;
CREATE SCHEMA FLATTEN_DATA;
```

### 2. Create the Raw Stage
We create a table (`CUSTOMER_RAW`) with a single column of type `VARIANT`. This is Snowflake's special data type for semi-structured data (JSON, Avro, Parquet).

```sql
CREATE OR REPLACE TABLE RAW_DATA.CUSTOMER_RAW (JSON_DATA VARIANT);
CREATE OR REPLACE STAGE RAW_DATA.CUSTOMER_STAGE;
```

### 3. Upload the File
**ACTION REQUIRED**: You must perform this step manually.
1.  Go to **Snowsight UI**.
2.  Navigate to **Data** -> **Databases** -> `CUSTOMER_DATA` -> `RAW_DATA` -> **Stages**.
3.  Select `CUSTOMER_STAGE`.
4.  Click **+ Files** (top right) and upload `customer_data.json`.

---

## 📥 Phase 2: Ingestion (Copy & Load)

We load the data from the Stage into the Raw Table.

```sql
COPY INTO RAW_DATA.CUSTOMER_RAW
FROM @RAW_DATA.CUSTOMER_STAGE/customer_data.json
FILE_FORMAT = (TYPE = 'JSON' STRIP_OUTER_ARRAY = FALSE);
```
> **Why `STRIP_OUTER_ARRAY = FALSE`?**
> Your JSON file is a large array `[...]`. By keeping it as `FALSE`, we load that entire array into a single row (or chunks). This allows us to use `LATERAL FLATTEN` effectively in the next step to "explode" that array into individual rows.

---

## 🔨 Phase 3: Flattening the Data

This is the magic step. We transform the messy JSON into a clean table.

### KEY CONCEPT: `LATERAL FLATTEN`
This function takes a VARIANT array and "explodes" it. For every item in the array, it creates a new row.
- **Input**: One row with a JSON array of 100 customers.
- **Output**: 100 rows, one for each customer.

```sql
SELECT 
    value:customerid::INT,     -- Extract 'customerid', cast to Integer
    value:name::STRING,        -- Extract 'name', cast to String
    ...
FROM RAW_DATA.CUSTOMER_RAW,
LATERAL FLATTEN(input => json_data);
```

We insert these results into `FLATTEN_DATA.CUSTOMER_FLATTEN`.

---

## 🔍 Phase 4: Dynamic Views

Sometimes you don't want to create a whole new table. You just want a "window" into the JSON.

```sql
CREATE OR REPLACE VIEW CUSTOMER_DATA_VIEW AS
SELECT 
    value:customerid::INT as ID,
    value:totalsales::FLOAT as SALES
FROM RAW_DATA.CUSTOMER_RAW,
LATERAL FLATTEN(input => json_data);
```
Now you can run simple SQL like `SELECT * FROM CUSTOMER_DATA_VIEW WHERE SALES > 1000` and Snowflake handles the JSON parsing on the fly!

---

## 📈 Phase 5: Analysis

Now that the data is structured, standard SQL works perfectly.

**Example: Top Selling Region**
```sql
SELECT TOP 1 REGION, SUM(TOTALSALES) 
FROM FLATTEN_DATA.CUSTOMER_FLATTEN 
GROUP BY REGION 
ORDER BY 2 DESC;
```

Refer to the `customer_data_project.sql` file for all 7 analysis queries needed for your project.
