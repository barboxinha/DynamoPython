"""
DynamoPython script to Generate Points in a Grid with Specific Offsets
This script creates a grid of points with specific offsets in the Z direction based on certain conditions.
It includes multiple methods for generating points, which can be uncommented as needed.
"""

# Load the Python Standard and DesignScript Libraries
import sys
import clr
clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *

# Empty list to add points to
out_points = []

# Points Method 1 - XY Grid Offset Specific Points
for i in range(11):
    sub_points = []
    for j in range(11):
        z = 0
        if (i == 5 and j == 5):
            z = 1
        elif (i == 8 and j == 2):
            z = 1
        sub_points.append(Point.ByCoordinates(i, j, z))
    out_points.append(sub_points)
 
# Points Method 2 - Line Offset Specific Point
#for i in range(11):
#    z = 0
#    if (i == 2):
#        z = 1
#    out_points.append(Point.ByCoordinates(i, 0, z))

# Points Method 3 - Line Offset Point Negatively
#for i in range(11):
#    z = 0
#    if (i == 7):
#        z = -1
#    out_points.append(Point.ByCoordinates(i, 5, z))

# Points Method 4 - Line Offset Point
#for i in range(11):
#    z = 0
#    if (i == 5):
#        z = 1
#    out_points.append(Point.ByCoordinates(i, 10, z))

# Points Method 5 - XY Grid Offset Specific Points
#for i in range(11):
#    sub_points = []
#    for j in range(11):
#        z = 0
#        if (i == 1 and j == 1):
#            z = 2
#        elif (i == 8 and j == 1):
#            z = 2
#        elif (i == 2 and j == 6):
#            z = 2
#        sub_points.append(Point.ByCoordinates(i, j, z))
#    out_points.append(sub_points)

OUT = out_points