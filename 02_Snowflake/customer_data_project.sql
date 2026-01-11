/*
=============================================================================
SNOWFLAKE JSON PROJECT: CUSTOMER DATA ANALYSIS
=============================================================================
This script sets up a complete environment to ingest, flatten, and analyze
semi-structured JSON data (customer_data.json).

OBJECTIVES:
1. Setup Database and Schemas (RAW_DATA, FLATTEN_DATA)
2. Create RAW Table (VARIANT) and Stage
3. Load Data from Stage
4. Flatten Data into Structured Table
5. Create a Dynamic View
6. Perform Advanced Analysis
=============================================================================
*/

-----------------------------------------------------------------------------
-- STEP 1: ENVIRONMENT SETUP
-----------------------------------------------------------------------------
-- Create the main database
CREATE DATABASE IF NOT EXISTS CUSTOMER_DATA;

USE DATABASE CUSTOMER_DATA;

-- Create Schemas
CREATE SCHEMA IF NOT EXISTS RAW_DATA;

CREATE SCHEMA IF NOT EXISTS FLATTEN_DATA;

-----------------------------------------------------------------------------
-- STEP 2: CREATE RAW TABLE & STAGE
-----------------------------------------------------------------------------
USE SCHEMA RAW_DATA;

-- Create the table to hold the raw JSON file
-- We use VARIANT data type to store semi-structured data
CREATE OR REPLACE TABLE CUSTOMER_RAW (JSON_DATA VARIANT);

-- Create an internal stage to upload the file
CREATE OR REPLACE STAGE CUSTOMER_STAGE;

-- -----------------------------------------------------
-- ACTION REQUIRED:
-- Upload 'customer_data.json' to CUSTOMER_STAGE now.
-- You can use Snowsight UI -> Internal Stages -> Upload
-- -----------------------------------------------------

-- Verify the file is staged
LIST @CUSTOMER_STAGE;

-----------------------------------------------------------------------------
-- STEP 3: LOAD DATA (COPY INTO)
-----------------------------------------------------------------------------
-- Copy the JSON data into the raw table.
-- STRIP_OUTER_ARRAY = FALSE because we want to use LATERAL FLATTEN on the specific array structure.
-- FILE_FORMAT = (TYPE = 'JSON') tells Snowflake how to parse it.

COPY INTO CUSTOMER_RAW
FROM @CUSTOMER_STAGE/customer_data.json
FILE_FORMAT = (TYPE = 'JSON' STRIP_OUTER_ARRAY = FALSE);

-- Verify raw data load
SELECT * FROM CUSTOMER_RAW LIMIT 1;

-----------------------------------------------------------------------------
-- STEP 4: FLATTEN DATA TO STRUCTURED TABLE
-----------------------------------------------------------------------------
-- Create the target table for flattened data
USE SCHEMA FLATTEN_DATA;

CREATE
OR
REPLACE
TABLE CUSTOMER_FLATTEN (
    CUSTOMERID INT,
    NAME STRING,
    EMAIL STRING,
    REGION STRING,
    COUNTRY STRING,
    PRODUCTNAME STRING,
    PRODUCTBRAND STRING,
    CATEGORY STRING,
    QUANTITY INT,
    PRICEPERUNIT FLOAT,
    TOTALSALES FLOAT,
    PURCHASEMODE STRING,
    MODEOFPAYMENT STRING,
    PURCHASEDATE DATE
);

-- Insert data by flattening the JSON array
-- LATERAL FLATTEN explodes the array so we can access individual objects as 'value'
INSERT INTO CUSTOMER_FLATTEN
SELECT 
    value:customerid::INT,
    value:name::STRING,
    value:email::STRING,
    value:region::STRING,
    value:country::STRING,
    value:productname::STRING,
    value:productbrand::STRING,
    value:category::STRING,
    value:quantity::INT,
    value:priceperunit::FLOAT,
    value:totalsales::FLOAT,
    value:purchasemode::STRING,
    value:modeofpayment::STRING,
    value:purchasedate::DATE
FROM CUSTOMER_DATA.RAW_DATA.CUSTOMER_RAW,
LATERAL FLATTEN(input => json_data);

-- Verify flattened data
SELECT * FROM CUSTOMER_FLATTEN LIMIT 10;

-----------------------------------------------------------------------------
-- STEP 5: CREATE EXPLODING VIEW (DYNAMIC ANALYSIS)
-----------------------------------------------------------------------------
-- Often you don't want to move data, just explore it.
-- This View provides a real-time window into the JSON without creating a new table.

USE SCHEMA RAW_DATA;

CREATE OR REPLACE VIEW CUSTOMER_DATA_VIEW AS
SELECT 
    value:customerid::INT as ID,
    value:name::STRING as CUSTOMER_NAME,
    value:email::STRING as EMAIL,
    value:totalsales::FLOAT as SALES,
    value:purchasedate::DATE as PURCHASE_DATE
FROM RAW_CUSTOMER_JSON, -- NOTE: Ensure this matches your Raw Table Name (CUSTOMER_RAW)
LATERAL FLATTEN(input => json_data);

-- Run a search on the View
SELECT * FROM CUSTOMER_DATA_VIEW WHERE SALES > 1000;

-----------------------------------------------------------------------------
-- STEP 6: DATA ANALYSIS
-----------------------------------------------------------------------------
USE SCHEMA FLATTEN_DATA;

-- Q1: Total sales for each region
SELECT REGION, SUM(TOTALSALES) as TOTAL_REGION_SALES
FROM CUSTOMER_FLATTEN
GROUP BY
    REGION
ORDER BY TOTAL_REGION_SALES DESC;

-- Q2: Region with the highest total sales
SELECT
    TOP 1 REGION,
    SUM(TOTALSALES) as TOTAL_REGION_SALES
FROM CUSTOMER_FLATTEN
GROUP BY
    REGION
ORDER BY TOTAL_REGION_SALES DESC;

-- Q3: Total quantity sold for each product brand
SELECT PRODUCTBRAND, SUM(QUANTITY) as TOTAL_QTY
FROM CUSTOMER_FLATTEN
GROUP BY
    PRODUCTBRAND
ORDER BY TOTAL_QTY DESC;

-- Q4: Product with the least quantity sold
-- (Aggregating by Product Name)
SELECT TOP 1 PRODUCTNAME, SUM(QUANTITY) as TOTAL_QTY
FROM CUSTOMER_FLATTEN
GROUP BY
    PRODUCTNAME
ORDER BY TOTAL_QTY ASC;

-- Q5: Customer who made the highest purchase (Single Transaction)
SELECT NAME, TOTALSALES
FROM CUSTOMER_FLATTEN
ORDER BY TOTALSALES DESC
LIMIT 1;

-- Q6: Product Name and Brand with the lowest unit price
SELECT
    TOP 1 PRODUCTNAME,
    PRODUCTBRAND,
    PRICEPERUNIT
FROM CUSTOMER_FLATTEN
ORDER BY PRICEPERUNIT ASC;

-- Q7: Top 5 best-selling products (By Sales Revenue)
SELECT
    TOP 5 PRODUCTNAME,
    SUM(TOTALSALES) as TOTAL_REVENUE
FROM CUSTOMER_FLATTEN
GROUP BY
    PRODUCTNAME
ORDER BY TOTAL_REVENUE DESC;