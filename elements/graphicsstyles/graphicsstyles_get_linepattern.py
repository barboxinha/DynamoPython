"""
GraphicsStyle.GetLinePattern
----------------------------
Gets the LinePatternElement associated to a given GraphicsStyle(s).
"""
__author__ = "Marco Barboza"


import clr

clr.AddReference("RevitNodes")
import Revit
clr.ImportExtensions(Revit.Elements)

clr.AddReference("RevitServices")
import RevitServices
from RevitServices.Persistence import DocumentManager

clr.AddReference("RevitAPI")
import Autodesk 
from Autodesk.Revit.DB import Document, GraphicsStyle, LinePatternElement, GraphicsStyleType


def get_graphics_style_line_pattern_name(_doc: Document, graphics_style: GraphicsStyle):
    """
    Gets the LinePatternElement name assigned to a given GraphicsStyle.
    """
    line_pattern_name = None

    if graphics_style.GraphicsStyleType != GraphicsStyleType.Projection:
        return line_pattern_name
    
    style_cat = graphics_style.GraphicsStyleCategory
    # The line pattern id will be one of the following:
    #     A negative value (representing a built-in line pattern)
    #     The id of a LinePatternElement
    #     InvalidElementId, indicating that this category does not have a stored line pattern id for this graphics style type.
    # REVIT API Remark: Note that Solid is special. It isn't a line pattern at all -- it is a special code that tells drawing and export code
    # to use solid lines rather than patterned lines. Solid is visible to the user when selecting line patterns.
    solid_pattern_id = LinePatternElement.GetSolidPatternId()
    line_pattern_id = style_cat.GetLinePatternId(GraphicsStyleType.Projection)

    if line_pattern_id.Equals(solid_pattern_id):
        line_pattern_name = "Solid"
    elif line_pattern_id is None:
        line_pattern_name = None
    else:
        line_pattern = _doc.GetElement(line_pattern_id)
        if line_pattern:
            line_pattern_name = line_pattern.Name

    return line_pattern_name


doc = DocumentManager.Instance.CurrentDBDocument

line_styles = UnwrapElement(IN[0]) if isinstance(IN[0], list) else [UnwrapElement(IN[0])]

# Get style Line Patterns
try:
    line_patterns = [get_graphics_style_line_pattern_name(doc, style) for style in line_styles]
    OUT = line_patterns if len(line_patterns) > 1 else line_patterns[0]
except Exception as e:
    import traceback
    OUT = traceback.format_exc()
