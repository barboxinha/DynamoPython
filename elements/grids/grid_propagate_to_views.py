"""
Grid.PropagateToViews
---------------------
Propagates the extents applied to this datum in the view to the specified parallel views.
"""
__author__ = "Marco Barboza"


import clr
import System

# Load System.Core assembly that contains HashSet for ISet
clr.AddReference("System.Core")
from System.Collections.Generic import HashSet

clr.AddReference("ProtoGeometry")
from Autodesk.DesignScript.Geometry import *

clr.AddReference("RevitNodes")
import Revit
clr.ImportExtensions(Revit.GeometryConversion)
clr.ImportExtensions(Revit.Elements)

clr.AddReference("RevitServices")
import RevitServices
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

clr.AddReference("RevitAPI")
import Autodesk
from Autodesk.Revit.DB import Grid, ElementId, View


doc = DocumentManager.Instance.CurrentDBDocument

grids = UnwrapElement(IN[0]) if isinstance(IN[0], list) else [UnwrapElement(IN[0])]
ref_view = UnwrapElement(IN[1])
prop_views = UnwrapElement(IN[2]) if isinstance(IN[2], list) else [UnwrapElement(IN[2])]

if prop_views:
	try:
		grid_names = []
		valid_ids = []
		success_views = []
	
		TransactionManager.Instance.EnsureInTransaction(doc)
		
		p_view_ids = [v.Id for v in prop_views]
		valid_views = []
		invalid_views = []
		
		for g in grids:
			# Get candidate propagation views
			view_ids = [id.Value for id in g.GetPropagationViews(ref_view)]
			val_views = []
			inv_views = []
			
			# Check input views are fit for propagation
			parallel_views = HashSet[ElementId]()
			
			for pv_id in p_view_ids:
				if pv_id.Value in view_ids:
					parallel_views.Add(pv_id)
					val_views.append(doc.GetElement(pv_id))
					if pv_id.Value in valid_ids:
						pass
					else:
						valid_ids.append(pv_id.Value)
						success_views.append(doc.GetElement(pv_id))
				else:
					inv_views.append(doc.GetElement(pv_id))
			
			# Propagate grid extents to valid views
			if val_views:
				g.PropagateToViews(ref_view, parallel_views)
				valid_views.append(val_views)
			
			if inv_views:
				invalid_views.append(inv_views)
			
			grid_names.append(g.Name)
		
		TransactionManager.Instance.TransactionTaskDone()
		
		output = ""
		
		if success_views:
			view_list = ["**{} : {}".format(p_view.ViewType, p_view.Name) for p_view in success_views]
			output = "Grids '{}' in '{} : {}' propagated to:\n\t{}".format(", ".join(grid_names), ref_view.ViewType, ref_view.Name, "\n\t".join(view_list))
		
		if invalid_views:
			inv_view_list = []
			for i in range(len(invalid_views)):
				iv_lst = []
				for j in invalid_views[i]:
					iv_lst.append("**{} : {}".format(j.ViewType, j.Name))
				
				inv_view_list.append("Could not propagate Grid '{}' to:\n\t{}".format(grid_names[i], "\n\t".join(iv_lst)))
			
			inv_output = "\n\n-----\n!!! Try uncropping the following views !!!\n\n{}".format("\n".join(inv_view_list))
			output += inv_output
		
		OUT = output, success_views	
	except Autodesk.Revit.Exceptions.ArgumentException as ae:
		OUT = ae.Message, "Tip: Try uncropping the parallel views first."
	except Exception as e:
		import traceback
		OUT = traceback.format_exc()
else:
	OUT = "There are no views to propagate grids to."