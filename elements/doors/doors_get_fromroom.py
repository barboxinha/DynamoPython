"""
Doors.FromRoom
--------------
Get the room that the door is hosted in.
"""
__author__ = "Marco Barboza"


import clr

clr.AddReference("RevitNodes")
import Revit
clr.ImportExtensions(Revit.Elements)

clr.AddReference("RevitAPI")
import Autodesk
from Autodesk.Revit.DB import FamilyInstance


def get_from_room(family_instance: FamilyInstance):
    """
    Get the room that the Door or Window is hosted in.
    """
    if not isinstance(family_instance, FamilyInstance) or family_instance.Category.Name not in ["Doors", "Windows"]:
        raise TypeError("Input must be a FamilyInstance representing a door or window.")
    
    from_room = family_instance.FromRoom
    if from_room:
        return from_room
    
    return None


doors = UnwrapElement(IN[0]) if isinstance(IN[0], list) else [UnwrapElement(IN[0])]

if IN[0]:
    try:
        from_rooms = [get_from_room(door) for door in doors]
        OUT = from_rooms if len(from_rooms) > 1 else from_rooms[0]
    except Exception as e:
        import traceback
        OUT = traceback.format_exc()
else:
    OUT = None