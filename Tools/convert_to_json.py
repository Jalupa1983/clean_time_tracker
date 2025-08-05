import re
import json

# Load the entire text file
with open("Just_For_Today.txt", "r", encoding="utf-8") as file:
    content = file.read()

# Regular expression to find date headers like "January 1"
date_pattern = r"(January|February|March|April|May|June|July|August|September|October|November|December) \d{1,2}"

# Split the content based on the date pattern
splits = re.split(f"(?=\\b{date_pattern}\\b)", content)

# Build dictionar+y from the splits
readings = {}
for entry in splits:
    if not entry.strip():
        continue
    match = re.match(date_pattern, entry.strip())
    if match:
        date = match.group()
        readings[date] = entry.strip()[len(date):].strip()

# Save as JSON
with open("Just_For_Today.json", "w", encoding="utf-8") as json_file:
    json.dump(readings, json_file, indent=2, ensure_ascii=False)

print("✅ Conversion complete. JSON file saved as 'Just_For_Today.json'")
