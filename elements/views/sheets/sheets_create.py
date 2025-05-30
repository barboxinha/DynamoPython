"""
Sheets.Create
-------------
Creates new sheets in the Revit document.
The sheets will be created with the specified title block, name, and number.
"""

import clr

clr.AddReference("RevitNodes")
import Revit
clr.ImportExtensions(Revit.Elements)

clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

clr.AddReference("RevitAPI")
import Autodesk
from Autodesk.Revit.DB import *


doc = DocumentManager.Instance.CurrentDBDocument

sheet_names = IN[0]
sheet_numbers = IN[1]
titleblock = UnwrapElement(IN[2])
is_placeholder = IN[3]
sheet_list = list()

TransactionManager.Instance.EnsureInTransaction(doc)

for num in range(len(sheet_numbers)):
    new_sheet = ViewSheet.Create(doc, titleblock.Id)
    new_sheet.Name = sheet_names[num]
    new_sheet.SheetNumber = sheet_numbers[num]
    new_sheet.IsPlaceholder = is_placeholder
    sheet_list.append(new_sheet.ToDSType(False))

TransactionManager.Instance.TransactionTaskDone()

OUT = sheet_list