# Data Modeling Interview Framework: Ask Questions Without Getting Lost 🎯

## The Problem
You know you should ask clarifying questions in interviews, but after 5 minutes of questions, you feel lost and don't know how to organize the information to design a solution.

## The Solution
Use this **structured framework** to ask questions in a logical order and **capture answers in a template** that directly maps to your design.

---

## 📋 The Interview Template (Fill This Out As You Ask)

```
BUSINESS CONTEXT
├─ Business Question: _________________________________
├─ Who Uses This: ____________________________________
└─ Success Metric: ___________________________________

DATA SOURCES
├─ Source 1: __________ (Type: ______, Volume: ______)
├─ Source 2: __________ (Type: ______, Volume: ______)
└─ Source 3: __________ (Type: ______, Volume: ______)

REQUIREMENTS
├─ Latency: Real-time / Hourly / Daily / Weekly
├─ History Needed: Yes / No (How far back: ________)
└─ Update Frequency: _________________________________

FACT TABLE (The Event)
├─ Grain: One row = __________________________________
├─ Measures: [__________, __________, __________]
└─ When it happens: __________________________________

DIMENSIONS (The Context)
├─ WHO: ______________________________________________
├─ WHAT: _____________________________________________
├─ WHEN: _____________________________________________
└─ WHERE: ____________________________________________
```

---

## 🎯 The 3-Phase Question Strategy

### PHASE 1: Understand the Business (2 minutes)
**Goal:** Know what problem you're solving

**Questions to Ask:**
1. "What business question are we trying to answer?"
2. "Who will be using this data and how?"
3. "What does success look like? What metric matters most?"

**Example:**
> Interviewer: "Design a data model for analyzing Uber rides"
> 
> You: "Great! Let me make sure I understand the business need:
> - What business questions do we want to answer? (e.g., 'Which drivers are most profitable?')
> - Who will use this—operations team, finance, product managers?
> - What's the key metric—total rides, revenue, driver ratings?"

**✍️ Write Down:**
```
Business Question: "Which drivers are most profitable by city?"
Who Uses This: Operations team, Finance
Success Metric: Revenue per driver, Rides per hour
```

---

### PHASE 2: Understand the Data (2 minutes)
**Goal:** Know what data you have to work with

**Questions to Ask:**
1. "What are the source systems? (databases, APIs, files?)"
2. "How much data are we talking about? (rows per day/month)"
3. "How often does this data update?"
4. "Do we need historical data or just current state?"

**Example:**
> You: "Let me understand the data sources:
> - Where does ride data come from—a MySQL database, an API?
> - How many rides per day are we talking about?
> - Do we need to track changes over time, like if a driver changes their car?
> - Is this data updated in real-time or batch?"

**✍️ Write Down:**
```
DATA SOURCES
├─ rides table (PostgreSQL): 1M rides/day
├─ drivers table (PostgreSQL): 100K drivers
└─ vehicles table (MongoDB): 50K vehicles

REQUIREMENTS
├─ Latency: Daily batch (acceptable)
├─ History: Yes, need 2 years
└─ Updates: Nightly at 2 AM
```

---

### PHASE 3: Identify the Event & Context (1 minute)
**Goal:** Figure out your fact table and dimensions

**Questions to Ask:**
1. "What's the event we're measuring? (the transaction, the action)"
2. "What do we want to measure about it? (amount, quantity, duration)"
3. "What context do we need? (who, what, when, where)"

**Example:**
> You: "Let me clarify the grain and dimensions:
> - Is one row = one ride? Or one row = one ride per driver-passenger pair?
> - What do we measure—fare amount, distance, duration, tip?
> - What context matters—driver info, passenger info, pickup/dropoff location, time?"

