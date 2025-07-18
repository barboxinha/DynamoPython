"""
View.SetCropBoxCurves
---------------------
Allows you to set the crop box curves of a view.
"""


import clr
import System

clr.AddReference("ProtoGeometry")
from Autodesk.DesignScript.Geometry import *

clr.AddReference("RevitAPI")
import Autodesk.Revit.DB

clr.AddReference("RevitNodes")
import Revit
# Import ToProtoType, ToRevitType geometry conversion extension methods
clr.ImportExtensions(Revit.GeometryConversion)
clr.ImportExtensions(Revit.Elements)

clr.AddReference("DSCoreNodes")
import DSCore
from DSCore import *

clr.AddReference("RevitServices")
import RevitServices
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager


doc = DocumentManager.Instance.CurrentDBDocument

views = UnwrapElement(IN[0]) if isinstance(IN[0], list) else [UnwrapElement(IN[0])]
listout = []

if isinstance(IN[1], list):
    if isinstance(IN[1][0], list):
        if IN[1][0][0].GetType() == PolyCurve:
            curves = [[PolyCurve.Curves(x) for x in y] for y in IN[1]]
        else:
            curves = IN[1]
    elif IN[1][0].GetType() == PolyCurve:
        curves = [PolyCurve.Curves(x) for x in IN[1]]
    elif IN[1][0].GetType() == Curve or IN[1][0].GetType() == Line:
        curves = List.OfRepeatedItem(IN[1],len(views))
    else:
        curves = IN[1]
else:
    if IN[1].GetType() == PolyCurve:
        curves = [PolyCurve.Curves(IN[1])]
    else:
        curves = [IN[1]]

try:
    TransactionManager.Instance.EnsureInTransaction(doc)
    
    for view,curve in zip(views,curves):
        regionMan = view.GetCropRegionShapeManager()
        revit_curve = [c.ToRevitType() for c in curve]
        curveloop = Autodesk.Revit.DB.CurveLoop()
        for c in revit_curve:
            curveloop.Append(c)
        if view.CropBoxActive == False:
            view.CropBoxActive = True
            view.CropBoxVisible = True
        regionMan.SetCropShape(curveloop)
        listout.append(view)
        
    TransactionManager.Instance.TransactionTaskDone()
except:
    import traceback
    listout = traceback.format_exc()

OUT = listout
