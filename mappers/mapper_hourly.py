import sys

for line in sys.stdin:
    line = line.strip()
    if not line or line.startswith("VendorID") or line.startswith("tpep_pickup_datetime"):
        continue
    parts = line.split(",")
    if len(parts) > 1:
        try:
            pickup_datetime = parts[1].strip()
            time_part = pickup_datetime.split(" ")[1]
            hour = int(time_part.split(":")[0])
            print(f"{hour:02d}\t1")
        except (IndexError, ValueError):
            continue