"""
Elements.FromLink
-----------------
Gets Elements for a given Category from linked Revit Model
"""
__author__ = "Marco Barboza"


import clr

clr.AddReference('RevitAPI')
from Autodesk.Revit.DB import *
from Autodesk.Revit.DB.Structure import *

clr.AddReference('RevitAPIUI')
from Autodesk.Revit.UI import *

clr.AddReference('RevitNodes')
import Revit
clr.ImportExtensions(Revit.GeometryConversion)
clr.ImportExtensions(Revit.Elements)

clr.AddReference('RevitServices')
from RevitServices.Persistence import DocumentManager


doc = DocumentManager.Instance.CurrentDBDocument
uidoc = DocumentManager.Instance.CurrentUIApplication.ActiveUIDocument

# Inputs from Dynamo to Revit
link_instance = UnwrapElement(IN[0])
revit_category = UnwrapElement(IN[1])

link_doc = link_instance.GetLinkDocument()
category_filter = ElementCategoryFilter(revit_category.Id)
link_elements = FilteredElementCollector(link_doc).WherePasses(category_filter).WhereElementIsNotElementType().ToElements()

# Address differing coordinate systems between host and link. 
# Useful for correct element placement / rotation.
host_coord_sys = link_instance.GetTotalTransform().ToCoordinateSystem(True)

OUT = list(link_elements), host_coord_sys