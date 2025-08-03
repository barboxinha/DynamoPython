"""
Section.Rotate
--------------
Rotates a list of section views by a specified angle around their centerline.
"""


import clr
import math

clr.AddReference("RevitAPI")
import Autodesk
from Autodesk.Revit.DB import *

clr.AddReference("RevitServices")
import RevitServices
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager


doc = DocumentManager.Instance.CurrentDBDocument

# Selected Element
sections = UnwrapElement(IN[0]) if isinstance(IN[0], list) else [UnwrapElement(IN[0])]
angle = math.radians(IN[1])
view = UnwrapElement(IN[2])

TransactionManager.Instance.EnsureInTransaction(doc)

for section in sections:
    bbox = section.BoundingBox[view]
    diag = Line.CreateBound(bbox.Min, bbox.Max)
    p1 = diag.Evaluate(0.5, True)
    p2 = XYZ(p1.X, p1.Y, p1.Z+1)
    axis_ = Line.CreateBound(p1, p2)
    ElementTransformUtils.RotateElement(doc, section.Id, axis_, angle)

TransactionManager.Instance.TransactionTaskDone()

OUT = sections
