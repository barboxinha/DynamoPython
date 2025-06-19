"""
Family.SetType
--------------
Sets the type of a family instance in Revit.
"""


import clr

clr.AddReference('RevitNodes')
import Revit
clr.ImportExtensions(Revit.Elements)

clr.AddReference('RevitAPI')
import Autodesk
from Autodesk.Revit.DB import *

clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager


doc = DocumentManager.Instance.CurrentDBDocument

family_instance = UnwrapElement(IN[0]) if isinstance(IN[0], list) else [UnwrapElement(IN[0])]
family_type = UnwrapElement(IN[1])

new_family_instance = []
count = 0

TransactionManager.Instance.EnsureInTransaction(doc)

for instance in family_instance:
    instance.Symbol = family_type
    new_family_instance.append(instance)
    count += 1

TransactionManager.TransactionTaskDone()

OUT = new_family_instance