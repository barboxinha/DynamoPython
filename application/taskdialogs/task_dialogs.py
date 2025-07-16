"""
User Feedback: Task Dialogs
---------------------------
Give users quick-and-dirty visual feedback.
"""

###### BOILERPLATE CODE GOES HERE ######
import clr

clr.AddReference("RevitAPIUI")
from Autodesk.Revit.UI import TaskDialog

# Create a simple TaskDialog instance for a pop-up window.
# TaskDialog.Show("Example Title", "Example text feedback here.")

# Customizing the TaskDialog - can be edited via the class' properties for a richer experience.
task_dialog = TaskDialog("Example Title")
task_dialog.CommonButtons = TaskDialogCommonButtons.Cancel | TaskDialogCommonButtons.Ok | TaskDialogCommonButtons.Close | TaskDialogCommonButtons.No | TaskDialogCommonButtons.Yes | TaskDialogCommonButtons.Retry | TaskDialogCommonButtons.None
task_dialog.FooterText = "Example Footer Text" # HTML Hyperlink tags can be used
task_dialog.MainInstruction = "Example Main Instruction" # The large primary text that appears at the top of a task dialog. Sum up problem or situation that is causing the message to display.
task_dialog.MainContent = "This is the main content for this TaskDialog" # The smaller text that appears just below the main instructions. It is optional. Should be used to give further explanation to the user, such as how to correct the problem or work around the situation.
task_dialog.Show()
