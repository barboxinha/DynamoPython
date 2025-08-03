"""
Retrieving Project Information Parameters
"""

###### BOILERPLATE CODE GOES HERE ######
import clr
clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager

clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import FilteredElementCollector, BuiltInCategory

doc = DocumentManager.Instance.CurrentDBDocument

# Retrieve the ProjectInfo object using a FilteredElementCollector
project_info = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_ProjectInformation).ToElements()[0]

# This returns a list of parameters, but it will only ever be 1 item long, 
# so we need to get the first element by its index using [0]
# project_info = project_info[0]

# Now we can access its ParameterSet or set of parameters
project_info_parameters = project_info.Parameters

# Iterate through each parameter, outputting its name and value
project_info_list = []

for parameter in project_info_parameters:
	project_info_list.append([parameter.Definition.Name, parameter.AsString()])	

OUT = project_info_list
