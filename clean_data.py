#!/usr/bin/env python3
"""
clean_data.py
Cleans TLC Yellow Taxi CSV data before uploading to HDFS.
Identifies and handles: missing values, invalid passenger counts, 
zero/negative distances, invalid fares, invalid timestamps, duplicates,
and impossible trip durations.

Usage: python clean_data.py --input raw.csv --output cleaned.csv --report report.txt
"""
import os
import sys
import argparse
import pandas as pd
import numpy as np
from datetime import datetime

def clean_taxi_data(input_file, output_file, report_file):
    print(f"Loading data from: {input_file}")
    df = pd.read_csv(input_file, low_memory=False)
    original_count = len(df)
    print(f"Original records: {original_count:,}")

    issues = []

    # 1. Missing values in critical columns
    critical_cols = ['tpep_pickup_datetime', 'tpep_dropoff_datetime', 
                     'passenger_count', 'trip_distance', 'fare_amount', 
                     'PULocationID', 'DOLocationID', 'payment_type']
    # Handle case variations
    col_map = {c.lower(): c for c in df.columns}

    missing_before = len(df)
    df = df.dropna(subset=[c for c in critical_cols if c in df.columns])
    missing_dropped = missing_before - len(df)
    issues.append(f"Missing critical values dropped: {missing_dropped:,} ({100*missing_dropped/original_count:.2f}%)")

    # 2. Invalid passenger counts (must be >= 1 and <= 9)
    if 'passenger_count' in df.columns:
        invalid_pass = len(df[(df['passenger_count'] < 1) | (df['passenger_count'] > 9) | (df['passenger_count'].isna())])
        df = df[(df['passenger_count'] >= 1) & (df['passenger_count'] <= 9)]
        issues.append(f"Invalid passenger_count dropped: {invalid_pass:,} ({100*invalid_pass/original_count:.2f}%)")

    # 3. Zero or negative trip_distance
    if 'trip_distance' in df.columns:
        invalid_dist = len(df[df['trip_distance'] <= 0])
        df = df[df['trip_distance'] > 0]
        issues.append(f"Zero/negative distance dropped: {invalid_dist:,} ({100*invalid_dist/original_count:.2f}%)")

    # 4. Invalid fares (negative or unreasonably high)
    if 'fare_amount' in df.columns:
        invalid_fare = len(df[(df['fare_amount'] <= 0) | (df['fare_amount'] > 1000)])
        df = df[(df['fare_amount'] > 0) & (df['fare_amount'] <= 1000)]
        issues.append(f"Invalid fare_amount dropped: {invalid_fare:,} ({100*invalid_fare/original_count:.2f}%)")

    # 5. Invalid timestamps and trip duration
    if 'tpep_pickup_datetime' in df.columns and 'tpep_dropoff_datetime' in df.columns:
        df['tpep_pickup_datetime'] = pd.to_datetime(df['tpep_pickup_datetime'], errors='coerce')
        df['tpep_dropoff_datetime'] = pd.to_datetime(df['tpep_dropoff_datetime'], errors='coerce')

        invalid_ts = len(df[df['tpep_pickup_datetime'].isna() | df['tpep_dropoff_datetime'].isna()])
        df = df[df['tpep_pickup_datetime'].notna() & df['tpep_dropoff_datetime'].notna()]
        issues.append(f"Invalid timestamps dropped: {invalid_ts:,} ({100*invalid_ts/original_count:.2f}%)")

        # Trip duration in minutes
        df['trip_duration_min'] = (df['tpep_dropoff_datetime'] - df['tpep_pickup_datetime']).dt.total_seconds() / 60.0

        # Impossible durations: negative or > 24 hours (1440 min)
        invalid_dur = len(df[(df['trip_duration_min'] <= 0) | (df['trip_duration_min'] > 1440)])
        df = df[(df['trip_duration_min'] > 0) & (df['trip_duration_min'] <= 1440)]
        issues.append(f"Impossible duration dropped: {invalid_dur:,} ({100*invalid_dur/original_count:.2f}%)")

    # 6. Duplicate records (exact duplicates on key fields)
    dup_cols = ['tpep_pickup_datetime', 'tpep_dropoff_datetime', 'PULocationID', 
                'DOLocationID', 'passenger_count', 'trip_distance', 'fare_amount']
    dup_cols = [c for c in dup_cols if c in df.columns]
    if dup_cols:
        duplicates = df.duplicated(subset=dup_cols, keep='first').sum()
        df = df.drop_duplicates(subset=dup_cols, keep='first')
        issues.append(f"Duplicate records dropped: {duplicates:,} ({100*duplicates/original_count:.2f}%)")

    # 7. Invalid Location IDs (must be > 0)
    for col in ['PULocationID', 'DOLocationID']:
        if col in df.columns:
            invalid_loc = len(df[df[col] <= 0])
            df = df[df[col] > 0]
            issues.append(f"Invalid {col} dropped: {invalid_loc:,} ({100*invalid_loc/original_count:.2f}%)")

    cleaned_count = len(df)
    total_dropped = original_count - cleaned_count

    # Save cleaned data
    df.to_csv(output_file, index=False)
    print(f"\nCleaned data saved to: {output_file}")
    print(f"Final records: {cleaned_count:,}")

    # Write report
    with open(report_file, 'w') as f:
        f.write("=" * 60 + "\n")
        f.write("TAXI DATA CLEANING REPORT\n")
        f.write("=" * 60 + "\n\n")
        f.write(f"Original records:   {original_count:,}\n")
        f.write(f"Cleaned records:    {cleaned_count:,}\n")
        f.write(f"Total dropped:      {total_dropped:,} ({100*total_dropped/original_count:.2f}%)\n\n")
        f.write("Detailed Breakdown:\n")
        f.write("-" * 60 + "\n")
        for issue in issues:
            f.write(f"  • {issue}\n")
        f.write("\nJustification for cleaning rules:\n")
        f.write("  • Missing critical fields: cannot analyze records without key dimensions.\n")
        f.write("  • Passenger count > 9: NYC taxis legally max at specified capacity.\n")
        f.write("  • Zero/negative distance: data entry errors or cancellations.\n")
        f.write("  • Fares > $1000 or <= 0: likely data corruption or test records.\n")
        f.write("  • Duration > 24h: indicates system error or parked meter.\n")
        f.write("  • Duplicates: double-counting biases all aggregations.\n")

    print(f"Report saved to: {report_file}")
    print("\nCleaning Summary:")
    for issue in issues:
        print(f"  • {issue}")
    print(f"\nTotal retention rate: {100*cleaned_count/original_count:.2f}%")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="Input raw CSV file")
    parser.add_argument("--output", required=True, help="Output cleaned CSV file")
    parser.add_argument("--report", default="cleaning_report.txt", help="Cleaning report file")
    args = parser.parse_args()
    clean_taxi_data(args.input, args.output, args.report)
