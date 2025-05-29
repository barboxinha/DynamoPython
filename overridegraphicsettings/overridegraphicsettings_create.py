"""
OverrideGraphicSettings.Create
--------------------------------
Creates an OverrideGraphicSettings object with the specified settings.
"""
__author__ = 'Marco Barboza'


import clr

# Import the Revit API
clr.AddReference('RevitAPI')
import Autodesk
from Autodesk.Revit.DB import *

# Import DocumentManager and TransactionManager
clr.AddReference('RevitServices')
import RevitServices
from RevitServices.Persistence import DocumentManager


doc = DocumentManager.Instance.CurrentDBDocument
uiapp = DocumentManager.Instance.CurrentUIApplication
app = uiapp.Application
version=int(app.VersionNumber)


def tolist(obj) -> list:
	"""Converts the input into a list if it is not already a list."""
	return obj if isinstance(obj, list) else [obj]


def equalize_list_lengths(*lists):
	"""
	Determines the maximum length of the input lists. Then, iterates through each list and appends the last item of the list until its length matches the maximum length.
	"""
	# Find the maximum length among the lists
	max_length = max(len(lst) for lst in lists)
	
	# Duplicate the last item in each list to match the maximum length
	for lst in lists:
		while len(lst) < max_length:
			if lst:
				lst.append(lst[-1])
			else:
				lst.append(None)
	return lists


def all_none(*args) -> bool:
	"""Returns True if all the input arguments are None."""
	return all(arg is None for arg in args)


def convert_to_revit_color(color) -> Autodesk.Revit.DB.Color:
	"""Converts a Dynamo color into a Revit color."""
	return Autodesk.Revit.DB.Color(color.Red, color.Green, color.Blue)


def create_overridegraphicsettings(projLinePat, projLineColor, projLineWeight, surfaceForePat, surfaceForePatcolor, surfaceBackPat, surfaceBackPatcolor, cutLinePat, cutLineColor, cutLineWeight, cutForePat, cutForePatcolor, cutBackPat, cutBackPatcolor, transparency, halftone) -> Autodesk.Revit.DB.OverrideGraphicSettings:
	"""Creates an OverrideGraphicSettings object with the specified settings."""
	ogs = None
	if not all_none(projLinePat, projLineColor, projLineWeight, surfaceForePat, surfaceForePatcolor, surfaceBackPat, surfaceBackPatcolor, cutLinePat, cutLineColor, cutLineWeight, cutForePat, cutForePatcolor, cutBackPat, cutBackPatcolor, transparency, halftone):
		ogs = OverrideGraphicSettings()
		if projLinePat:
			ogs.SetProjectionLinePatternId(projLinePat.Id)
		if projLineColor:
			ogs.SetProjectionLineColor(convert_to_revit_color(projLineColor))
		if projLineWeight:
			ogs.SetProjectionLineWeight(projLineWeight)
		if cutLinePat:
			ogs.SetCutLinePatternId(cutLinePat.Id)
		if cutLineColor:
			ogs.SetCutLineColor(convert_to_revit_color(cutLineColor))
		if cutLineWeight:
			ogs.SetCutLineWeight(cutLineWeight)
		if transparency:
			ogs.SetSurfaceTransparency(transparency)
		if halftone:
			ogs.SetHalftone(halftone)
		if version < 2019:
			if surfaceForePatcolor:
				ogs.SetProjectionFillColor(convert_to_revit_color(surfaceForePatcolor))
			if surfaceForePat:
				ogs.SetProjectionFillPatternId(surfaceForePat.Id)
				ogs.SetProjectionFillPatternVisible(True)
			if surfaceBackPatcolor:
				ogs.SetProjectionFillColor(convert_to_revit_color(surfaceBackPatcolor))
			if surfaceBackPat:
				ogs.SetProjectionFillPatternId(surfaceBackPat.Id)
				ogs.SetProjectionFillPatternVisible(True)
			if cutForePatcolor:
				ogs.SetCutFillColor(convert_to_revit_color(cutForePatcolor))
			if cutForePat:
				ogs.SetCutFillPatternId(cutForePat.Id)
				ogs.SetCutFillPatternVisible(True)
			if cutBackPatcolor:
				ogs.SetCutFillColor(convert_to_revit_color(cutBackPatcolor))
			if cutBackPat:
				ogs.SetCutFillPatternId(cutBackPat.Id)
				ogs.SetCutFillPatternVisible(True)
		else:
			if surfaceForePatcolor:
				ogs.SetSurfaceForegroundPatternColor(convert_to_revit_color(surfaceForePatcolor))
			if surfaceForePat:
				ogs.SetSurfaceForegroundPatternId(surfaceForePat.Id)
				ogs.SetSurfaceForegroundPatternVisible(True)
			if surfaceBackPatcolor:
				ogs.SetSurfaceBackgroundPatternColor(convert_to_revit_color(surfaceBackPatcolor))
			if surfaceBackPat:
				ogs.SetSurfaceBackgroundPatternId(surfaceBackPat.Id)
				ogs.SetSurfaceBackgroundPatternVisible(True)	
			if cutForePatcolor:
				ogs.SetCutForegroundPatternColor(convert_to_revit_color(cutForePatcolor))
			if cutForePat:
				ogs.SetCutForegroundPatternId(cutForePat.Id)
				ogs.SetCutForegroundPatternVisible(True)
			if cutBackPatcolor:
				ogs.SetCutBackgroundPatternColor(convert_to_revit_color(cutBackPatcolor))
			if cutBackPat:
				ogs.SetCutBackgroundPatternId(cutBackPat.Id)
				ogs.SetCutBackgroundPatternVisible(True)
	return ogs


