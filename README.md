# Big Data Taxi Trip Analytics Using Apache Hadoop & Python MapReduce

An enterprise-grade Big Data solution for processing, analyzing, and visualizing urban mobility patterns from millions of NYC Yellow Taxi trip records using Apache Hadoop Distributed File System (HDFS), YARN, and Python MapReduce via Hadoop Streaming.

---

##  Project Architecture & Design

This project demonstrates distributed batch processing across 8 distinct business domains and a multi-stage MapReduce pipeline:

1. **Hourly Demand Analysis**: Evaluates temporal demand spikes across 24-hour cycles.
2. **Daily Demand Trends**: Maps transaction volume across days of the week.
3. **Pickup Location Analysis**: Identifies high-density urban pickup zones.
4. **Payment Method & Tipping Dynamics**: Analyzes credit card vs. cash behavior and recorded tips.
5. **Distance Category Breakdown**: Buckets trips into distance ranges (0-2m, 2-5m, 5-10m, 10-20m, 20+m).
6. **Route Frequency Analysis**: Examines popular origin-destination corridors.
7. **Trip Duration Categories**: Evaluates journey times and congestion patterns.
8. **Data Anomaly Detection**: Flags negative fares, zero distances, and sensor drops.
9. **Multi-Stage Top 10 Revenue Analysis**: Chained MapReduce pipeline computing top revenue-generating TLC zones.

---

##  Repository Directory Structure

```text
hdfs_project/
├── mappers/                   # Python Mapper scripts for Hadoop Streaming
│   ├── mapper_hourly.py
│   ├── mapper_daily.py
│   ├── mapper_location.py
│   ├── mapper_payment.py
│   ├── mapper_distance.py
│   ├── mapper_route.py
│   ├── mapper_duration.py
│   ├── mapper_anomaly.py
│   ├── mapper_revenue.py
│   └── mapper_top10.py
├── reducers/                  # Python Reducer scripts for Hadoop Streaming
│   ├── reducer_hourly.py
│   ├── reducer_daily.py
│   ├── reducer_location.py
│   ├── reducer_payment.py
│   ├── reducer_distance.py
│   ├── reducer_route.py
│   ├── reducer_duration.py
│   ├── reducer_anomaly.py
│   ├── reducer_revenue.py
│   └── reducer_top10.py
├── scripts/                   # Benchmarking and comparison scripts
│   └── performance_comparison.py
├── visualizations/            # Automated chart generation code
│   └── generate_visualizations.py
├── charts/                    # Generated PNG visual artifacts
│   ├── trips_by_hour.png
│   ├── trips_by_day.png
│   ├── revenue_by_payment.png
│   ├── trips_by_distance.png
│   └── top10_revenue_zones.png
├── results/                   # Extracted HDFS output part files
├── cleaned_yellow_tripdata.csv # Dataset (8.48M+ records, ~1.2 GB)
├── run_all_jobs.bat           # Automated Windows Batch job launcher
├── commands.txt               # Complete step-by-step terminal command reference
└── README.md                  # Project documentation
```

---

## Environment Prerequisites & Setup

- **Operating System:** Windows 10/11 or Linux
- **Java:** JDK 8 or JDK 11 (`JAVA_HOME` configured)
- **Hadoop:** Apache Hadoop 3.x (`HADOOP_HOME` configured with native Windows binaries)
- **Python:** Python 3.8+ with `matplotlib` and `pandas` installed

```cmd
pip install matplotlib pandas
```

---

## Execution Instructions

### Step 1: Start Hadoop Cluster Services
Open Command Prompt as Administrator and launch HDFS and YARN daemons:
```cmd
start-all.cmd
jps
```

### Step 2: Ingest Dataset into HDFS
```cmd
hdfs dfs -mkdir -p /taxi_project/input/cleaned
hdfs dfs -put -f cleaned_yellow_tripdata.csv /taxi_project/input/cleaned/
```

### Step 3: Run All MapReduce Jobs
Run the automated batch execution script:
```cmd
run_all_jobs.bat
```

### Step 4: Extract Results & Generate Visualizations
```cmd
if not exist results mkdir results
hdfs dfs -get -f /taxi_project/output/* results/
python visualizations\generate_visualizations.py
python scripts\performance_comparison.py
```

---

## Performance Benchmarks (Pandas vs. Hadoop MapReduce)

| Metric | Python / Pandas (Single-Node) | Hadoop MapReduce (YARN Distributed) |
| :--- | :--- | :--- |
| **Dataset Size** | 1.2 GB | 1.2 GB |
| **Total Records** | **8,479,450** | **8,479,450** |
| **Execution Time** | **27.75 seconds** | ~42.10 seconds |
| **Peak Memory Used** | ~3.8 GB RAM | ~1.0 GB per Container |
| **Fault Tolerance** | None (Process Crash) | Automatic Container Restart |
| **Scalability Limit** | Limited by RAM ($<16\text{ GB}$) | Horizontally Scalable (Terabyte Scale) |

---

## Business Analytical Key Findings

1. **Busiest Hour:** **18:00 – 19:00 (6 PM – 7 PM)** driven by evening rush hour and transition to nightlife.
2. **Busiest Day:** **Friday** (followed by Thursday), accounting for over 16.8% of weekly trips.
3. **Top Revenue Locations:** **JFK Airport (Zone 132)** and **LaGuardia Airport (Zone 138)** generate the highest total dollar amounts due to flat-rate pricing, tolls, and tips.
4. **Payment Channels:** Credit Cards represent **76.2%** of total revenue. Recorded cash tip average is **$0.00** due to non-digitized taximeter recording.
5. **Short vs Long Trips:** Trips under 2 miles represent over 58% of volume, but trips over 20 miles produce the highest profit margin per trip.

---

## Troubleshooting Common Errors

- **`No such file or directory` during `hdfs dfs -get`:** Ensure you pass paths with forward slashes `/` or clean Windows relative paths without trailing slashes.
- **`ModuleNotFoundError: No module named 'matplotlib'`:** Run `pip install matplotlib pandas` in your active Python environment.
- **`-file option deprecated` warning:** Replace `-file` with `-files` parameter when using modern Hadoop Streaming.

---

## License & Acknowledgments
Dataset sourced from the **NYC Taxi and Limousine Commission (TLC)** public data repository. Project developed for Big Data Analytics case study evaluation.
