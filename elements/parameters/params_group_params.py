"""
Accessing Group Parameters
"""

###### BOILERPLATE CODE GOES HERE ######

# Instance parameters can be read directly from a group instance
# either by collecting using a FilteredElementCollector, or passed as an unwrapped argument
group = UnwrapElement(IN[0])
group_parameter = group.LookupParameter("Group Mark").AsString()

# To access Group Type params, first access the GroupType object by either using a FilteredElementCollector with the .WhereElementIsElementType() filter, 
# or by accessing it from a placed group instance.
group_type_id = group.GetTypeId()
group_type = doc.GetElement(group_type_id)

group_type_parameter = group_type.LookupParameter("Apt Type").AsString()

# Iterate through a list of groups to access their parameter values
groups = UnwrapElement(IN[1])

groups_type_params = []
for g in groups:
	g_type_id = g.GetTypeId()
	g_type = doc.GetElement(g_type_id)
	groups_type_params.append(g_type.LookupParameter("Apt Type").AsString())
	
OUT = groups_type_params
