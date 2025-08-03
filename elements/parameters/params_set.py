"""
Parameter.Set
-------------
Set the value of a parameter for a list of elements in Revit.
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

elements = UnwrapElement(IN[0]) if isinstance(IN[0], list) else [UnwrapElement(IN[0])]
parameter = IN[1] # Parameter Name string
parameter_set = IN[2]

out_list = []

TransactionManager.Instance.EnsureInTransaction(doc)

for element in elements:
    p = element.LookupParameter(parameter)
    p_set = p.Set(parameter_set)
    out_list.append(p_set.AsString())

TransactionManager.Instance.TransactionTaskDone()

OUT = out_list
