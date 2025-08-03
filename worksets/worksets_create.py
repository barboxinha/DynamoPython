"""
Worksets.Create
----------------
Creates new worksets in a Revit document based on a list of names provided as input.
"""

import clr

clr.AddReference('RevitAPI')
from Autodesk.Revit import DB
from Autodesk.Revit.DB.Structure import *

clr.AddReference('RevitAPIUI')
from Autodesk.Revit.UI import *

clr.AddReference('System')
from System.Collections.Generic import List

clr.AddReference('RevitNodes')
import Revit
clr.ImportExtensions(Revit.GeometryConversion)
clr.ImportExtensions(Revit.Elements)

clr.AddReference('RevitServices')
import RevitServices
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager


doc = DocumentManager.Instance.CurrentDBDocument


def create_worksets(d, names):
	"""Creates new worksets in the Revit document based on the provided names."""
	new_Worksets = []
	doc_Worksets = DB.FilteredWorksetCollector(d).OfKind(DB.WorksetKind.UserWorkset).ToWorksets()
	doc_ws_Names = [workset.Name for workset in doc_Worksets]
	for name in names:
		if name not in doc_ws_Names:
			ws = DB.Workset.Create(d, name)
			new_Worksets.append(ws)
	return new_Worksets


workset_names = IN[0]

TransactionManager.Instance.EnsureInTransaction(doc)

OUT = create_worksets(doc, workset_names)

TransactionManager.Instance.TransactionTaskDone()