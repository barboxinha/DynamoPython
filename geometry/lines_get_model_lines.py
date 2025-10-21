"""
Line.GetModelLines
------------------
Retrieves model line instances from a document.
"""
__author__ = "Marco Barboza"


import clr

clr.AddReference("RevitNodes")
import Revit
clr.ImportExtensions(Revit.Elements)

clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager

clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import FilteredElementCollector, CurveElementFilter, CurveElementType


def get_model_lines(doc) -> list:
    """
    Retrieves all model line instances from the given document.
    """
    return FilteredElementCollector(doc).WherePasses(CurveElementFilter(CurveElementType.ModelCurve)).ToElements()


doc = DocumentManager.Instance.CurrentDBDocument

OUT = get_model_lines(doc)