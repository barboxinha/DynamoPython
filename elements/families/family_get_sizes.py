"""
Family.Sizes
------------
Retrieves the size of family files associated with family instances in a Revit document.
"""


import sys
import clr
import os
import tempfile
import math

clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *

clr.AddReference('RevitServices')
import RevitServices
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

clr.AddReference('RevitAPI')
import Autodesk
from Autodesk.Revit.DB import *


# Convert byte size to appropriate units
def convert_size(size_bytes):
    if not size_bytes:
        return "N/A"
    size_unit = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    size = round(size_bytes / p, 2)
    return "{}{}".format(size, size_unit[i])


doc = DocumentManager.Instance.CurrentDBDocument

family_instances = UnwrapElement(IN[0]) if isinstance(IN[0], list) else [UnwrapElement(IN[0])]
all_family_sizes = []

# Create a temporary file directory to save family files
temp_dir = os.path.join(tempfile.gettempdir(), "RVT_ModelFamilySizes")
if not os.path.exists(temp_dir):
    os.mkdir(temp_dir)

save_as_options = SaveAsOptions()
save_as_options.OverwriteExistingFile = True

for fam in family_instances:
    # Get the FamilyInstance Family object
    family_type = fam.Symbol
    family = family_type.Family

    # Get the Family's Document
    if family.IsEditable:
        TransactionManager.Instance.ForceCloseTransaction()
        family_doc = doc.EditFamily(family)
        family_path = family_doc.PathName
        
        if not family_path or not os.path.exists(family_path):
            # save in temporary path to retrieve family file size
            family_path = os.path.join(temp_dir, family_doc.Title)
            family_doc.SaveAs(family_path, save_as_options)
        
        # Get the family document's file size
        family_size = 0
        if family_path and os.path.exists(family_path):
            family_size = os.path.getsize(family_path)
        all_family_sizes.append(convert_size(family_size))

        # Close opened family documents
        family_doc.Close(False)

        # Remove temporary family file
        if family_path.lower().startswith(temp_dir.lower()):
            os.remove(family_path)
    elif family.IsInPlace:
        all_family_sizes.append("In-Place Model")
    else:
        all_family_sizes.append("N/A")

OUT = all_family_sizes