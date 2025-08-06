import re
import json

with open("NABasicTextClean.txt", "r", encoding="utf-8") as f:
    text = f.read()

# Split pages by a newline with just a number (page number)
# The pattern looks for lines that contain only digits (with optional spaces)
pages_raw = re.split(r'\n\s*\d+\s*\n', text)

# Remove empty strings if any (e.g. before first page number)
pages = [p.strip() for p in pages_raw if p.strip()]

# Create dictionary: page number as string -> page text with line breaks intact
pages_dict = {str(i+1): page for i, page in enumerate(pages)}

# Save JSON with line breaks preserved
with open("NA_Basic_Text.json", "w", encoding="utf-8") as f:
    json.dump(pages_dict, f, ensure_ascii=False, indent=2)

print(f"Saved {len(pages_dict)} pages with line breaks preserved.")









