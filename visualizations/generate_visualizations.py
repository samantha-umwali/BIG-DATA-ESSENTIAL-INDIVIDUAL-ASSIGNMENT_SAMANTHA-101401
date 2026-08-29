import os
import glob
import matplotlib.pyplot as plt
import pandas as pd

os.makedirs("charts", exist_ok=True)

def find_file(job_name):
    paths = [
        f"results/{job_name}/part*",
        f"results/output/{job_name}/part*",
        f"results/{job_name}/part-00000",
        f"results/output/{job_name}/part-00000"
    ]
    for p in paths:
        matches = glob.glob(p)
        if matches:
            return matches[0]
    return None

# 1. Trips by Hour
hourly_file = find_file("hourly")
if hourly_file:
    df_h = pd.read_csv(hourly_file, sep="\t", names=["Hour", "Trips"]).sort_values("Hour")
    plt.figure(figsize=(10, 5))
    plt.plot(df_h["Hour"], df_h["Trips"], marker="o", color="navy")
    plt.title("Taxi Trips by Hour of Day")
    plt.xlabel("Hour (0-23)")
    plt.ylabel("Total Trips")
    plt.grid(True)
    plt.savefig("charts/trips_by_hour.png")
    plt.close()

# 2. Trips by Day of Week
daily_file = find_file("daily")
if daily_file:
    df_day = pd.read_csv(daily_file, sep="\t", names=["Day", "Trips"])
    plt.figure(figsize=(9, 5))
    plt.bar(df_day["Day"], df_day["Trips"], color="teal")
    plt.title("Taxi Trips by Day of Week")
    plt.ylabel("Total Trips")
    plt.savefig("charts/trips_by_day.png")
    plt.close()

# 3. Revenue by Payment Method
payment_file = find_file("payment")
if payment_file:
    df_p = pd.read_csv(payment_file, sep="\t", names=["Payment", "Trips", "Revenue", "AvgFare", "AvgTip"])
    plt.figure(figsize=(8, 5))
    plt.bar(df_p["Payment"], df_p["Revenue"], color="skyblue")
    plt.title("Total Revenue by Payment Method")
    plt.ylabel("Revenue ($)")
    plt.savefig("charts/revenue_by_payment.png")
    plt.close()

# 4. Trips by Distance Category
distance_file = find_file("distance")
if distance_file:
    df_d = pd.read_csv(distance_file, sep="\t", names=["Category", "Trips", "Revenue", "AvgFare", "AvgTip"])
    plt.figure(figsize=(8, 5))
    plt.bar(df_d["Category"], df_d["Trips"], color="lightgreen")
    plt.title("Trips by Distance Category")
    plt.xlabel("Distance Range")
    plt.ylabel("Trip Count")
    plt.savefig("charts/trips_by_distance.png")
    plt.close()

# 5. Top 10 Revenue Zones
top10_file = find_file("revenue_top10")
if top10_file:
    df_t = pd.read_csv(top10_file, sep="\t", names=["Zone", "Revenue"])
    df_t["Revenue"] = df_t["Revenue"].str.replace("$", "").astype(float)
    plt.figure(figsize=(10, 5))
    plt.barh(df_t["Zone"], df_t["Revenue"], color="coral")
    plt.title("Top 10 Highest Revenue Pickup Zones")
    plt.xlabel("Revenue ($)")
    plt.gca().invert_yaxis()
    plt.savefig("charts/top10_revenue_zones.png")
    plt.close()

print("All charts generated and saved in the 'charts' folder.")