"""
GraphicsStyle.ByName
-------------------------
Retrieves all graphics styles in the current Revit document and 
allows the user to select one by name.
"""
__author__ = "Marco Barboza"


import clr

clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *

clr.AddReference("RevitNodes")
import Revit
clr.ImportExtensions(Revit.Elements)
clr.ImportExtensions(Revit.GeometryConversion)

clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager

clr.AddReference("RevitAPI")
clr.AddReference("RevitAPIUI")
import Autodesk 
from Autodesk.Revit.DB import *
from Autodesk.Revit.UI import *


doc = DocumentManager.Instance.CurrentDBDocument

# Filter GraphicsStyle elements
all_graphicsstyles = FilteredElementCollector(doc).OfClass(GraphicsStyle).ToElements()
all_graphicsstyle_names = []

for gs in all_graphicsstyles:
	gs_name = gs.Name
	gs_type = gs.GraphicsStyleType.ToString()
	if gs_type == "Projection":
		all_graphicsstyle_names.append(gs_name)
	
graphicsstyle_index = all_graphicsstyle_names.IndexOf(IN[0])
output_graphicsstyle = all_graphicsstyles[graphicsstyle_index]
graphicsstyle_id = output_graphicsstyle.Id

OUT = output_graphicsstyle