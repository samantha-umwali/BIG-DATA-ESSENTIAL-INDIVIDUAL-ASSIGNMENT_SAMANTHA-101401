#!/usr/bin/env python3
import sys

for line in sys.stdin:
    line = line.strip()
    if not line or line.startswith("VendorID") or line.startswith("tpep_pickup_datetime"):
        continue
    fields = line.split(",")
    if len(fields) > 16:
        try:
            dist = float(fields[4])
            fare = float(fields[10])
            tip = float(fields[13])

            if dist <= 2: cat = "0-2_miles"
            elif dist <= 5: cat = "2-5_miles"
            elif dist <= 10: cat = "5-10_miles"
            elif dist <= 20: cat = "10-20_miles"
            else: cat = "20+_miles"

            print(f"{cat}\t1,{fare},{tip},{dist}")
        except ValueError:
            continue