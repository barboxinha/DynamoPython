"""
AreaBoundary.FromLines
----------------------
Creates area boundary lines from a list of curves, a view, and a sketch plane.
"""
__author__ = "Marco Barboza"


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

curve_lst = []

TransactionManager.Instance.EnsureInTransaction(doc)

doc_creator = doc.Create

for curve in curves:
    area_boundary = doc_creator.NewAreaBoundaryLine(sketch_plane, curve.ToRevitType(), view)
    curve_lst.append(area_boundary)

TransactionManager.Instance.TransactionTaskDone()

OUT = curve_lst