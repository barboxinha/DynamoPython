"""
Built-In Parameters (BuiltInParameter)
hardcoded into Revit cannot be defined or deleted
Each parameter has an underscore-separated name written in all-capitals.
"""

###### BOILERPLATE CODE GOES HERE ######

# To read the sill height from a placed window
my_window = UnwrapElement(IN[0])
sill_height = my_window.get_Parameter(BuiltInParameter.INSTANCE_SILL_HEIGHT_PARAM).AsDouble()

OUT = sill_height

# To help in identifying the BuiltInParameter you're looking for:
# Find the name the parameter is referred to in the UI and use a CTRL+F search in the BuiltInParameter Enumeration page of APIDocs.co.
# Run a quick Google search to see if others have already asked the same question.
# Use the excellent RevitLookup add-in for Revit.
