"""
Grid.GetPropagationViews
------------------------
Retrieves a list of candidate views that are parallel to the current view and to which the extents of the datum may be propagated.
It is used to prepare the input for the `Grid.PropagateToViews` method.
"""
__author__ = "Marco Barboza"


import clr

clr.AddReference("ProtoGeometry")
from Autodesk.DesignScript.Geometry import *

clr.AddReference("RevitNodes")
import Revit
clr.ImportExtensions(Revit.GeometryConversion)
clr.ImportExtensions(Revit.Elements)

clr.AddReference("RevitServices")
import RevitServices
from RevitServices.Persistence import DocumentManager

clr.AddReference("RevitAPI")
import Autodesk
from Autodesk.Revit.DB import Grid, View


doc = DocumentManager.Instance.CurrentDBDocument

grids = UnwrapElement(IN[0]) if isinstance(IN[0], list) else [UnwrapElement(IN[0])]
view = UnwrapElement(IN[1])

prop_views = []

for g in grids:
	view_ids = g.GetPropagationViews(view)
	views = [doc.GetElement(id) for id in view_ids]
	prop_views.append(views)

OUT = prop_views