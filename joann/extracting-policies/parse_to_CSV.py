#This document converts the extracted policies .txt files from the bash script and parses them into csvs. 
import os
import csv
import argparse

# Set up argument parsing
parser = argparse.ArgumentParser(description='Process SELinux policies and import into Memgraph')
parser.add_argument('--input_dir', type=str, required=True, help='Path to the directory containing the SELinux policy txt files')
parser.add_argument('--output_dir', type=str, help='Path to output directory for processed CSV files')
args = parser.parse_args()

# Set output directory
if args.output_dir:
    output_dir = args.output_dir
else:
    output_dir = os.path.join(os.path.expanduser("~"), "Downloads", "selinux-policies-processed")

# Create output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

def process_te_rules(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w', newline='') as outfile:
        csv_writer = csv.writer(outfile)
        csv_writer.writerow(['source', 'target', 'class', 'permission'])  # header
        for line in infile:
            if line.startswith('allow'):
                parts = line.strip().split()
                if len(parts) >= 4:
                    source = parts[1]
                    target = parts[2]
                    class_perms = parts[3].split(':')
                    if len(class_perms) == 2:
                        obj_class = class_perms[0]
                        permissions = class_perms[1].strip('{ }').split()
                        for perm in permissions:
                            csv_writer.writerow([source, target, obj_class, perm])

def process_type_attributes(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w', newline='') as outfile:
        csv_writer = csv.writer(outfile)
        csv_writer.writerow(['type', 'attributes'])  # header
        current_type = None
        attributes = []
        for line in infile:
            if line.startswith('attribute'):
                if current_type and attributes:
                    csv_writer.writerow([current_type, ','.join(attributes)])
                current_type = line.strip().split()[1]
                attributes = []
            elif line.strip().startswith('typeattribute'):
                attr = line.strip().split()[1]
                attributes.append(attr)
        if current_type and attributes:
            csv_writer.writerow([current_type, ','.join(attributes)])

def process_object_classes(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w', newline='') as outfile:
        csv_writer = csv.writer(outfile)
        csv_writer.writerow(['class', 'permissions'])  # header
        current_class = None
        permissions = []
        for line in infile:
            if line.startswith('class'):
                if current_class and permissions:
                    csv_writer.writerow([current_class, ','.join(permissions)])
                current_class = line.strip().split()[1]
                permissions = []
            elif not line.strip():  # empty line indicates end of current class
                if current_class and permissions:
                    csv_writer.writerow([current_class, ','.join(permissions)])
                current_class = None
                permissions = []
            else:
                perms = line.strip().split()
                permissions.extend(perms)
        if current_class and permissions:
            csv_writer.writerow([current_class, ','.join(permissions)])

# Process the txt files
process_te_rules(os.path.join(args.input_dir, "allow_rules.txt"), os.path.join(output_dir, "te_rules.csv"))
process_type_attributes(os.path.join(args.input_dir, "type_attributes.txt"), os.path.join(output_dir, "type_attributes.csv"))
process_object_classes(os.path.join(args.input_dir, "object_classes.txt"), os.path.join(output_dir, "object_classes.csv"))

print("Policy processing completed. CSV files are in", output_dir)
