"""
Sheets.Titleblock
-----------------
Gets the Titleblock element of a given Sheet element.
"""

import sys
import clr

clr.AddReference("RevitNodes")
import Revit
clr.ImportExtensions(Revit.Elements)

clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager

clr.AddReference("RevitAPI")
import Autodesk.Revit.DB as DB


def get_view_titleblock(active_doc, source_view):
    """Gets the Sheet Titleblock element."""
    if source_view.ViewType != DB.ViewType.DrawingSheet:
        return None

    view_titleblock = DB.FilteredElementCollector(active_doc, source_view.Id)\
                      .OfCategory(DB.BuiltInCategory.OST_TitleBlocks)\
                      .FirstElement()
    
    return view_titleblock


doc = DocumentManager.Instance.CurrentDBDocument

sheets = UnwrapElement(IN[0]) if isinstance(IN[0], list) else [UnwrapElement(IN[0])]
titleblocks = []

if isinstance(sheets[0], DB.ViewSheet):
    for sheet in sheets:
        tb = get_view_titleblock(doc, sheet)
        titleblocks.append(tb)
    
    OUT = titleblocks
else:
    OUT = "Please input Sheet elements."