#!/usr/bin/env python3
import sys

current_p, trips, total_fare, total_tip, total_rev = None, 0, 0.0, 0.0, 0.0

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    ptype, val = line.split("\t")
    c, f, t, r = map(float, val.split(","))

    if current_p == ptype:
        trips += int(c)
        total_fare += f
        total_tip += t
        total_rev += r
    else:
        if current_p:
            print(f"{current_p}\t{trips}\t{total_rev:.2f}\t{(total_fare/trips):.2f}\t{(total_tip/trips):.2f}")
        current_p, trips, total_fare, total_tip, total_rev = ptype, int(c), f, t, r

if current_p:
    print(f"{current_p}\t{trips}\t{total_rev:.2f}\t{(total_fare/trips):.2f}\t{(total_tip/trips):.2f}")