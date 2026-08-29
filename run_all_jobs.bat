@echo off
SETLOCAL ENABLEDELAYEDEXPANSION

:: Find Hadoop Streaming JAR automatically from HADOOP_HOME
FOR /R "%HADOOP_HOME%\share\hadoop\tools\lib" %%F IN (hadoop-streaming-*.jar) DO (
    SET STREAMING_JAR=%%F
)

echo Using Hadoop Streaming JAR: %STREAMING_JAR%

:: List of standard MapReduce analyses
SET JOBS=hourly daily location payment distance route duration anomaly revenue

:: Loop through and execute each job
FOR %%J IN (%JOBS%) DO (
    echo.
    echo ================= Starting MapReduce Job: %%J =================
    call hdfs dfs -rm -r -f /taxi_project/output/%%J

    call hadoop jar "%STREAMING_JAR%" ^
        -input /taxi_project/input/cleaned ^
        -output /taxi_project/output/%%J ^
        -mapper "python mapper_%%J.py" ^
        -reducer "python reducer_%%J.py" ^
        -file mappers\mapper_%%J.py ^
        -file reducers\reducer_%%J.py
)

:: Execute Stage 2 of Multi-Stage MapReduce (Top 10 Revenue)
echo.
echo ================= Starting Multi-Stage Job 2: Top 10 Revenue =================
call hdfs dfs -rm -r -f /taxi_project/output/revenue_top10

call hadoop jar "%STREAMING_JAR%" ^
    -input /taxi_project/output/revenue ^
    -output /taxi_project/output/revenue_top10 ^
    -mapper "python mapper_top10.py" ^
    -reducer "python reducer_top10.py" ^
    -file mappers\mapper_top10.py ^
    -file reducers\reducer_top10.py

echo.
echo ================= All Hadoop Jobs Completed Successfully =================
pause