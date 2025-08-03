"""
ScheduleSheetInstance.IsTitleblockRevisionSchedule
--------------------------------------------------
Checks if a given ScheduleSheetInstance is a titleblock revision schedule.
"""
__author__ = "Marco Barboza"


import clr

clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager

clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import ScheduleSheetInstance


doc = DocumentManager.Instance.CurrentDBDocument

# Ensure input is list type and unwrap elements.
schedule_instance = UnwrapElement(IN[0]) if isinstance(IN[0], list) else [UnwrapElement(IN[0])]

# Iterate through list of schedules depending on their list dimension.
if isinstance(schedule_instance[0], list):
	is_rev_schedule = [[i.IsTitleblockRevisionSchedule for i in inst] for inst in schedule_instance]
else:
	is_rev_schedule = [i.IsTitleblockRevisionSchedule for i in schedule_instance]

OUT = is_rev_schedule