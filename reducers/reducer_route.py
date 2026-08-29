#!/usr/bin/env python3
import sys

current_route, trips, total_rev = None, 0, 0.0

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    route, val = line.split("\t")
    c, r = map(float, val.split(","))

    if current_route == route:
        trips += int(c)
        total_rev += r
    else:
        if current_route:
            print(f"{current_route}\t{trips}\t{total_rev:.2f}")
        current_route, trips, total_rev = route, int(c), r

if current_route:
    print(f"{current_route}\t{trips}\t{total_rev:.2f}")