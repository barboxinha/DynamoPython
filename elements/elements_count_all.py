"""
Elements.CountAll
-----------------
Counts ALL Elements in the Revit Model
"""

import clr

clr.AddReference('RevitNodes')
import Revit
clr.ImportExtensions(Revit.Elements)

clr.AddReference('RevitServices')
from RevitServices.Persistence import DocumentManager

clr.AddReference('RevitAPI')
from Autodesk.Revit.DB import FilteredElementCollector


# Get current Revit document
doc = DocumentManager.Instance.CurrentDBDocument

count = 0

#Get ALL Revit elements within the model
fec = FilteredElementCollector(doc).WhereElementIsNotElementType().ToElementIds()

count = len(fec)

OUT = count