"""
Elements.Rotate
---------------
Rotates selected elements in Revit by a specified angle around their reference point.
"""

import clr
import math

clr.AddReference("RevitNodes")
import Revit
clr.ImportExtensions(Revit.Elements)
clr.ImportExtensions(Revit.GeometryConversion)

clr.AddReference('RevitAPI')
from Autodesk.Revit.DB import *

clr.AddReference('RevitServices')
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager


doc = DocumentManager.Instance.CurrentDBDocument

# Input selected elements, rotation angle
elements = UnwrapElement(IN[0]) if isinstance(IN[0], list) else [UnwrapElement(IN[0])]
angle = math.radians(IN[1])

TransactionManager.Instance.EnsureInTransaction(doc)

for e in elements:
    ref_location = e.Location.Point
    rot_axis = Line.CreateBound(ref_location, XYZ(ref_location.X, ref_location.Y, ref_location.Z+1))
    ElementTransformUtils.RotateElement(doc, e.Id, rot_axis, angle)

TransactionManager.Instance.TransactionTaskDone()

OUT = elements