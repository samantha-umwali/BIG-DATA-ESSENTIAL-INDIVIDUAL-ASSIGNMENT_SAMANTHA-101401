#!/usr/bin/env python3
import sys

current_day, total_trips = None, 0
for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    day, count = line.split("\t")
    if current_day == day:
        total_trips += int(count)
    else:
        if current_day:
            print(f"{current_day}\t{total_trips}")
        current_day, total_trips = day, int(count)
if current_day:
    print(f"{current_day}\t{total_trips}")