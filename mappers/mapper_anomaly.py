#!/usr/bin/env python3
import sys
from datetime import datetime

for line in sys.stdin:
    line = line.strip()
    if not line or line.startswith("VendorID") or line.startswith("tpep_pickup_datetime"):
        continue
    fields = line.split(",")
    if len(fields) > 16:
        try:
            passengers = int(fields[3])
            dist = float(fields[4])
            fare = float(fields[10])
            pu_t = datetime.strptime(fields[1].strip(), "%Y-%m-%d %H:%M:%S")
            do_t = datetime.strptime(fields[2].strip(), "%Y-%m-%d %H:%M:%S")
            duration = (do_t - pu_t).total_seconds() / 60.0

            is_anomaly = False
            if passengers <= 0 or dist <= 0 or fare <= 0 or duration <= 0:
                is_anomaly = True
            elif dist > 0 and (fare / dist > 200 or fare / dist < 0.5):
                is_anomaly = True

            status = "ANOMALY" if is_anomaly else "VALID"
            print(f"{status}\t1")
        except Exception:
            print("ANOMALY\t1")