"""
Elements.Isolate
----------------
Isolates elements in the active view of a Revit document.
"""
__author__ = "Marco Barboza"


import sys
import clr

clr.AddReference("RevitNodes")
import Revit
clr.ImportExtensions(Revit.Elements)
clr.ImportExtensions(Revit.GeometryConversion)

clr.AddReference('RevitServices')
import RevitServices
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

clr.AddReference('RevitAPI')
import Autodesk
from Autodesk.Revit.DB import *

import System
from System.Collections.Generic import *


doc = DocumentManager.Instance.CurrentDBDocument

# Collect all elements of your preference (class or category) in Active View
active_view_elems = FilteredElementCollector(doc, doc.ActiveView.Id).OfClass(Wall).ToElements()
elements = UnwrapElement(active_view_elems)
view = UnwrapElement(doc.ActiveView)
ids = [e.Id for e in elements]
id_elements = List[ElementId](ids)

TransactionManager.Instance.EnsureInTransaction(doc)

# Isolate elements with .IsolateElementsTemporary(ElementId) method
view.IsolateElementsTemporary(id_elements)

TransactionManager.Instance.TransactionTaskDone()

OUT = elements