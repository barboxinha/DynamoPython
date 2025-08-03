
"""
Unit Conversions
----------------
Feet, Inches, Meters, and Millimetres
"""

###### BOILERPLATE CODE GOES HERE ######

# When retrieving any length value using Revit's API, it will automatically be returned in decimal feet (for example, 6 inches = 0.5 Feet).
# Converting between units
detail_line = UnwrapElement(IN[0])
decimal_feet_length = detail_line.GeometryCurve.Length
metric_length = UnitUtils.Convert(decimal_feet_length, DisplayUnitType.DUT_DECIMAL_FEET, DisplayUnitType.DUT_METERS)

OUT = metric_length

# Converting Rotations
angle = 90.0
radians_equivalent = UnitUtils.Convert(angle, DisplayUnitType.DUT_DECIMAL_DEGREES, DisplayUnitType.DUT_RADIANS)

OUT = radians_equivalent