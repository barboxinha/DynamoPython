"""
File.DuplicateToNewFilepath
----------------
Duplicates template or file to new filepath
using the shutil Python library
"""


import shutil


# Auto-copies the Excel template file using Python's shutil library.
template_path = IN[0]
output_path = IN[1]
project_number = IN[2]
project_name = IN[3]

# Create new filename. Format: "12345.000 ProjectName Warnings Dashboard"
new_file_name = '{0} {1} Warnings Dashboard'.format(project_number, project_name)

# Extract file extension from the template path
file_extension = template_path.split('.')[-1]

# Destination filepath (include file extension)
new_filepath = '{0}\\{1}{2}'.format(output_path, new_file_name, file_extension)

# Shutil arguments: (filepath to copy file from, new destination filepath)
shutil.copy2(template_path, new_filepath)

# Output the full filepath, with extension, for later in the process!
OUT = new_filepath
