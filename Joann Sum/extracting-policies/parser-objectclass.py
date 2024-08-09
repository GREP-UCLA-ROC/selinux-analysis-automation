from setools import SELinuxPolicy
import csv

def get_all_permissions(class_obj):
    perms = set(class_obj.perms)
    try:
        if class_obj.common:
            perms.update(class_obj.common.perms)
    except:
        pass  # If there's no common, just continue with the class's own permissions
    return perms

# Load the policy
policy = SELinuxPolicy()

# Open CSV file for writing
with open('objectclass.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Name', 'Permissions'])  # Write header

    # Iterate through all object classes
    for class_obj in policy.classes():
        class_name = class_obj.name
        all_perms = get_all_permissions(class_obj)
        perms_str = ', '.join(sorted(all_perms))
        writer.writerow([class_name, perms_str])

print("Object class data has been saved to objectclass.csv")