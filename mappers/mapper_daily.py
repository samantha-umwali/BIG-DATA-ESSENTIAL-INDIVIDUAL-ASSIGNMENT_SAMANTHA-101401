#!/usr/bin/env python3
import sys
from datetime import datetime

for line in sys.stdin:
    line = line.strip()
    if not line or line.startswith("VendorID") or line.startswith("tpep_pickup_datetime"):
        continue
    fields = line.split(",")
    if len(fields) > 1:
        try:
            pickup_dt = datetime.strptime(fields[1].strip(), "%Y-%m-%d %H:%M:%S")
            day_name = pickup_dt.strftime("%A")
            print(f"{day_name}\t1")
        except Exception:
            continue