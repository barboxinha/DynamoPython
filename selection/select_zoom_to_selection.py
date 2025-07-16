"""
Select.ZoomToSelection
----------------------
Isolates the selected linked elements in the current view (if it's a 3D view) or creates a new 3D view and zooms to fit.
"""


import clr

clr.AddReference("RevitAPI")
import Autodesk
from Autodesk.Revit.DB import *

clr.AddReference("RevitAPIUI")
from Autodesk.Revit.UI import *
from Autodesk.Revit.UI.Selection import *

clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager


doc = DocumentManager.Instance.CurrentDBDocument
uidoc = DocumentManager.Instance.CurrentUIApplication.ActiveUIDocument


def sum_boxes(boxes):
	minx = min([b.Min.X for b in boxes])
	miny = min([b.Min.Y for b in boxes])
	minz = min([b.Min.Z for b in boxes])
	maxx = max([b.Max.X for b in boxes])
	maxy = max([b.Max.Y for b in boxes])
	maxz = max([b.Max.Z for b in boxes])
	bb = BoundingBoxXYZ()
	bb.Min = XYZ(minx,miny,minz)
	bb.Max = XYZ(maxx,maxy,maxz)
	return bb


class CustomISelectionFilter(ISelectionFilter):
	def AllowElement(self, e):
		return True

	def AllowReference(self, refer, point):
		rvt_link_instance = doc.GetElement(refer)
		doc_link = rvt_link_instance.GetLinkDocument()
		elem_link = doc_link.GetElement(refer.LinkedElementId)
		if elem_link.Category.CategoryType == CategoryType.Model and elem_link.Category.Id.IntegerValue != BuiltInCategory.OST_DetailComponents.value__ and elem_link.Category.Id.IntegerValue != BuiltInCategory.OST_RasterImages.value__:
			return True	
		else:
			return False		


# Get 3D View ViewFamilyType
view_type = FilteredElementCollector(doc).OfClass(ViewFamilyType).ToElements().Find(lambda x : x.ViewFamily == ViewFamily.ThreeDimensional)
bbx,elems_in_links = [],[]

TaskDialog.Show("Selection", "Select the linked elements and press Finish")
ref_link = uidoc.Selection.PickObjects(ObjectType.LinkedElement, CustomISelectionFilter(), "Select linked elements")

for ref in ref_link:
	link_inst = doc.GetElement(ref)
	tf_link = link_inst.GetTotalTransform()
	doc_link = link_inst.GetLinkDocument()
	elem_in_link = doc_link.GetElement(ref.LinkedElementId)
	elems_in_links.append(elem_in_link)
	box = elem_in_link.get_BoundingBox(None)
	box.Min = tf_link.OfPoint(box.Min)
	box.Max = tf_link.OfPoint(box.Max)
	#box.Transform = tf_link
	bbx.append(box)
	sum_box = sum_boxes(bbx)

TransactionManager.Instance.EnsureInTransaction(doc)

view = doc.ActiveView if doc.ActiveView.ViewType == ViewType.ThreeD else View3D.CreateIsometric(doc, view_type.Id)
view.SetSectionBox(sum_box)

TransactionManager.Instance.TransactionTaskDone()	

TransactionManager.Instance.ForceCloseTransaction()
# Impossible to set the uidoc.ActiveView in Revit’s Idling event since Dynamo operates inside this event
#uidoc.ActiveView = view
uidoc.RequestViewChange(view)
uidoc.RefreshActiveView()

#Zoom to the linked elements
try:
	uiviews = uidoc.GetOpenUIViews()
	uiview = [x for x in uiviews if x.ViewId == view.Id][0]
	uiview.ZoomAndCenterRectangle(sum_box.Min, sum_box.Max)
except:
	pass

if len(elems_in_links) > 1: 
	OUT = view, elems_in_links, link_inst
else:
	OUT = view, elems_in_links[0], link_inst