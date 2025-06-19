"""
Dimensions.OverrideText
-------------------
Overrides the text of a dimension in Revit.
"""
__author__ = "Marco Barboza"


import clr

clr.AddReference('RevitNodes')
import Revit
clr.ImportExtensions(Revit.Elements)

clr.AddReference('RevitServices')
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

clr.AddReference('RevitAPI')
import Autodesk
from Autodesk.Revit.DB import *


doc = DocumentManager.Instance.CurrentDBDocument

dims = UnwrapElement(IN[0]) if isinstance(IN[0], list) else [UnwrapElement(IN[0])]
override_text = IN[1]

TransactionManager.Instance.EnsureInTransaction(doc)

updated_dims = []

for d in dims:
    d.ValueOverride = override_text
    updated_dims.append(d.ValueOverride)

TransactionManager.Instance.TransactionTaskDone()

OUT = updated_dims