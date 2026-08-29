import sys

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    parts = line.split("\t")
    if len(parts) >= 2:
        zone, revenue = parts[0], parts[1]
        print(f"{zone}\t{revenue}")