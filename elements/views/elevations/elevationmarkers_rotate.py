"""
ElevationMarker.Rotate
----------------------
Rotate the elevation marker in the view.
This script rotates the elevation markers in the specified view by a given angle.
"""
__author__ = "Marco Barboza"


import clr
import math

clr.AddReference('RevitAPI')
import Autodesk
from Autodesk.Revit.DB import *

clr.AddReference('RevitNodes')
import Revit
clr.ImportExtensions(Revit.GeometryConversion)
clr.ImportExtensions(Revit.Elements)

clr.AddReference('RevitServices')
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager


doc = DocumentManager.Instance.CurrentDBDocument

elevation_markers = UnwrapElement(IN[0]) if isinstance(IN[0], list) else [UnwrapElement(IN[0])]
rotation_angle = [math.radians(a) for a in IN[1]] # List of angles in degrees
view = UnwrapElement(IN[2]) # Must be a plan view
axis = []

# Build rotation axis for each elevation marker	
for em in elevation_markers:
	bbox = (em.BoundingBox[view])
	diag = Line.CreateBound(bbox.Min,bbox.Max)
	p1 = diag.Evaluate(0.5, True)
	p2 = XYZ(p1.X, p1.Y,p1.Z+1)
	axis_ = Line.CreateBound(p1, p2)
	axis.append(axis_)
	
TransactionManager.Instance.EnsureInTransaction(doc)

elev_markers = []

for elev_marker, axis, rotation_angle in zip(elevation_markers, axis, rotation_angle):
	Autodesk.Revit.DB.ElementTransformUtils.RotateElement(doc, elev_marker.Id, axis, rotation_angle)
	elev_markers.append(elev_marker)
	
TransactionManager.Instance.TransactionTaskDone()

OUT = elev_markers