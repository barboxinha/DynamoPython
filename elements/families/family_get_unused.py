"""
Family.GetUnused
--------------
Get the unused families in the document.
"""
__author__ = "Marco Barboza"


import clr

clr.AddReference("RevitNodes")
import Revit
clr.ImportExtensions(Revit.Elements)

clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager

clr.AddReference("RevitAPI")
import Autodesk
from Autodesk.Revit.DB import Family, FamilyInstance, FilteredElementCollector


def get_unused_families(doc) -> list:
    """
    Get the unused families in the document.
    """
    all_families = FilteredElementCollector(doc).OfClass(Family).ToElements()
    family_instances = FilteredElementCollector(doc).OfClass(FamilyInstance).WhereElementIsNotElementType().ToElements()
    unused_families = []

    for family in all_families:
        # Check if the family has any instances in the document
        if not any(instance.Symbol.Family.Id == family.Id for instance in family_instances):
            unused_families.append(family)

    return unused_families


doc = DocumentManager.Instance.CurrentDBDocument

unused_families = get_unused_families(doc)

OUT = unused_families if len(unused_families) > 1 else (unused_families[0] if unused_families else None)