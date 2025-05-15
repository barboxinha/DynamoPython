#Alban de Chasteigner 2021
#twitter : @geniusloci_bim
#geniusloci.bim@gmail.com
#https://github.com/albandechasteigner/GeniusLociForDynamo


import math
import clr
clr.AddReference('RevitAPI')
import Autodesk
from Autodesk.Revit.DB import Options, GeometryInstance, XYZ

clr.AddReference("RevitNodes")
import Revit
clr.ImportExtensions(Revit.GeometryConversion)
clr.ImportExtensions(Revit.Elements)

clr.AddReference("RevitServices")
import RevitServices
from RevitServices.Persistence import DocumentManager


uiapp = DocumentManager.Instance.CurrentUIApplication
version = int(uiapp.Application.VersionNumber)

points, rotations, blocks, layersAll = [],[],[],[]

elem = UnwrapElement(IN[0])
geoElem = elem.get_Geometry(Options())

for geoObj in geoElem:
    transform = geoObj.Transform
    instance = geoObj.SymbolGeometry
    for inst in instance:
        layers = []
        if isinstance(inst,GeometryInstance):
            points.append(transform.OfPoint(inst.Transform.Origin).ToPoint())
            rotation = abs(math.degrees(inst.Transform.BasisX.AngleOnPlaneTo(XYZ.BasisX, XYZ.BasisZ))-360)
            if round(rotation,3) == 360:
                rotation = 0
            rotations.append(round(rotation,3))
            if version > 2022:
                blocks.append(elem.Document.GetElement(inst.GetSymbolGeometryId().SymbolId).ToDSType(True).Name.split(".dwg.")[-1])
            else:
                blocks.append(inst.Symbol.ToDSType(True).Name.split(".dwg.")[-1])
            geom = inst.SymbolGeometry
            for geo in geom:
                try:
                    layers.append(elem.Document.GetElement(geo.GraphicsStyleId).GraphicsStyleCategory.Name)
                except:
                    layers.append(None)
            if layers != []:
                layersAll.append(layers[0])
            else:
                layersAll.append(layers)
            
OUT = blocks, points, rotations, layersAll