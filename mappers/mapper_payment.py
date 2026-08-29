#!/usr/bin/env python3
import sys

# Payment types: 1=Credit card, 2=Cash, 3=No charge, 4=Dispute
pay_map = {"1": "Credit_Card", "2": "Cash", "3": "No_Charge", "4": "Dispute"}

for line in sys.stdin:
    line = line.strip()
    if not line or line.startswith("VendorID") or line.startswith("tpep_pickup_datetime"):
        continue
    fields = line.split(",")
    if len(fields) > 16:
        try:
            ptype = pay_map.get(fields[9].strip(), "Other")
            fare = float(fields[10])
            tip = float(fields[13])
            total = float(fields[16])
            print(f"{ptype}\t1,{fare},{tip},{total}")
        except ValueError:
            continue