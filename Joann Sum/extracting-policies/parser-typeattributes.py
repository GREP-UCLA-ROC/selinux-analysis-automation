import csv
import re

def parse_type_attributes(line):
    # Match the type and attributes
    match = re.match(r'\s*type\s+(\S+),\s*(.*?);', line)
    if match:
        type_name = match.group(1)
        attributes = match.group(2).strip()
        return [type_name, attributes]
    return None

# Input and output file names
input_file = 'typeattributedata.txt'
output_file = 'attributes.csv'

# Read from input file and write to CSV
with open(input_file, 'r') as infile, open(output_file, 'w', newline='') as outfile:
    csv_writer = csv.writer(outfile)
    csv_writer.writerow(['1', '2'])  # Write header

    for line in infile:
        # Skip the first line with the type count
        if line.strip().startswith('Types:'):
            continue
        
        parsed = parse_type_attributes(line)
        if parsed:
            csv_writer.writerow(parsed)

print(f"Parsing complete. {output_file} has been created.")