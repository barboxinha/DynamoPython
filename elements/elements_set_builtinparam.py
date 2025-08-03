# Copyright(c) 2019, Konrad K Sobon
# @arch_laboratory, http://archi-lab.net
# Last Edited By: Marco Barboza

##### ----- NOTES ----- #####
# - Added ability to process a nested list of elements. +Lines 60-68
# - Added ability to map a single parameter value to multiple elements. +Lines 56-59, 70-72

import clr
import sys
import System

clr.AddReference("RevitNodes")
import Revit
clr.ImportExtensions(Revit.Elements)

clr.AddReference("RevitServices")
import RevitServices
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

clr.AddReference("RevitAPI")
import Autodesk
from Autodesk.Revit.DB import *

doc = DocumentManager.Instance.CurrentDBDocument

paramName = IN[0]

if not isinstance(IN[1], list):
    elements = [IN[1]]
else:
    elements = IN[1]

if not isinstance(IN[2], list):
    paramValues = [IN[2]]
else:
    paramValues = IN[2]


def GetBuiltInParam(paramName):
    builtInParams = System.Enum.GetValues(BuiltInParameter)
    builtInParamNames = System.Enum.GetNames(BuiltInParameter)
    test = []
    #for i in builtInParams:
    for i, j in zip(builtInParamNames, builtInParams):
        #if i.ToString() == paramName:
        if i == paramName:
            test.append(j)
            break
        else:
            continue
    return test[0]


def duplicate(item: object, num_times: int):
    """Duplicates an item a given number of times."""
    for i in range(num_times):
        yield item


try:
    errorReport = None
    count = 0

    TransactionManager.Instance.EnsureInTransaction(doc)
    
    bipName = GetBuiltInParam(paramName)

    if len(elements) != len(paramValues):
        if len(paramValues) == 1:
            paramValues = duplicate(paramValues[0], len(elements))
    
    for i, j in zip(elements, paramValues):
        if isinstance(i, list):
            for k, l in zip(i, j):
                param = UnwrapElement(k).get_Parameter(bipName)
                if param.StorageType == StorageType.ElementId:
                    id = ElementId(l)
                    param.Set(id)
                else:
                    param.Set(l)
        else:
            param = UnwrapElement(i).get_Parameter(bipName)
            if param.StorageType == StorageType.ElementId:
                id = ElementId(j)
                param.Set(id)
            else:
                param.Set(j)
        count += 1

    TransactionManager.Instance.TransactionTaskDone()
except:
    import traceback
    errorReport = traceback.format_exc()

if errorReport == None:
    OUT = elements
else:
    OUT = errorReport