"""
Views.GetCustomScaleName
------------------------
Retrieves the custom scale names of Revit views.
"""
__author__ = "Marco Barboza"


import clr

clr.AddReference("ProtoGeometry")
from Autodesk.DesignScript.Geometry import *

clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import View, Viewport, BuiltInParameter


views = UnwrapElement(IN[0]) if isinstance(IN[0], list) else [UnwrapElement(IN[0])]
custom_scale_names = [view.get_Parameter(BuiltInParameter.VIEW_SCALE_CUSTOMNAME).AsString() for view in views]

OUT = custom_scale_names
