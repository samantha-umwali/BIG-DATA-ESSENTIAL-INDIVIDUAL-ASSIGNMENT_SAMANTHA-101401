#!/bin/bash
chmod +x mappers/*.py reducers/*.py

HADOOP_STREAMING_JAR=$(find $HADOOP_HOME/ -name "hadoop-streaming-*.jar" | head -n 1)

jobs=("hourly" "daily" "location" "payment" "distance" "route" "duration" "anomaly" "revenue")

for job in "${jobs[@]}"; do
    echo "================ Starting MapReduce Job: $job ================"
    # Remove output path if already exists
    hdfs dfs -rm -r -f /taxi_project/output/$job

    hadoop jar $HADOOP_STREAMING_JAR \
        -input /taxi_project/input/cleaned \
        -output /taxi_project/output/$job \
        -mapper "python3 mapper_${job}.py" \
        -reducer "python3 reducer_${job}.py" \
        -file mappers/mapper_${job}.py \
        -file reducers/reducer_${job}.py
done

# Execute Multi-Stage Job 2 (Top 10 Revenue from Stage 1 Revenue Output)
echo "================ Starting Multi-Stage Job 2: Top 10 Revenue ================"
hdfs dfs -rm -r -f /taxi_project/output/revenue_top10

hadoop jar $HADOOP_STREAMING_JAR \
    -input /taxi_project/output/revenue \
    -output /taxi_project/output/revenue_top10 \
    -mapper "python3 mapper_top10.py" \
    -reducer "python3 reducer_top10.py" \
    -file mappers/mapper_top10.py \
    -file reducers/reducer_top10.py

echo "================ All Hadoop Jobs Complete ================"