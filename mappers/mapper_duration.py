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
            pu_t = datetime.strptime(fields[1].strip(), "%Y-%m-%d %H:%M:%S")
            do_t = datetime.strptime(fields[2].strip(), "%Y-%m-%d %H:%M:%S")
            duration_mins = (do_t - pu_t).total_seconds() / 60.0
            
            fare = float(fields[10])
            dist = float(fields[4])

            if duration_mins <= 10: cat = "0-10_min"
            elif duration_mins <= 20: cat = "10-20_min"
            elif duration_mins <= 40: cat = "20-40_min"
            elif duration_mins <= 60: cat = "40-60_min"
            else: cat = "60+_min"

            print(f"{cat}\t1,{fare},{dist}")
        except Exception:
            continue