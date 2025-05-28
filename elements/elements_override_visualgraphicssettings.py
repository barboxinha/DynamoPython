"""
Elements.OverrideGraphicSettings
--------------------------------
Overrides the given elements' visual graphic settings.
"""


import clr

clr.AddReference("ProtoGeometry")
from Autodesk.DesignScript.Geometry import *

clr.AddReference("RevitNodes")
import Revit
clr.ImportExtensions(Revit.Elements)

clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

clr.AddReference("RevitAPI")
import Autodesk
from Autodesk.Revit.DB import *


def ConvertColor(dynamo_color):
    """
    Converts a Dynamo color to a Revit color.
    """
    return Autodesk.Revit.DB.Color(dynamo_color.Red, dynamo_color.Green, dynamo_color.Blue)


def OverrideElement(element, color, fill):
    """
    Overrides the visual graphic settings of a Revit element.
    """
    ogs = OverrideGraphicSettings()
    ogs.SetProjectionFillColor(color)
    ogs.SetProjectionFillPatternId(fill.Id)
    ogs.SetCutFillColor(color)
    ogs.SetCutFillPatternId(fill.Id)
    doc.ActiveView.SetElementOverrides(element.Id, ogs)


doc = DocumentManager.Instance.CurrentDBDocument

elements = UnwrapElement(IN[0]) if isinstance(IN[0], list) else [UnwrapElement(IN[0])]
color = ConvertColor(IN[1])
fill_pattern = UnwrapElement(IN[2])

for e in elements:
    TransactionManager.Instance.EnsureInTransaction(doc)
    OverrideElement(e, color, fill_pattern)
    TransactionManager.Instance.TransactionTaskDone()

OUT = elements