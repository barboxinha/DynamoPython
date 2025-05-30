"""
Elevation.LocationPoint
------------------------
Get the location of the elevation in the project coordinate system.
"""
__author__ = "Marco Barboza"


import clr

clr.AddReference('RevitNodes')
import Revit
clr.ImportExtensions(Revit.Elements)
clr.ImportExtensions(Revit.GeometryConversion)

clr.AddReference('RevitAPI')
import Autodesk
from Autodesk.Revit.DB import XYZ


def elevation_location(elevation: Autodesk.Revit.DB.ViewSection) -> XYZ:
    """Get the location of the elevation in the project coordinate system."""
    # Construct a point at the midpoint of the front bottom edge of the elevation view cropbox
    xmax = elevation.CropBox.Max.X
    xmin = elevation.CropBox.Min.X
    ymin = elevation.CropBox.Min.Y
    zmax = elevation.CropBox.Max.Z

    pt = XYZ(xmax - 0.5 * (xmax - xmin), ymin, zmax)

    # Translate to project coordinate system
    pt = elevation.CropBox.Transform.OfPoint(pt)

    return pt


elevations = UnwrapElement(IN[0]) if isinstance(IN[0], list) else [UnwrapElement(IN[0])]
pts = []

for elev in elevations:
    pt = elevation_location(elev)
    pts.append(pt.ToPoint())

OUT = pts