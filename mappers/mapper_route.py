#!/usr/bin/env python3
import sys

for line in sys.stdin:
    line = line.strip()
    if not line or line.startswith("VendorID") or line.startswith("tpep_pickup_datetime"):
        continue
    fields = line.split(",")
    if len(fields) > 16:
        try:
            pu = fields[7].strip()
            do = fields[8].strip()
            rev = float(fields[16])
            if pu and do:
                print(f"{pu}->{do}\t1,{rev}")
        except ValueError:
            continue