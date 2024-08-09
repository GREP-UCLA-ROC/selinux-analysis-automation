#!/bin/bash

# Function to check if a command was successful
check_command() {
    if [ $? -ne 0 ]; then
        echo "Error: $1 failed"
        exit 1
    fi
}

# Run sesearch and save output
echo "Extracting allow rules..."
sesearch --allow /etc/selinux/targeted/policy/policy.* > allowrules.txt
check_command "Extracting allow rules"

echo "Extracting dontaudit rules..."
sesearch --dontaudit /etc/selinux/targeted/policy/policy.* > dontaudit.txt


# Run seinfo and save output
echo "Extracting type attribute data..."
seinfo -t -x > typeattributedata.txt
check_command "Extracting type attribute data"

# Run Python scripts
echo "Parsing allow rules..."
python parser-allowrules.py allowrules.txt
check_command "Parsing allow rules"

echo "Parsing dontaudit rules..."
python parser-dontaudit.py dontaudit.txt
check_command "Parsing dontaudit rules"

echo "Parsing type attributes..."
python parser-typeattributes.py
check_command "Parsing type attributes"

echo "Generating object class CSV..."
python parser-objectclass.py
check_command "Generating object class CSV"

echo "All operations completed successfully."
