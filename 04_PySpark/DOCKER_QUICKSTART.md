# 🐳 PySpark Docker Quick Start Guide

## What This Gives You

A fully configured PySpark environment running in Docker with:
- ✅ **PySpark 3.5+** (latest stable)
- ✅ **Jupyter Lab** interface
- ✅ **No Windows compatibility issues**
- ✅ **Spark UI** for monitoring jobs
- ✅ **Persistent notebooks** (saved to your local machine)

## 🚀 Getting Started

### 1. Start the Container

```bash
cd c:\Users\ksank\training\04_PySpark
docker-compose up -d
```

### 2. Access Jupyter Lab

Open your browser and go to:
```
http://localhost:8888
```

No password required! Start coding immediately.

### 3. Access Spark UI (when running jobs)

```
http://localhost:4040
```

## 📝 Your First PySpark Notebook

Create a new notebook and try this:

```python
from pyspark.sql import SparkSession

# Create Spark session
spark = SparkSession.builder \
    .appName("MyFirstSparkApp") \
    .getOrCreate()

# Create a simple DataFrame
data = [("Alice", 34), ("Bob", 45), ("Charlie", 28)]
df = spark.createDataFrame(data, ["Name", "Age"])

# Show the data
df.show()

# Stop the session when done
spark.stop()
```

## 🛠️ Useful Commands

```bash
# Start the container
docker-compose up -d

# Stop the container
docker-compose down

# View logs
docker-compose logs -f

# Restart the container
docker-compose restart

# Check if running
docker ps
```

## 📂 Where Are My Notebooks?

All notebooks are saved in:
```
c:\Users\ksank\training\04_PySpark\notebooks\
```

They persist even when you stop the container!

## 🎯 Why This Is Better Than Local Windows Setup

1. **No Java/Hadoop configuration** - Everything is pre-configured
2. **No winutils.exe errors** - Linux environment handles everything
3. **Consistent environment** - Works the same on any machine
4. **Easy updates** - Just pull the latest image
5. **Isolated** - Doesn't interfere with your Windows Python installations

## 🔧 Troubleshooting

**Container won't start?**
```bash
docker-compose down
docker-compose up -d
```

**Port 8888 already in use?**
Edit `docker-compose.yml` and change `"8888:8888"` to `"8889:8888"`, then access at `http://localhost:8889`

**Want to use a specific Spark version?**
Change the image in `docker-compose.yml`:
```yaml
image: jupyter/pyspark-notebook:spark-3.5.0
```
