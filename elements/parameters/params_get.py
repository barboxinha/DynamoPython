"""
Parameter.Get
-------------
Gets the values of a specified shared parameter from a list of Revit elements.
"""


import clr

clr.AddReference("ProtoGeometry")
from Autodesk.DesignScript.Geometry import *

clr.AddReference("RevitServices")
import RevitServices
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

clr.AddReference("RevitAPI")
clr.AddReference("RevitAPIUI")
from Autodesk.Revit.DB import *


doc = DocumentManager.Instance.CurrentDBDocument
uiapp = DocumentManager.Instance.CurrentUIApplication
app = uiapp.Application

elements = UnwrapElement(IN[0])
parameter = IN[1] # Parameter Name string

out_list = []
family_type = []

for element in elements:
    for p in element.Parameters:
        if p.IsShared and p.Definition.Name == parameter:
            parameter_value = element.get_Parameter(p.GUID)
            out_list.append(parameter_value.AsString())

for element in elements:
    id = element.GetTypeId()
    if id == ElementId.InvalidElementId:
        family_type.append(None)
    else:
        family_type.append(doc.GetElement(id))

builtin_param_type = BuiltInParameter.INSERT_BUILTIN_PARAM #<Enumerated BuiltIn Parameter

for element in UnwrapElement(family_type):
    builtin_param = element.get_Parameter(builtin_param_type)
    out_list.append(builtin_param.AsString())

OUT = out_list
