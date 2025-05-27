"""
FilteredElementCollector USAGE SAMPLE
-------------------------------------
Demonstrates how to use the FilteredElementCollector class in Revit API to filter elements based on their category, class, and view.
"""

# Boilerplate goes here
# Import the necessary Revit API classes

# Filter elements by their Revit Category using the OfCategory(BuiltInCategory enum) method
# Use the WhereElementIsNotElementType() method to filter only instances. WhereElementIsElementType() returns only types
# Use the ToElements() method to return Revit elements and ToElementIds() to return their Ids
all_furniture = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Furniture).WhereElementIsNotElementType().ToElements()

#Filter elements by their Class using the OfClass() method
all_views = FilteredElementCollector(doc).OfClass(View).ToElementIds()

#Filter elements within the Active View in Revit
active_view = FilteredElementCollector(doc, doc.ActiveView.Id).OfClass(Wall).ToElements()

OUT = all_furniture

# Use the ElementLevelFilter to filter for elements hosted at a level
# Use the ElementWorksetFilter to filter only for elements on a specific workset
# Go to https://thebuildingcoder.typepad.com/blog/about-the-author.html#5.9 for in detail documentation of FilteredElementCollectors