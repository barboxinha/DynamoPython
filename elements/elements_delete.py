"""
Elements.Delete
---------------
Deletes the given Revit Elements
"""
__author__ = "Marco Barboza"


import clr

clr.AddReference("RevitNodes")
import Revit
clr.ImportExtensions(Revit.Elements)

clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager


def delete(elements: list) -> list:
    """
    Deletes elements from the Revit DB.
    """
    if not elements or elements is None:
        return elements
    
    deleted_ids = []
    
    doc = DocumentManager.Instance.CurrentDBDocument

    TransactionManager.Instance.EnsureInTransaction(doc)

    for e in elements:
        deleted_ids.append(e.Id.Value)
        doc.Delete(e.Id)

    TransactionManager.Instance.TransactionTaskDone()

    return deleted_ids


elements = UnwrapElement(IN[0]) if isinstance(IN[0], list) else [UnwrapElement(IN[0])]

try:
    OUT = delete(elements)
except Exception:
    import traceback
    OUT = traceback.format_exc()
