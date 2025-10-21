"""
Family.Category
--------------
Get the category of the family.
"""
__author__ = "Marco Barboza"


import clr

clr.AddReference("RevitNodes")
import Revit
clr.ImportExtensions(Revit.Elements)

clr.AddReference("RevitAPI")
import Autodesk
from Autodesk.Revit.DB import Family


def get_dynamo_category(category) -> Revit.Elements.Category:
    """
    Retrieves a Dynamo category given a Revit category.
    """
    return Revit.Elements.Category.ById(category.Id.Value)


families = UnwrapElement(IN[0]) if isinstance(IN[0], list) else [UnwrapElement(IN[0])]
family_categories = [family.FamilyCategory for family in families]
dynamo_categories = []
unavailable = []

for category in family_categories:
    try:
        dynamo_category = get_dynamo_category(category)
        dynamo_categories.append(dynamo_category)
    except Exception as e:
        dynamo_categories.append(None)
        if category.Name not in unavailable:
            unavailable.append(category.Name)
    
OUT = {"Category": dynamo_categories, "Unavailable in Dynamo": unavailable}