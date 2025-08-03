###### BOILERPLATE CODE GOES HERE ######

# Import necessary libraries
# RevitAPI, RevitAPIUI, RevitServices, RevitNodes

# Get Current Document
doc = DocumentManager.Instance.CurrentDBDocument

# Unwrap Revit FamilyInstance
revit_element = UnwrapElement(IN[0])

# Access element Instance parameters
element_parameters = revit_element.Parameters

# Access a specific parameter, use methods Element.LookupParameter("param") OR Element.get_Parameter("param")
# Use .AsString() OR .AsDouble() methods to read the parameter values
# This is the equivalent of using the GetParameterValueByName node
height_parameter = revit_element.LookupParameter("Height")
height_value = height_parameter.AsDouble()

area_parameter = revit_element.GetParameters("Area")
area_value = area_parameter[0].AsValueString()

mark_parameter = revit_element.LookupParameter("Mark")
mark_value = mark_parameter.AsString()

# Get FamilyType from FamilyInstance to access element Type parameters
family_type = doc.GetElement(revit_element.GetTypeId())
