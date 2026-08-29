#!/usr/bin/env python3
import sys

valid_count, anomaly_count = 0, 0
for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    status, count = line.split("\t")
    if status == "VALID":
        valid_count += int(count)
    else:
        anomaly_count += int(count)

total = valid_count + anomaly_count
pct = (anomaly_count / total * 100) if total > 0 else 0
print(f"VALID_RECORDS\t{valid_count}")
print(f"ANOMALY_RECORDS\t{anomaly_count}")
print(f"ANOMALY_PERCENTAGE\t{pct:.2f}%")