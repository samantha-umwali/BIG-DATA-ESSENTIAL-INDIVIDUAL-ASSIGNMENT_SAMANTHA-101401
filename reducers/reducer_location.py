#!/usr/bin/env python3
import sys

current_zone, total_trips = None, 0
for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    zone, count = line.split("\t")
    if current_zone == zone:
        total_trips += int(count)
    else:
        if current_zone:
            print(f"{current_zone}\t{total_trips}")
        current_zone, total_trips = zone, int(count)
if current_zone:
    print(f"{current_zone}\t{total_trips}")