#!/bin/bash

POLICY_DIR="/etc/selinux/targeted/policy"
OUTPUT_DIR="selinux_policy_output"

# Create output directory if it doesn't exist
mkdir -p $OUTPUT_DIR

# Find the latest policy file
POLICY_FILE=$(ls -t $POLICY_DIR/policy.* | head -1)

if [ -z "$POLICY_FILE" ]; then
    echo "No policy file found in $POLICY_DIR"
    exit 1
fi

echo "Using policy file: $POLICY_FILE"

# Extract allow rules
echo "Extracting allow rules..."
sesearch --allow $POLICY_FILE > $OUTPUT_DIR/allow_rules.txt

# Extract type attributes
echo "Extracting type attributes..."
seinfo -t $POLICY_FILE > $OUTPUT_DIR/type_attributes.txt

# Extract object classes and permissions
echo "Extracting object classes and permissions..."
seinfo -c $POLICY_FILE > $OUTPUT_DIR/object_classes.txt

echo "Extraction complete. Output files are in $OUTPUT_DIR"
