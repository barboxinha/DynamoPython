"""
View.IsCropBoxActive
--------------------
Checks if the crop box is active for a given list of Revit views.
"""


import clr

clr.AddReference("ProtoGeometry")
from Autodesk.DesignScript.Geometry import *

clr.AddReference("RevitNodes")
import Revit
clr.ImportExtensions(Revit.GeometryConversion)

clr.AddReference("RevitAPI")
import Autodesk
from Autodesk.Revit.DB import View, ViewCropRegionShapeManager


views = UnwrapElement(IN[0]) if isinstance(IN[0], list) else [UnwrapElement(IN[0])]

is_active = []

for view in views:
	region = view.GetCropRegionShapeManager().GetCropShape()
	is_active.append(len(region) > 0)

OUT = is_active