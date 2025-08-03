"""
View3D.SetSectionBox
--------------------
Sets the section box for a given View3D in Revit.
Takes a View3D element and a BoundingBox as inputs, and applies the section box
"""
__author__ = "Marco Barboza"


import clr

clr.AddReference("ProtoGeometry")
from Autodesk.DesignScript.Geometry import *

clr.AddReference("RevitNodes")
import Revit
clr.ImportExtensions(Revit.GeometryConversion)
clr.ImportExtensions(Revit.Elements)

clr.AddReference("RevitAPI")
import Autodesk
from Autodesk.Revit.DB import BoundingBoxXYZ, View3D, XYZ

clr.AddReference("RevitServices")
import RevitServices
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager


# Create View3D SectionBox function
def set_view3d_sectionbox(view3D, bBox):
	"""Set the section box for a given View3D element."""
	# Rebuild BoundingBox and assign to View3D
	new_max = bBox.MaxPoint.ToRevitType()
	new_min = bBox.MinPoint.ToRevitType()
	new_bbox = BoundingBoxXYZ()
	new_bbox.Max = new_max
	new_bbox.Min = new_min
	view3D.SetSectionBox(new_bbox)
	
	return view3D


doc = DocumentManager.Instance.CurrentDBDocument

# Ensure inputs are list format
view3d = UnwrapElement(IN[0]) if isinstance(IN[0], list) else [UnwrapElement(IN[0])]
bbox = IN[1] if isinstance(IN[1], list) else [IN[1]]

view = []

TransactionManager.Instance.EnsureInTransaction(doc)

for i in range(len(view3d)):
	try:
		sbox_view = set_view3d_sectionbox(view3d[i], bbox[i])
		view.append(sbox_view)
	except Exception as e:
		view.append("Error: {}".format(str(e)))

TransactionManager.Instance.TransactionTaskDone()

OUT = view