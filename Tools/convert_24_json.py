import re
import json

def convert_text_to_json(input_txt_path, output_json_path):
    with open(input_txt_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    data = {}
    current_date = None
    current_text_lines = []

    # Regex to detect date header lines (e.g. "JANUARY 1—AA Thought for the Day")
    date_header_pattern = re.compile(r'^[A-Z]+\s\d+—AA Thought for the Day')

    for line in lines:
        line = line.rstrip('\n')
        if date_header_pattern.match(line):
            # Save previous entry if exists
            if current_date:
                data[current_date] = '\n'.join(current_text_lines).strip()

            # Start new entry
            current_date = line.split('—')[0].title()  # e.g. "January 1"
            current_text_lines = [line]  # keep header line too
        else:
            if current_date:
                current_text_lines.append(line)

    # Save last entry
    if current_date:
        data[current_date] = '\n'.join(current_text_lines).strip()

    # Save to JSON
    with open(output_json_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"Converted text file saved to {output_json_path}")

# Example usage:
convert_text_to_json('24hoursaday.txt', '24hoursaday.json')