**✍️ Write Down:**
```
FACT TABLE: fact_rides
├─ Grain: One row = one completed ride
├─ Measures: fare_amount, distance_miles, duration_minutes, tip_amount
└─ When: ride_completed_timestamp

DIMENSIONS
├─ WHO: dim_driver (driver_id, name, rating, city)
├─ WHO: dim_passenger (passenger_id, name, signup_date)
├─ WHAT: dim_vehicle (vehicle_id, make, model, year)
├─ WHEN: dim_date (date_key, date, day_of_week, month, quarter)
└─ WHERE: dim_location (location_id, city, state, lat, long)
```

---

## 🗺️ From Questions to Design (The Bridge)

Now that you have your template filled out, here's how to turn it into a design:

### Step 1: State Your Understanding (30 seconds)
> "Based on what you've told me, here's what I understand:
> - We're analyzing Uber rides to find profitable drivers
> - We have 1M rides per day from PostgreSQL
> - We need daily updates with 2 years of history
> - The key event is a completed ride
> 
> Does that sound right?"

**Why this works:** Confirms you listened and gives interviewer a chance to correct you

### Step 2: Propose the Fact Table (1 minute)
> "I'd design a fact table called `fact_rides` where:
> - **Grain:** One row = one completed ride
> - **Measures:** fare_amount, distance_miles, duration_minutes, tip_amount
> - **Foreign keys:** driver_key, passenger_key, vehicle_key, pickup_location_key, dropoff_location_key, date_key
> 
> This grain lets us answer questions like 'total revenue per driver' or 'average ride distance by city.'"

**Why this works:** Shows you understand grain and how it enables analysis

### Step 3: Propose the Dimensions (1 minute)
> "I'd create these dimension tables:
> - **dim_driver:** driver info, rating, city, join_date
> - **dim_passenger:** passenger info, signup_date
> - **dim_vehicle:** vehicle details, make, model
> - **dim_location:** city, state, coordinates (for pickup/dropoff)
> - **dim_date:** standard date dimension
> 
> For driver changes like rating or city, I'd use Type 2 SCD to track history."

**Why this works:** Shows you know what context is needed and how to handle changes

### Step 4: Explain the Pipeline (1 minute)
> "For the pipeline, I'd:
> 1. Extract from PostgreSQL nightly
> 2. Load into Bronze layer (raw data)
> 3. Transform in Silver layer (clean, deduplicate)
> 4. Build star schema in Gold layer
> 5. Connect to Tableau for dashboards
> 
> This gives us flexibility to re-transform if business logic changes."

**Why this works:** Shows end-to-end thinking

---

## 💡 Pro Tips to Avoid Getting Lost

### Tip 1: Take Notes in the Template
**Don't just ask questions—write down answers immediately**

Use a whiteboard or paper with this structure:
```
┌─────────────────────────────────────┐
│ BUSINESS: Revenue per driver       │
├─────────────────────────────────────┤
│ SOURCES: PostgreSQL (1M rides/day) │
├─────────────────────────────────────┤
│ FACT: fact_rides (grain = 1 ride)  │
│   - fare_amount                     │
│   - distance_miles                  │
├─────────────────────────────────────┤
│ DIMS: driver, passenger, vehicle,   │
│       location, date                │
└─────────────────────────────────────┘
```

### Tip 2: Ask Questions in Order
**Don't jump around—follow the 3 phases:**
1. Business first (why)
2. Data second (what)
3. Design third (how)

This keeps you organized and shows structured thinking.

### Tip 3: Summarize After Each Phase
**After Phase 1:**
> "So we're building this for the operations team to find profitable drivers. Got it."

**After Phase 2:**
> "We have 1M rides per day from PostgreSQL, need daily updates. Understood."

**After Phase 3:**
> "The event is a completed ride, and we measure fare, distance, duration. Makes sense."

This confirms understanding and keeps you on track.

### Tip 4: Draw As You Go
**Visual > Text**

```
     ┌──────────────┐
     │  fact_rides  │
     │──────────────│
     │ ride_id      │
     │ driver_key ──┼───> dim_driver
     │ passenger_key├───> dim_passenger
     │ vehicle_key ─┼───> dim_vehicle
     │ date_key ────┼───> dim_date
     │ fare_amount  │
     │ distance     │
     └──────────────┘
```

