"""
Room.GetRoomAtPoint
-------------------
Retrieves the room at a specified point in Revit, optionally considering a specific phase.
"""
__author__ = "Marco Barboza"


import clr

clr.AddReference('RevitAPI')
from Autodesk.Revit.DB import XYZ, Phase
from Autodesk.Revit.DB.Architecture import Room

clr.AddReference('RevitServices')
from RevitServices.Persistence import DocumentManager


def get_room_at_point(doc, point_xyz, phase=None) -> Room:
    """Gets the room at the given point."""
    return doc.GetRoomAtPoint(point_xyz) if phase is None else doc.GetRoomAtPoint(point_xyz, phase)


doc = DocumentManager.Instance.CurrentDBDocument

points = IN[0] if isinstance(IN[0], list) else [IN[0]]
phase = UnwrapElement(IN[1]) if IN[1] else None

# Convert Dynamo point to Revit XYZ
xyz = [pt.ToXyz() for pt in points]

# Get room at point
rooms = [get_room_at_point(doc, pt, phase) for pt in xyz]

OUT = rooms
