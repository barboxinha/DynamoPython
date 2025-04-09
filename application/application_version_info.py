"""
Application.RevitVersion
------------------------
Gets the current Revit application version info.
"""

# Import libraries and assemblies
import clr

clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager

doc = DocumentManager.Instance.CurrentDBDocument
uiapp = DocumentManager.Instance.CurrentUIApplication
app = uiapp.Application

# Get Full Version based on year
if int(app.VersionNumber) > 2017:
    fullVersion = app.SubVersionNumber
else:
    fullVersion = str(app.VersionNumber)

OUT = fullVersion