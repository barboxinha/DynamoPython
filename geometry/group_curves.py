# ALL CREDIT GOES TO THE ORIGINAL AUTHOR
# This code is a modified version of the original script by Konrad Sobon.
# Copyright(c) 2015, Konrad Sobon
# @arch_laboratory, http://archi-lab.net

import clr
clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *


input_curves = IN[0]

grouped_curves = []

# Join/group curves function
def group_curves(Line_List): 
	ignore_distance = 0.1 # Assume points this close or closer to each other are touching 
	grouped_lines = [] 
	Queue = set() 
	while Line_List: 
		Shape = [] 
		Queue.add(Line_List.pop()) # Move a line from the Line_List to our queue 
		while Queue: 
			Current_Line = Queue.pop() 
			Shape.append(Current_Line) 
			for Potential_Match in Line_List: 
				Points = (Potential_Match.StartPoint, Potential_Match.EndPoint)
				for P1 in Points: 
					for P2 in (Current_Line.StartPoint, Current_Line.EndPoint): 
						distance = P1.DistanceTo(P2) 
						if distance <= ignore_distance: 
							Queue.add(Potential_Match) 
			Line_List = [item for item in Line_List if item not in Queue]
		grouped_lines.append(Shape) 
	return grouped_lines

# Loop through every nested list of curves
for lst in input_curves:
	crvs = group_curves(lst)
	grouped_curves.append(crvs)
	
OUT = grouped_curves