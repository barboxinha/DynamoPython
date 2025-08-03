"""
View.SetCustomScaleDisplayName
------------------------------
Sets the custom scale display name for Revit views.
"""
__author__ = "Marco Barboza"


import clr

clr.AddReference("ProtoGeometry")
from Autodesk.DesignScript.Geometry import *

clr.AddReference("RevitNodes")
import Revit
clr.ImportExtensions(Revit.Elements)

clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import View, Viewport, BuiltInParameter

clr.AddReference("RevitServices")
import RevitServices
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager


doc = DocumentManager.Instance.CurrentDBDocument

views = UnwrapElement(IN[0]) if isinstance(IN[0], list) else [UnwrapElement(IN[0])]
custom_scale_name = IN[1]
display_name = IN[2]

TransactionManager.Instance.EnsureInTransaction(doc)

for view in views:
	custom_name_param = view.get_Parameter(BuiltInParameter.VIEW_SCALE_CUSTOMNAME)
	custom_name_param.Set(custom_scale_name)
	display_name_param = view.get_Parameter(BuiltInParameter.VIEW_SCALE_HAVENAME)
	display_name_param.Set(display_name)
	
TransactionManager.Instance.TransactionTaskDone()

OUT = views