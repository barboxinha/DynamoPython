"""
Doors.FindMirrored
-----------------------
This script finds all doors in the Revit document that are mirrored and sets a parameter value accordingly.
"""

import clr

# Import RevitAPI.dll Assembly Classes
clr.AddReference('RevitAPI')
from Autodesk.Revit.DB import FilteredElementCollector, BuiltInCategory

# Import DocumentManager and TransactionManager
clr.AddReference('RevitServices')
from RevitServices.Transactions import TransactionManager
from RevitServices.Persistence import DocumentManager


# Revit Document
doc = DocumentManager.Instance.CurrentDBDocument

# Inputs and variables
param_name = IN[0]  # Parameter name to set, e.g., 'Comments' (Ensure the parameter exists in the document)
mirrored_doors = []  # List to store mirrored doors

# Start Revit Transaction
TransactionManager.Instance.EnsureInTransaction(doc)

doors = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Doors).WhereElementIsNotElementType()

for door in doors:
	if door.Mirrored:
		mirrored_doors.append(door)
		value = 'Is Mirrored'
	else:
		value = 'NOT Mirrored'
	param = door.LookupParameter('Comments')
	param.Set(value)	

# End Revit Transaction
TransactionManager.Instance.TransactionTaskDone()

# Assign output to the OUT variable.
OUT = mirrored_doors