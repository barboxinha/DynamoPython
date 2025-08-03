"""
Line.CreateRoomSeparations
--------------------------
Creates room separation lines from a list of curves, a view, and a sketch plane.
"""


import clr
clr.AddReference('RevitAPI')
from Autodesk.Revit.DB import *

clr.AddReference("RevitNodes")
import Revit
clr.ImportExtensions(Revit.GeometryConversion)

clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager


doc = DocumentManager.Instance.CurrentDBDocument

curves = UnwrapElement(IN[0]) if isinstance(IN[0], list) else [UnwrapElement(IN[0])]
sketch_plane = UnwrapElement(IN[1])
view = UnwrapElement(IN[2])

TransactionManager.Instance.EnsureInTransaction(doc)

curve_array = CurveArray()

for curve in curves:
	curve_array.Append(curve.ToRevitType())

doc_creation = doc.Create
separator_array = doc_creation.NewRoomBoundaryLines(sketch_plane, curve_array, view)

TransactionManager.Instance.TransactionTaskDone()

room_boundaries = []

for line in separator_array:
	room_boundaries.append(line)

OUT = room_boundaries