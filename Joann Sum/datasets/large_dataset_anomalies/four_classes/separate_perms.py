import csv
from collections import defaultdict

def separate_permissions(input_file, output_file):
    # Read the input CSV file
    with open(input_file, 'r') as f:
        reader = csv.DictReader(f)
        data = list(reader)

    # Prepare the output data
    output_data = []
    for row in data:
        permissions = row['permissions'].split(',')
        for permission in permissions:
            new_row = row.copy()
            new_row['permissions'] = permission.strip()
            output_data.append(new_row)

    # Write the output CSV file
    with open(output_file, 'w', newline='') as f:
        fieldnames = data[0].keys()
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(output_data)

def main():
    input_file = 'rules_combined_permissions.csv'
    output_file = 'rules_separated_permissions.csv' 

    separate_permissions(input_file, output_file)
    print(f"Permissions separated and saved to {output_file}")

if __name__ == "__main__":
    main()