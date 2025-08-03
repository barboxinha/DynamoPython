#Alban de Chasteigner 2022
#twitter : @geniusloci_bim
#geniusloci.bim@gmail.com
#https://github.com/albandechasteigner/GeniusLociForDynamo

"""
CAD.SelectCurve
---------------
Select a curve in a CAD import instance and return the curve and its layer name.
"""

import clr
clr.AddReference('RevitAPI')
import Autodesk
from Autodesk.Revit.DB import Curve, PolyLine, ElementId

clr.AddReference('RevitServices')
from RevitServices.Persistence import DocumentManager

clr.AddReference('RevitAPIUI')
from Autodesk.Revit.UI.Selection import ObjectType

clr.AddReference("RevitNodes")
import Revit
clr.ImportExtensions(Revit.GeometryConversion)


doc = DocumentManager.Instance.CurrentDBDocument
uiapp = DocumentManager.Instance.CurrentUIApplication

coords, line, layerName = [],[],[]

sel = uiapp.ActiveUIDocument.Selection
pickedRef = sel.PickObjects(ObjectType.PointOnElement, "Click on the line")

for ref in pickedRef:
    #coords.append(ref.GlobalPoint.ToPoint())
    element = doc.GetElement(ref)
    trans = element.GetTotalTransform()
    geoObj = element.GetGeometryObjectFromReference(ref)
    if isinstance (geoObj, Curve):
        line.append(geoObj.CreateTransformed(trans).ToProtoType())
    elif isinstance (geoObj, PolyLine):
        try: line.append(geoObj.GetTransformed(trans).ToProtoType())
        except: line.append(geoObj.GetTransformed(trans))
    if geoObj.GraphicsStyleId != ElementId.InvalidElementId:
        gs = doc.GetElement(geoObj.GraphicsStyleId)
        if (gs != None):
            layerName.append(gs.GraphicsStyleCategory.Name)

OUT = line, layerName#, trans.ToCoordinateSystem(1)