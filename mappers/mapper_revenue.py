#!/usr/bin/env python3
import sys

for line in sys.stdin:
    line = line.strip()
    if not line or line.startswith("VendorID") or line.startswith("tpep_pickup_datetime"):
        continue
    fields = line.split(",")
    if len(fields) > 16:
        try:
            zone = fields[7].strip()
            fare = float(fields[10])
            tip = float(fields[13])
            total = float(fields[16])
            dist = float(fields[4])
            print(f"{zone}\t1,{fare},{tip},{total},{dist}")
        except ValueError:
            continue