import sys

records = []

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    parts = line.split("\t")
    if len(parts) >= 2:
        zone = parts[0]
        try:
            rev_val = float(parts[1].replace("$", "").replace(",", ""))
            records.append((zone, rev_val))
        except ValueError:
            continue

records.sort(key=lambda x: x[1], reverse=True)

for zone, revenue in records[:10]:
    print(f"Zone {zone}\t${revenue:,.2f}")