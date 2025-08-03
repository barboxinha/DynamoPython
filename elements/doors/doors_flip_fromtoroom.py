"""
Doors.FlipFromToRoom
--------------------
Flip the Door or Window instance's From/To Room properties.
"""
__author__ = "Marco Barboza"


import clr

clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

clr.AddReference("RevitAPI")
import Autodesk
from Autodesk.Revit.DB import FamilyInstance


def flip_from_to_room(family_instance: FamilyInstance):
    """
    Flip the Door or Window instance's From/To Room properties.
    """
    if not isinstance(family_instance, FamilyInstance) or family_instance.Category.Name not in ["Doors", "Windows"]:
        raise TypeError("Input must be a FamilyInstance representing a door or window.")
    
    if family_instance:
        family_instance.FlipFromToRoom()


doc = DocumentManager.Instance.CurrentDBDocument

doors = UnwrapElement(IN[0]) if isinstance(IN[0], list) else [UnwrapElement(IN[0])]

# Flip From/To Room for each door
if IN[0]:
    try:
        TransactionManager.Instance.EnsureInTransaction(doc)
        for door in doors:
            flip_from_to_room(door)     
        TransactionManager.Instance.TransactionTaskDone()
        OUT = doors
    except Exception as e:
        import traceback
        OUT = traceback.format_exc()
else:
    OUT = None