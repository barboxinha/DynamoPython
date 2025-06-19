"""
Family Acrobatics USAGE SAMPLE
------------------------------
Demonstrates how to navigate between Family, FamilyType, and FamilyInstance objects in Revit.
i.e. Family -> FamilyType -> FamilyInstance -> FamilyType -> Family
"""

# Boilerplate code above

# Moving Upstream from FamilyInstance -> FamilyType -> Family
family_instance = UnwrapElement(IN[0])
family_type_id = family_instance.GetTypeId()
family_type = family_instance.Symbol
family_type_2 = doc.GetElement(family_type_id)
family = family_type.Family

OUT = family_instance, family_type, family_type_2, family

# Moving Downstream from Family -> FamilyTypes -> FamilyInstances
family = UnwrapElement(IN[0])
family_type_ids = family.GetFamilySymbolIds()
family_types = [doc.GetElement(id) for id in family_type_ids]

# To find ALL FamilyInstance objects of a given Type, create a FamilyInstanceFilter using the Id of the required FamilyType.
family_instances = []

for family_type_id in family_type_ids:
	family_instance_filter = FamilyInstanceFilter(doc, family_type_id)
	elements = FilteredElementCollector(doc).WherePasses(family_instance_filter).ToElements()
	family_instances.append(elements)

OUT = family_instances
