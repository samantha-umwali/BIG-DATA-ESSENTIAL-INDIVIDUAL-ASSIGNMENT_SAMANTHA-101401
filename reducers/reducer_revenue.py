#!/usr/bin/env python3
import sys

current_zone = None
trips, total_fare, total_tip, total_rev, total_dist = 0, 0.0, 0.0, 0.0, 0.0

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    zone, val = line.split("\t")
    c, f, t, r, d = map(float, val.split(","))

    if current_zone == zone:
        trips += int(c)
        total_fare += f
        total_tip += t
        total_rev += r
        total_dist += d
    else:
        if current_zone:
            avg_f = total_fare / trips
            avg_d = total_dist / trips
            print(f"{current_zone}\t{trips}\t{total_fare:.2f}\t{total_tip:.2f}\t{total_rev:.2f}\t{avg_f:.2f}\t{avg_d:.2f}")
        current_zone = zone
        trips, total_fare, total_tip, total_rev, total_dist = int(c), f, t, r, d

if current_zone:
    avg_f = total_fare / trips
    avg_d = total_dist / trips
    print(f"{current_zone}\t{trips}\t{total_fare:.2f}\t{total_tip:.2f}\t{total_rev:.2f}\t{avg_f:.2f}\t{avg_d:.2f}")