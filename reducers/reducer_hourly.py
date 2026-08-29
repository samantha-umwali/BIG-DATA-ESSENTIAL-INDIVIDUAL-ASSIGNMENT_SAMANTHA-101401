import sys

current_hour = None
current_count = 0

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    parts = line.split("\t")
    if len(parts) != 2:
        continue
    
    hour, count = parts[0], int(parts[1])

    if current_hour == hour:
        current_count += count
    else:
        if current_hour is not None:
            print(f"{current_hour}\t{current_count}")
        current_hour = hour
        current_count = count

if current_hour is not None:
    print(f"{current_hour}\t{current_count}")