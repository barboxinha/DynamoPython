import clr
# Import RevitAPI Classes
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import * # Replace * with the class you need separated by comma.

clr.AddReference("RevitNodes")
import Revit
# Adds ToDSType (bool) extension method to Wrapped elements. Works only with DB.Element inherited types. 
# ToDSType(Autodesk.Revit.DB.Element ele, bool isRevitOwned). "isRevitOwned" => Whether the returned object should be revit owned or not.
clr.ImportExtensions(Revit.Elements)
# Adds ToProtoType, ToRevitType geometry conversion extension methods to objects
clr.ImportExtensions(Revit.GeometryConversion)

# Import DocumentManager and TransactionManager
clr.AddReference("RevitServices")
from RevitServices.Transactions import TransactionManager
from RevitServices.Persistence import DocumentManager

# Create variable for Revit Document
doc = DocumentManager.Instance.CurrentDBDocument

# Start Transaction
TransactionManager.Instance.EnsureInTransaction(doc)

# Code that modifies Revit Database goes here!

# End Transaction
TransactionManager.Instance.TransactionTaskDone()

# Script output
OUT = None