# Setup inputs as lists
projLinePats = tolist(IN[0])
projLineColors = tolist(IN[1])
projLineWeights = tolist(IN[2])
surfaceForePats = tolist(IN[3])
surfaceForePatcolors = tolist(IN[4])
surfaceBackPats = tolist(IN[5])
surfaceBackPatcolors = tolist(IN[6])
cutLinePats = tolist(IN[7])
cutLineColors = tolist(IN[8])
cutLineWeights = tolist(IN[9])
cutForePats = tolist(IN[10])
cutForePatcolors = tolist(IN[11])
cutBackPats = tolist(IN[12])
cutBackPatcolors = tolist(IN[13])
transparencies = tolist(IN[14])
halftones = tolist(IN[15])

# Equalize list lengths
equalize_list_lengths(projLinePats, projLineColors, projLineWeights, surfaceForePats, surfaceForePatcolors, surfaceBackPats, surfaceBackPatcolors, cutLinePats, cutLineColors, cutLineWeights, cutForePats, cutForePatcolors, cutBackPats, cutBackPatcolors, transparencies, halftones)

# Unwrap any required inputs
projLinePats = UnwrapElement(projLinePats)
surfaceForePats = UnwrapElement(surfaceForePats)
surfaceBackPats = UnwrapElement(surfaceBackPats)
cutLinePats = UnwrapElement(cutLinePats)
cutForePats = UnwrapElement(cutForePats)
cutBackPats = UnwrapElement(cutBackPats)

overrides = []

for projLinePat, projLineColor, projLineWeight, surfaceForePat, surfaceForePatcolor, surfaceBackPat, surfaceBackPatcolor, cutLinePat, cutLineColor, cutLineWeight, cutForePat, cutForePatcolor, cutBackPat, cutBackPatcolor, transparency, halftone in zip(projLinePats, projLineColors, projLineWeights, surfaceForePats, surfaceForePatcolors, surfaceBackPats, surfaceBackPatcolors, cutLinePats, cutLineColors, cutLineWeights, cutForePats, cutForePatcolors, cutBackPats, cutBackPatcolors, transparencies, halftones):
	#Create the OverridesGraphicsSettings
	ogs = create_overridegraphicsettings(projLinePat, projLineColor, projLineWeight, surfaceForePat, surfaceForePatcolor, surfaceBackPat, surfaceBackPatcolor, cutLinePat, cutLineColor, cutLineWeight, cutForePat, cutForePatcolor, cutBackPat, cutBackPatcolor, transparency, halftone)
	if ogs:
		overrides.append(ogs)
	

OUT = overrides if overrides else None