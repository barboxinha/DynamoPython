"""
GraphicsStyle.AllAttributes
---------------------------
Retrieves all attributes of GraphicsStyle elements in Revit.
Returns the name, line weight, color, and line pattern name of each GraphicsStyle.
"""
__author__ = "Marco Barboza"


import clr

clr.AddReference("RevitNodes")
import Revit
clr.ImportExtensions(Revit.Elements)

clr.AddReference("DSCore")
import DSCore

clr.AddReference("RevitServices")
import RevitServices
from RevitServices.Persistence import DocumentManager

clr.AddReference("RevitAPI")
import Autodesk 
from Autodesk.Revit.DB import Document, GraphicsStyle, LinePatternElement, GraphicsStyleType, Color


def get_graphics_style_line_weight(graphics_style: GraphicsStyle) -> int:
    """
    Gets the line weight assigned to a given GraphicsStyle.
    """
    if graphics_style.GraphicsStyleType != GraphicsStyleType.Projection:
        return None
    
    style_cat = graphics_style.GraphicsStyleCategory

    return style_cat.GetLineWeight(GraphicsStyleType.Projection)


def get_graphics_style_color(graphics_style: GraphicsStyle) -> Color:
    """
    Gets the line color assigned to a given GraphicsStyle.
    """
    if graphics_style.GraphicsStyleType != GraphicsStyleType.Projection:
        return None
    
    style_cat = graphics_style.GraphicsStyleCategory

    return style_cat.LineColor


def convert_db_color_to_dyn_color(db_color: Color) -> DSCore.Color:
    """
    Converts Revit object Autodesk.Revit.DB.Color to Dynamo object DSCore.Color.
    """
    
    return DSCore.Color.ByARGB(255, db_color.Red, db_color.Green, db_color.Blue)


def get_graphics_style_line_pattern_name(_doc: Document, graphics_style: GraphicsStyle):
    """
    Gets the LinePatternElement name assigned to a given GraphicsStyle.
    """
    if graphics_style.GraphicsStyleType != GraphicsStyleType.Projection:
        return None
    
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
        else:
            line_pattern_name = None

    return line_pattern_name


doc = DocumentManager.Instance.CurrentDBDocument

line_styles = UnwrapElement(IN[0]) if isinstance(IN[0], list) else [UnwrapElement(IN[0])]
names = []
weights = []
colors = []
line_patterns = []

# Get style attributes
try:
    for style in line_styles:
        names.append(style.Name)
        weights.append(get_graphics_style_line_weight(style))
        colors.append(convert_db_color_to_dyn_color(get_graphics_style_color(style)))
        line_patterns.append(get_graphics_style_line_pattern_name(doc, style))
    
    OUT = names, weights, colors, line_patterns
except Exception as e:
    import traceback
    OUT = traceback.format_exc()
