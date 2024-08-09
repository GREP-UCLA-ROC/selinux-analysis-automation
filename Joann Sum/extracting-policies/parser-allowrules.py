import csv
import re
import sys

def parse_selinux_rule(rule):
    # Extract the main components of the rule
    match = re.match(r'allow (\S+) (\S+):(\S+) (.+)', rule)
    if not match:
        return []

    source, target, obj_class, permissions_str = match.groups()
    
    # Check if permissions are in curly braces
    if permissions_str.startswith('{'):
        # Multiple permissions
        permissions = re.findall(r'\w+', permissions_str)
    else:
        # Single permission
        permissions = [permissions_str.strip()]

    # Generate a row for each permission
    return [
        [source, target, obj_class, permission]
        for permission in permissions
    ]

# Check if input file is provided as command-line argument
if len(sys.argv) < 2:
    print("Usage: python script_name.py input_file.txt")
    sys.exit(1)

# Input and output file names
input_file = sys.argv[1]
output_file = 'SELinuxRealTE.csv'

# Read rules from file and write to CSV
try:
    with open(input_file, 'r') as infile, open(output_file, 'w', newline='') as outfile:
        csv_writer = csv.writer(outfile)
        csv_writer.writerow(['Source', 'Target', 'ObjectClass', 'Permission'])  # Write header

        for line in infile:
            rule = line.strip()
            if rule:  # Skip empty lines
                parsed_rows = parse_selinux_rule(rule)
                csv_writer.writerows(parsed_rows)

    print(f"Parsing complete. {output_file} has been created.")
except FileNotFoundError:
    print(f"Error: The file '{input_file}' was not found.")
    sys.exit(1)
except PermissionError:
    print(f"Error: Permission denied when trying to read '{input_file}' or write to '{output_file}'.")
    sys.exit(1)
except Exception as e:
    print(f"An error occurred: {str(e)}")
    sys.exit(1)
