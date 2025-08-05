import re
import json

with open("Daily_Reflections.txt", "r", encoding="utf-8") as file:
    content = file.read()

entries = re.split(r'\n(?=[A-Z]{3,9} \d{1,2}(?:\n| ))', content)

readings = {}

for entry in entries:
    lines = entry.strip().splitlines()
    if not lines:
        continue

    # Extract date from first line
    match = re.match(r'^([A-Z]{3,9} \d{1,2})', lines[0])
    if not match:
        continue
    date_key = match.group(1).title()

    # Remove the date part from the first line to get the rest of the content for that day
    first_line_rest = lines[0][len(match.group(1)):].strip()
    reading_lines = [first_line_rest] + lines[1:] if first_line_rest else lines[1:]
    reading = "\n".join(reading_lines).strip()

    if date_key and reading:
        readings[date_key] = reading

with open("Daily_Reflections.json", "w", encoding="utf-8") as json_file:
    json.dump(readings, json_file, indent=2, ensure_ascii=False)

print("✅ Conversion complete! Saved as 'Daily_Reflections.json'")

