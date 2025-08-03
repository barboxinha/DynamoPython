"""
View.SetElementOverrides
------------------------
Set the visual graphic settings of elements in a given view.
"""
__author__ = "Marco Barboza"


import clr
import System
from System.Collections.Generic import List

clr.AddReference("RevitAPI")
import Autodesk
from Autodesk.Revit.DB import *

clr.AddReference("RevitServices")
import RevitServices
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager


def tolist(obj):
	"""Converts the input into a list if it is not already a list."""
	return obj if isinstance(obj, list) else [obj]


def is_nested_list(lst):
    """
    Check if the given list is a nested list of lists.

    Parameters:
    lst (list): The list to check.

    Returns:
    bool: True if the list is a nested list of lists, False otherwise.
    """
    if not isinstance(lst, list):
        return False
    return all(isinstance(i, list) for i in lst)


# Function by Konrad Sobon, @archilab
def HideElements(view, elements):
	ids = List[ElementId]()
	for e in elements:
		if not e.IsHidden(view) and e.CanBeHidden(view):
			ids.Add(e.Id)
	view.HideElements(ids)
	return None


# Function by Konrad Sobon, @archilab
def UnhideElements(view, elements):
	ids = List[ElementId]()
	for e in elements:
		if e.IsHidden(view):
			ids.Add(e.Id)
	if len(ids) > 0:
		view.UnhideElements(ids)
	return None


doc = DocumentManager.Instance.CurrentDBDocument

views = UnwrapElement(tolist(IN[0]))
elements = UnwrapElement(tolist(IN[1]))
ogs = tolist(IN[2])
hide = IN[3]

TransactionManager.Instance.EnsureInTransaction(doc)

# Account for nested lists of views and elements
if is_nested_list(IN[0]):
    for v, e, o in zip(views, elements, ogs):
        v = UnwrapElement(v)
        for view in v:
            if o:
                result = [view.SetElementOverrides(elem.Id, o) for elem in e]
            if hide: 
                HideElements(view, e)
            elif hide is None:
                pass
            else: 
                UnhideElements(view, e)
else:
    for x in range(len(views)):
        if ogs[0]:
            result = [views[x].SetElementOverrides(e.Id, ogs[x]) for e in elements] if len(ogs) > 1 else [views[x].SetElementOverrides(e.Id, ogs[0]) for e in elements]
        if hide: 
            HideElements(views[x], elements)
        elif hide is None:
            pass
        else: 
            UnhideElements(views[x], elements)

TransactionManager.Instance.TransactionTaskDone()

OUT = views if len(IN[0]) > 1 else views[0]
