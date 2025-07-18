"""
ViewFamily.GetViewFamilyTypeAndNames
------------------------------
Retrieves all ViewFamilyType elements of a given type from the current Revit document
and extracts their names.
"""
__author__ = "Marco Barboza"


import clr

clr.AddReference("RevitNodes")
import Revit
clr.ImportExtensions(Revit.GeometryConversion)

clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager

clr.AddReference("RevitAPI")
import Autodesk
from Autodesk.Revit.DB import *


doc = DocumentManager.Instance.CurrentDBDocument

view_family_types = []
type_names = []

# Get ViewFamilyType
collector = FilteredElementCollector(doc).OfClass(ViewFamilyType).ToElements()

# Get ViewFamilyType Names
for vft in collector:
	if vft.ViewFamily == ViewFamily.Elevation: # Switch to whatever view family you need
		view_family_types.append(vft)
		for param in vft.Parameters:
			if param.Definition.Name == "Type Name":
				type_names.append(param.AsString())
				break

OUT = view_family_types, type_names