Drawing helps you organize and shows the interviewer your thought process.

---

## 🎭 Practice Scenario: E-commerce Orders

**Interviewer:** "Design a data model for analyzing e-commerce orders."

**Your Response (Using the Framework):**

### Phase 1: Business (2 min)
**You:** "Let me understand the business need:
- What questions do we want to answer? Revenue by product? Customer lifetime value?
- Who uses this—marketing, finance, product team?
- What's the key metric we care about?"

**Interviewer:** "Marketing wants to see which products drive the most revenue and which customers are most valuable."

**✍️ You write:**
```
Business: Revenue by product, Customer LTV
Users: Marketing team
Metric: Total revenue, Repeat purchase rate
```

### Phase 2: Data (2 min)
**You:** "Got it. Now about the data:
- Where does order data come from—MySQL, API?
- How many orders per day?
- Do we need to track order status changes (pending → shipped → delivered)?
- How far back do we need history?"

**Interviewer:** "Orders are in PostgreSQL, about 10K orders/day. Yes, track status changes. Need 3 years of history."

**✍️ You write:**
```
Source: PostgreSQL orders table (10K/day)
History: 3 years
Track: Order status changes (Type 2 SCD)
```

### Phase 3: Event & Context (1 min)
**You:** "Perfect. Let me clarify the grain:
- Is one row = one order? Or one row = one product per order (order line item)?
- What do we measure—order total, quantity, discount?
- What context—customer info, product details, date?"

**Interviewer:** "One row = one product per order. Measure quantity, price, discount. Need customer and product details."

**✍️ You write:**
```
FACT: fact_order_items
Grain: One row = one product per order
Measures: quantity, unit_price, discount_amount, total_amount

DIMS: dim_customer, dim_product, dim_date, dim_order_status
```

### Your Design (2 min)
**You:** "Based on what you've told me, here's my design:

**Fact Table: `fact_order_items`**
- Grain: One row per product per order
- Measures: quantity, unit_price, discount_amount, total_amount
- Keys: customer_key, product_key, date_key, order_status_key

**Dimensions:**
- `dim_customer`: customer details, segment, signup_date
- `dim_product`: product name, category, brand
- `dim_date`: standard date dimension
- `dim_order_status`: status (pending, shipped, delivered) - Type 2 SCD to track changes

**Pipeline:**
1. Extract from PostgreSQL nightly
2. Bronze: Raw order data
3. Silver: Clean, deduplicate
4. Gold: Star schema
5. Serve to Tableau

This lets marketing answer 'revenue by product category' and 'customer lifetime value' easily."

**Result:** You stayed organized, showed structured thinking, and delivered a complete design!

---

## ✅ Quick Checklist: Did You Cover Everything?

Before you finish, verify:
- [ ] Defined the business question
- [ ] Identified all data sources
- [ ] Stated the fact table grain clearly
- [ ] Listed all measures in the fact table
- [ ] Identified all necessary dimensions
- [ ] Mentioned how to handle changes (SCD Type 1 or 2)
- [ ] Described the pipeline (Bronze → Silver → Gold)
- [ ] Connected to business value

---

## 🎯 Final Tip: The "Parking Lot"

If the interviewer mentions something complex mid-conversation:

**You:** "That's a great point about handling refunds. Let me note that down and come back to it after we nail the core design."

**Write:** `⭐ TODO: Handle refunds`

This shows you're organized and won't forget important details.

---

## 🚀 Practice This!

1. **Use the template** for every practice problem
2. **Time yourself** - 5 min questions, 5 min design
3. **Record yourself** - Listen to how you organize your thoughts
4. **Practice with a friend** - Have them play interviewer

You've got this! The framework keeps you organized so you can focus on showing your expertise. 💪
