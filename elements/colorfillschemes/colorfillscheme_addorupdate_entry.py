"""
ColorFillScheme.AddOrUpdateEntry
--------------------------------
Updates an entry in a Color Fill Scheme or creates it if it does not exist.
"""
__author__ = "Marco Barboza"


import clr

clr.AddReference('RevitAPI')
import Autodesk
from Autodesk.Revit.DB import *

clr.AddReference('RevitServices')
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager


def tolist(obj1):
    if isinstance(obj1, list): return obj1
    else: return [obj1]


def to_revit_color(dynamo_color) -> Autodesk.Revit.DB.Color:
    """Converts a Dynamo color to a Revit color."""
    return Autodesk.Revit.DB.Color(dynamo_color.Red, dynamo_color.Green, dynamo_color.Blue)


def get_colorfillscheme_entries(color_scheme):
    """Get the entries of a Color Fill Scheme."""
    return color_scheme.GetEntries()


def get_colorfillscheme_entry_value(entry):
    """Get the value of a Color Fill Scheme Entry."""
    if entry.StorageType == StorageType.ElementId:
        return entry.GetElementIdValue()
    elif entry.StorageType == StorageType.String:
        return entry.GetStringValue()
    elif entry.StorageType == StorageType.Integer:
        return entry.GetIntegerValue()
    else:
        return entry.GetDoubleValue()


def create_colorfillscheme_entry(value, color, fill_pattern_id, is_visible):
    """Create a new Color Fill Scheme Entry."""
    if value is None:
        return None

    if isinstance(value, ElementId):
        storage_type = StorageType.ElementId
    elif isinstance(value, str):
        storage_type = StorageType.String
    elif isinstance(value, int):
        storage_type = StorageType.Integer
    else:
        storage_type = StorageType.Double

    entry = ColorFillSchemeEntry(storage_type)

    if color:
        entry.Color = color
    
    if fill_pattern_id:
        entry.FillPatternId = fill_pattern_id
    
    if is_visible is not None:
        entry.IsVisible = is_visible

    if storage_type != StorageType.String:
        if entry.CanSetValue(value):
            if storage_type == StorageType.ElementId:
                entry.SetElementIdValue(value)
            elif storage_type == StorageType.Integer:
                entry.SetIntegerValue(value)
            else:
                entry.SetDoubleValue(value)
    else:
        entry.SetStringValue(value)

    return entry


doc = DocumentManager.Instance.CurrentDBDocument

element = tolist(UnwrapElement(IN[0]))[0]
entries = tolist(UnwrapElement(IN[1]))
colors = tolist(IN[2])
fill_patterns = tolist(UnwrapElement(IN[3]))
visibles = tolist(IN[4])
color_len = len(colors) == 1
fill_patterns_len = len(fill_patterns) == 1
visibles_len = len(visibles) == 1

# Check if element is ColorFillScheme object or name
if isinstance(element, Autodesk.Revit.DB.ColorFillScheme):
    scheme = element
elif isinstance(element, str):
    #scheme = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_ColorFillSchema).ToElements().Find(lambda x : x.Name == element)
    scheme = next((x for x in FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_ColorFillSchema).ToElements() if x.Name == element), None)

if not scheme:
    raise Exception("ColorFillScheme not found.")

TransactionManager.Instance.EnsureInTransaction(doc)

# Get existing scheme entries
ex_entries = get_colorfillscheme_entries(scheme)

for number in range(len(entries)):
    entry = None
    if isinstance(entries[number], Autodesk.Revit.DB.ColorFillSchemeEntry):
        entry = entries[number]
    else:
        # Check if entry exists in the scheme or create a new one
        entry_value = entries[number].Id if isinstance(entries[number], Autodesk.Revit.DB.Element) else entries[number]
        ex_entry = next((x for x in ex_entries if get_colorfillscheme_entry_value(x) == entry_value), None)
        
        if ex_entry:
            entry = ex_entry
        else:
            entry = create_colorfillscheme_entry(entry_value, None, None, True)
            
    if IN[2] != None:   
        c = 0 if color_len else number
        entry.Color = to_revit_color(colors[c])
    else: pass
    if IN[3] != None:
        f = 0 if fill_patterns_len else number
        entry.FillPatternId = fill_patterns[f].Id
    else: pass
    if IN[4] != None:
        v = 0 if visibles_len else number
        entry.IsVisible = visibles[v]
    else: pass

    # Add or update scheme entry.
    if scheme.CanUpdateEntry(entry): # Checks whether entry exists in the scheme and not the same as input one.
        scheme.UpdateEntry(entry)
    else:
        scheme_consistency = scheme.IsEntryConsistentWithScheme(entry)
        if scheme_consistency == EntryAndSchemeConsistency.Consistent:
            scheme.AddEntry(entry)
        else:
            import System
            raise Exception("{}: Entry is not consistent with scheme: {}".format(get_colorfillscheme_entry_value(entry), System.Enum.GetName(EntryAndSchemeConsistency, scheme_consistency)))

TransactionManager.Instance.TransactionTaskDone()

OUT = scheme
