"""
RevisionCloud.Views
-------------------
Get views pertaining to a RevisionCloud element in Revit.
"""
__author__ = "Marco Barboza"


# Import libraries and assemblies
import clr

clr.AddReference("ProtoGeometry")
from Autodesk.DesignScript.Geometry import *

clr.AddReference("RevitServices")
import RevitServices
from RevitServices.Persistence import DocumentManager

clr.AddReference("RevitAPI")
import Autodesk 
from Autodesk.Revit.DB import RevisionCloud, Document, View


# Get element OwnerView and dependent views function
def element_views(document, element):
	"""
	Get the OwnerView and dependent views of a given element.
	"""
	element_views = []

	view_id = element.OwnerViewId
	element_view = document.GetElement(view_id)
	element_views.append(element_view)
	dep_view_id = element_view.GetDependentViewIds()

	if len(dep_view_id) >= 1:
		for i in dep_view_id:
			dep_view = document.GetElement(i)
			element_views.append(dep_view)

	return element_views


# Current document
doc = DocumentManager.Instance.CurrentDBDocument

# Revision Cloud input
revision_clouds = IN[0]

# Get RevisionCloud views
views = []

for i in revision_clouds:
	if isinstance(i, list):
		v_list = []
		for c in UnwrapElement(i):
			v_list.append(element_views(doc, c))
		views.append(v_list)
	else:
		c = UnwrapElement(i)
		views.append(element_views(doc, c))

OUT = views