"""
Titleblock.Sheet
----------------
Gets the sheet views associated with a list of titleblocks in a Revit document.
"""
__author__ = "Marco Barboza"


import sys
import clr

clr.AddReference("RevitNodes")
import Revit
clr.ImportExtensions(Revit.Elements)

clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager

clr.AddReference("RevitAPI")
import Autodesk.Revit.DB as DB


def get_titleblock_view(active_doc, _titleblock):
    """Gets the Titleblock sheet view."""
    view_id = _titleblock.OwnerViewId
    return active_doc.GetElement(view_id)


doc = DocumentManager.Instance.CurrentDBDocument

titleblocks = UnwrapElement(IN[0]) if isinstance(IN[0], list) else [UnwrapElement(IN[0])]
sheets = []

for tb in titleblocks:
	tb_sheet = get_titleblock_view(doc, tb)
	sheets.append(tb_sheet)

OUT = sheets