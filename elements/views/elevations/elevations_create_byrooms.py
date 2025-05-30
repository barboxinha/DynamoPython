"""
Elevations.CreateByRooms
-- 
Create elevation views given placement point, rotation angles, view type, and count.
"""
__author__ = "Marco Barboza"


import sys
import clr
import math

clr.AddReference("RevitNodes")
import Revit
clr.ImportExtensions(Revit.GeometryConversion)

clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

clr.AddReference("RevitAPI")
import Autodesk.Revit.DB as DB
from Autodesk.Revit.DB import ElementType, XYZ, Line, ElevationMarker, View


doc = DocumentManager.Instance.CurrentDBDocument

# Inputs: boolean toggle, ElevationMarker points, ElevationMarker rotation angles, elevation ViewType, 1-4 integer count
toggle = IN[0]
points = UnwrapElement(IN[1])
rot_angles = [math.radians(a) for a in IN[2]]
view_type = UnwrapElement(IN[3])
view_count = IN[4]

if toggle:
	try:
		views_lst = []
		
		TransactionManager.Instance.EnsureInTransaction(doc)
		
		for ind, point in enumerate(points):
						
			# Create Z-Axis line for elevation marker to rotate around.		
			ele_marker_pt = point.ToXyz()
			ele_rotate_pt = XYZ(ele_marker_pt.X, ele_marker_pt.Y, ele_marker_pt.Z+1) #Imperial Units, for metric units add integer > 10 to pt.Z
			axis = Line.CreateBound(ele_marker_pt, ele_rotate_pt)
	
			# Create Elevation Marker and Elevation Views.
			ele_marker = ElevationMarker.CreateElevationMarker(doc, view_type.Id, ele_marker_pt, 100)
			ele_views = []
			for e in range(view_count):
				ele = ele_marker.CreateElevation(doc, doc.ActiveView.Id, e)
				ele_views.append(ele)
				
			# Rotate Elevation Marker (Important! Views need to exist for Marker to be able to rotate).
			DB.ElementTransformUtils.RotateElement(doc, ele_marker.Id, axis, rot_angles[ind])
			views_lst.append(ele_views)
	
		TransactionManager.Instance.TransactionTaskDone()
		
		OUT = views_lst
	
	except Exception as e:
		import traceback
		OUT = traceback.format_exc()	
else:
	OUT = "Set toggle to TRUE"