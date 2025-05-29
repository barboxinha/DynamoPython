"""
Category.DynamoTypeByName
---------------
Attempts to retrieve a Dynamo category by its Revit category name.
"""
__author__ = "Marco Barboza"


import sys
import clr

clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *

clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import Categories, Category

clr.AddReference("RevitNodes")
import Revit
clr.ImportExtensions(Revit.Elements)

clr.AddReference("RevitServices")
from RevitServices.Transactions import TransactionManager
from RevitServices.Persistence import DocumentManager


def get_dynamo_category_by_name(doc, category_name):
    """
    Attempts to retrieve a Dynamo category by its Revit category name.
    """
    categories = doc.Settings.Categories
    category = None
    
    try:
        for cat in categories:
            if cat.Name == category_name:
                category = Revit.Elements.Category.ById(cat.Id.IntegerValue)
                break
        
        if category == None:
            category = "There is no category with that name."
    except Exception as e:
        category = str(e)
            
    return category


doc = DocumentManager.Instance.CurrentDBDocument

OUT = get_dynamo_category_by_name(doc, IN[0])