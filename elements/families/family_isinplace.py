"""
Family.IsInPlace
----------------
Checks if a given FamilyType is an in-place family in Revit.
Returns True if the family is in-place, otherwise it returns False.
"""
__author__ = "Marco Barboza"


import clr

clr.AddReference("RevitAPI")
import Autodesk.Revit.DB as DB

clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager


doc = DocumentManager.Instance.CurrentDBDocument

family_type = UnwrapElement(IN[0]) if isinstance(IN[0], list) else [UnwrapElement(IN[0])]
is_in_place = []

# Get Family object from FamilyType
for ft in family_type:
    in_place = False
    if isinstance(ft, int):
        ft = doc.GetElement(DB.ElementId(ft))

    if isinstance(ft, DB.FamilySymbol):
        family = ft.Family
        # Check if Family is modeled in place
        in_place = family.IsInPlace
    elif isinstance(ft, DB.Family):
        # If it's already a Family, check directly
        in_place = ft.IsInPlace
    
    is_in_place.append(in_place)

OUT = is_in_place if len(is_in_place) > 1 else is_in_place[0]