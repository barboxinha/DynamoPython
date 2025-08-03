"""
Accessing Global Parameters
"""

###### BOILERPLATE CODE GOES HERE ######

# To retrieve a list of all global parameters' IDs we can use the GlobalParametersManager class and the GetAllGlobalParameters() method
all_global_parameter_ids = GlobalParametersManager.GetAllGlobalParameters(doc)

# Check if global parameters allowed in document with AreGlobalParametersAllowed() method
allowed_global_parameters = GlobalParametersManager.AreGlobalParametersAllowed(doc)

# We can also retrieve a single global parameter using its name
# the FindByName() method takes args doc, "<param>"
global_parameter_id = GlobalParametersManager.FindByName(doc,"Detail Guide Visibility")

# Finally, we can get the GlobalParameter object using the Document.GetElement() method
global_parameter = doc.GetElement(global_parameter_id)

"""
Getting and Setting Global Parameter Values
"""

# Retrieve the value from any GlobalParameter object using its GetValue() method
value = global_parameter.GetValue().Value

# Set the value by using the SetValue() method. Needs to be wrapped in a transaction as the document is being changed.
TransactionManager.Instance.EnsureInTransaction(doc)
global_parameter.SetValue(5.0) 
TransactionManager.Instance.TransactionTaskDone()   