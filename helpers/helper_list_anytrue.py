"""
List.AnyTrue
"""
__author__ = "Marco Barboza"


# Can be substituted with Dynamo native 'List.AnyTrue' node
# in Revit v2022+


import clr

clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *


def to_list(obj):
	if isinstance(obj, list):
		return obj
	return [obj]


def any_true(bool_list):
	return any(bool_list)

bool = to_list(IN[0])

OUT = any_true(bool)