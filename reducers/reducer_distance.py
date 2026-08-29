#!/usr/bin/env python3
import sys

current_cat, trips, total_fare, total_tip, total_dist = None, 0, 0.0, 0.0, 0.0

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    cat, val = line.split("\t")
    c, f, t, d = map(float, val.split(","))

    if current_cat == cat:
        trips += int(c)
        total_fare += f
        total_tip += t
        total_dist += d
    else:
        if current_cat:
            print(f"{current_cat}\t{trips}\t{total_fare:.2f}\t{(total_fare/trips):.2f}\t{(total_tip/trips):.2f}")
        current_cat, trips, total_fare, total_tip, total_dist = cat, int(c), f, t, d

if current_cat:
    print(f"{current_cat}\t{trips}\t{total_fare:.2f}\t{(total_fare/trips):.2f}\t{(total_tip/trips):.2f}")