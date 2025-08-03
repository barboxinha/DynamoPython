# Copyright(c) 2015, Konrad K Sobon
# @arch_laboratory, http://archi-lab.net
# Last Edited By: Marco Barboza

##### ----- NOTES ----- #####
# - Added ability to process a nested list of elements. +Lines 96-99

import clr
import sys
import System
clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *

# Import Element wrapper extension methods
clr.AddReference("RevitNodes")
import Revit
clr.ImportExtensions(Revit.Elements)

# Import DocumentManager and TransactionManager
clr.AddReference("RevitServices")
import RevitServices
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

doc = DocumentManager.Instance.CurrentDBDocument
uiapp = DocumentManager.Instance.CurrentUIApplication
app = uiapp.Application

# Import RevitAPI
clr.AddReference("RevitAPI")
import Autodesk
from Autodesk.Revit.DB import *


paramNames = IN[0]

if isinstance(IN[1], list):
    elements = [UnwrapElement(i) for i in IN[1]]
else:
    elements = [UnwrapElement(IN[1])]


def ProcessList(_func, _list):
    return map( lambda x: ProcessList(_func, x) if type(x)==list else _func(x), _list )

def ProcessListArg(_func, _list, _arg):
    return map( lambda x: ProcessListArg(_func, x, _arg) if type(x)==list else _func(x, _arg), _list )

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

def GetBipValue(element, bip):
    doc = element.Document
    value = None
    try:
        tempValue = element.get_Parameter(bip)
    except:
        tempValue = None
        pass
    if tempValue != None and tempValue.HasValue:
        if element.get_Parameter(bip).StorageType == StorageType.String:
            value = element.get_Parameter(bip).AsString()
        elif element.get_Parameter(bip).StorageType == StorageType.Integer:
            value  = element.get_Parameter(bip).AsInteger()
        elif element.get_Parameter(bip).StorageType == StorageType.Double:
            value = element.get_Parameter(bip).AsDouble()
        elif element.get_Parameter(bip).StorageType == StorageType.ElementId:
            id = element.get_Parameter(bip).AsElementId()
            value = doc.GetElement(id)
        return value
    else:
        return None

try:
    errorReport = None
    paramValues = []
    if isinstance(paramNames, list):
        builtInParams = ProcessList(GetBuiltInParam, paramNames)
        for i in builtInParams:
            paramValues.append(ProcessListArg(GetBipValue, elements, i))
    else:
        builtInParams = GetBuiltInParam(paramNames)
        if isinstance(elements, list):
            for element in elements:
                if isinstance(element, list) or isinstance(element, "__iter__"):
                    paramValues.append(ProcessListArg(GetBipValue, element, builtInParams))
                else:
                    paramValues.append(GetBipValue(element, builtInParams))
except:
    # if error accurs anywhere in the process catch it
    import traceback
    errorReport = traceback.format_exc()

#Assign your output to the OUT variable
if errorReport == None:
    OUT = paramValues
else:
    OUT = errorReport