"""
Prompting UI Selection
----------------------
User-Selection Workflows
Revit's Selection class can be used to read the user's currently-selected elements
in the active Revit document, or to prompt the user to select via various methods (by click or by dragging a rectangle).
"""

# The ISelectionFilter Interface can be implemented to restrict the kinds of elements a user can select, using any kind of coded logic.
# For this, create a new class which implements the interface.
# Example code needed to prompt a user to select (only) Walls:

import clr
clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager

clr.AddReference("RevitAPIUI")
#Import the below namespace to get access to the ISelectionFilter interface
from Autodesk.Revit.UI.Selection import *


# Get the active UIDocument
uiapp = DocumentManager.Instance.CurrentUIApplication
uidoc = uiapp.ActiveUIDocument


# Define a custom selection filter class that implements the ISelectionFilter interface.
# This class will allow only Walls to be selected.
class MySelectionFilter(ISelectionFilter):
	def __init__(self):
		pass
	def AllowElement(self, element):
		if element.Category.Name == "Walls":
			return True
		else:
			return False
			

# Instantiate the selection filter class created above.
# This will be used to filter the selection of elements.
selection_filter = MySelectionFilter()

walls = uidoc.Selection.PickElementsByRectangle(selection_filter)

OUT = walls

"""
The ISelectionFilter interface has an __init__ method, like any other Python class, 
and two methods called AllowElement() and AllowReference(). 
The AllowElement() method can be used to define custom logic, returning True when an element meets your criteria. 
The AllowReference() method can be used to return geometry references, such as edges and faces and, again, it can be built to return True or False as desired.
"""
