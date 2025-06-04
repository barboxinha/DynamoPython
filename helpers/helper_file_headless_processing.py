"""
Open & Close External Files
---------------------------
Headlessly open and batch process multiple files
"""

# Boilerplate code above
# This example works for both (.rfa) and (.rvt) files
input_paths = IN[0] if isinstance(IN[0], list) else [IN[0]]

open_options = OpenOptions() # Creating a new OpenOptions object
report = [] # Creating an empty list, which will contain our final report

for path in input_paths: # Iterating through each filepath string
	filepath = FilePath(path) # Creating a Revit FilePath object from this
	family_doc = app.OpenDocumentFile(filepath, open_options) # Telling the Revit application to open the file we specify
	dimensions = FilteredElementCollector(family_doc).OfCategory(BuiltInCategory.OST_Dimensions).WhereElementIsNotElementType().ToElements() # Creating a FilteredElementCollector to gather dimension elements
	number_dimensions = len(dimensions) # Counting the number of dimensions
	report_message = "File {} contains {} dimensions." # Specify report message string
	report.append(report_message.format(path, number_dimensions)) # Creating a formatted string for our report
	family_doc.Close(False) # Finally, closing the document (False = without saving)

OUT = report # Outputting the report we generated
