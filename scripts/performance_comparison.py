import time
import pandas as pd
import sys

def benchmark_pandas(file_path):
    print("Starting Pandas benchmark...")
    start_time = time.time()
    
    # Read dataset
    df = pd.read_csv(file_path, low_memory=False)
    
    # Simple Aggregation: Revenue by Pickup Location
    result = df.groupby('PULocationID')['total_amount'].sum().reset_index()
    
    elapsed_time = time.time() - start_time
    
    print("--- Pandas Benchmark Results ---")
    print(f"File Processed: {file_path}")
    print(f"Total Rows: {len(df):,}")
    print(f"Execution Time: {elapsed_time:.2f} seconds")

if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "cleaned_yellow_tripdata.csv"
    benchmark_pandas(path)