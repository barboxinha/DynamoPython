"""
Sheets.BadSheetNumbers
----------------------
Identifies sheets that do not match a specified text pattern.
"""

import sys
import clr
import re


# For help building the regex pattern here --> https://pythex.org/
sheets = IN[0]
pattern = '\D\d.\d.\d'
bad_sheets = []

# Iterate through sheets and identify which ones don't match text pattern.
for sheet in sheets:
	if re.search(pattern, sheet.SheetNumber):
		pass
	else:
		bad_sheets.append(sheet)

# Output the sheets not matching text pattern.
OUT = bad_sheets