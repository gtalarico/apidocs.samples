#
#License:
#
#
# Revit Batch Processor Sample Code
#
# Copyright (c) 2021  Jan Christel
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#

import clr
import System

# import common library modules
import RevitCommonAPI as com
import RevitWorksets as rWork
import Result as res
import Utility as util
import RevitFamilyUtils as rFamU

# import Autodesk
from Autodesk.Revit.DB import *

clr.ImportExtensions(System.Linq)

# -------------------------------------------- common variables --------------------
# header used in reports
REPORT_GRIDS_HEADER = ['HOSTFILE','ID', 'NAME', 'WORKSETNAME', 'EXTENTMAX', 'EXTENTMIN']

# --------------------------------------------- utility functions ------------------

# doc:   current model document
def GetAllGridHeadsByCategory(doc):
    ''' this will return a filtered element collector of all grid head types in the model'''
    collector = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_GridHeads).WhereElementIsElementType()
    return collector

# doc:   current model document
def GetAllGridTypesByCategory(doc):
    ''' this will return a filtered element collector of all grid types in the model'''
    collector = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Grids).WhereElementIsElementType()
    return collector

# doc:   current model document
def GetAllGridTypeIdsByCategory(doc):
    ''' this will return a filtered element collector of all grid types ids in the model'''
    collector = GetAllGridTypesByCategory(doc)
    ids = com.GetIdsFromElementCollector(collector)
    return ids

# returns a list of list containing a valid grid types available in model
# format: [[GridTypeId as Revit ElementId, grid type name as string],[...]]
# doc: the current revit document
# g: a grid in the model
def GetGridTypeNames (doc, g):
    validGridTypes = []
    validgridTypeIds = g.GetValidTypes()
    for validGridTypeId in validgridTypeIds:
        gridData = []
        gtypeT = doc.GetElement(validGridTypeId)
        gridData.append(validGridTypeId)
        gridData.append(Element.Name.GetValue(gtypeT))
        validGridTypes.append(gridData)
    return validGridTypes

# returns the grid type name of a grid
# doc: the current revit document
# g: a grid in the model
def GetGridTypeName (doc, g):
    value = 'unknown'
    gtypeT = doc.GetElement(g.GetTypeId())
    value = Element.Name.GetValue(gtypeT)
    return value

# returns the grid type Id based on it's name, if no match found it returns the Revit Invalid Element Id
# doc: the current revit document
# gridtypeName: a grid type name in the model
def GetGridTypeIdByName (doc, gridtypeName):
    id = ElementId.InvalidElementId
    grids = FilteredElementCollector(doc).OfClass(Grid).ToList()
    if(len(grids) > 0):
        g = grids[0]
        validgridTypeIds = g.GetValidTypes()
        for gridTypId in validgridTypeIds:
            gtypeTName = Element.Name.GetValue(doc.GetElement(gridTypId))
            if(gtypeTName ==  gridtypeName):
                id = gridTypId
                break
    return id

# returns true if a given parameter and its value match the condition supplied
# g: a grid in the model
# paraName: the parameter name (by default 'Name' and 'Scope Box' are available)
# paraCondition: a method comparing the values. Default methods can be found in Utility module: ConDoesNotEqual, ConDoesEqual
# conditionValue: the value you are comparing the parameter value with
def FilterGridByParameterAndValue(g, paraName, paraCondition, conditionValue):
    ruleMatch = False
    # loop over parameters and compare value as required
    pValue = com.GetParameterValueByName(g, paraName)
    if (pValue != None):
        ruleMatch = com.CheckParameterValue(p, paraCondition, conditionValue)
    return ruleMatch

# returns true if a given grid and its type match the condition supplied
# doc: the current revit document
# g: a grid in the model
# paraCondition: a method comparing the values. Default methods can be found in Utility module: ConDoesNotEqual, ConDoesEqual
# conditionValue: the value you are comparing the parameter value with
def FilterGridByTypeName(doc, g, paraCondition, conditionValue):
    gridTypeName = GetGridTypeName (doc, g)
    isMatch = paraCondition(util.EncodeAscii(conditionValue), util.EncodeAscii(gridTypeName))
    return isMatch

# returns true if a given parameter has a value meeting the parameter condition
# g: a grid in the model
# paraName: the parameter name
# paraCondition: the test condition method
# conditionValue: the parameter condition value to check against
def GridCheckParameterValue(g, paraName, paraCondition, conditionValue):
    ruleMatch = False
    pValue = com.GetParameterValueByName(g, paraName)
    if (pValue != None):
        ruleMatch = com.CheckParameterValue(p, paraCondition, conditionValue)
    return ruleMatch

# returns the maximum extent of a grid as a string:
# g: a grid in the model
# format:
#max=[x,y,z]<tab>min[x,y,z]
def GetMaxExtentAsString(g):
    ex = g.GetExtents()
    max = '['+ ','.join([str(ex.MaximumPoint.X), str(ex.MaximumPoint.Y), str(ex.MaximumPoint.Z)]) + ']'
    min = '['+ ','.join([str(ex.MinimumPoint.X), str(ex.MinimumPoint.Y), str(ex.MinimumPoint.Z)]) + ']'    
    return '\t'.join([min, max])

# ------------------------------------------------------ grids workset modifiers ------------------------------------------
# workset modifier method
# moves all grids to one workset
# returns a result object
# rules format:
#['Model name',[
#       [workset modifier method,
#           [worksetName]
#           ]
#       ]
def ModifyGridWorkSetsDefault (doc, worksetRules):
    gridsResults = res.Result()
    collectorGrids = FilteredElementCollector(doc).OfClass(Grid)
    for rule in worksetRules:
        for defaultWorksetName in rule:
            grids = rWork.ModifyElementWorkset(doc, defaultWorksetName, collectorGrids, 'grids')
            gridsResults.Update(grids)
    return gridsResults

# workset modifier method
# moves grids matching type condition to a particular workset
# returns a result object
#defaultWorksetTypeRules_ = [
#    ['model name',[
#        [ModifyGridWorkSetsByTypeName,[
#            ['workset name', util.ConDoesNotEqual, 'grid type name'],
#            ['workset name', util.ConDoesEqual, 'grid type name']
#            ]
#        ]
#        ]
#    ]
#]
def ModifyGridWorkSetsByTypeName(doc, worksetRules):
    gridsResults = res.Result()
    # loop over grid type filter and address one at the time
    # get all grids matching type name filter
    for defaultWorksetName, typeNameCondition, typeName,  in worksetRules:
        # get the grid type id from the type name
        typeId = GetGridTypeIdByName(doc, typeName)
        collectorGrids = FilteredElementCollector(doc).OfClass(Grid).Where(lambda e: typeNameCondition(e.GetTypeId(), typeId))
        grids = rWork.ModifyElementWorkset(doc, defaultWorksetName, collectorGrids, 'grids')
        gridsResults.Update(grids)
    return gridsResults

# workset modifier method
# moves grids matching parameter condition to a particular workset
# returns a result object
#defaultWorksetRulesNames_ = [
#    ['model name',[
#        [ModifyGridWorkSetsByParameterValue,[
#            ['workset name', util.ConTwoStartWithOne, 'Name' ,'name starts with value']
#            ]
#        ]
#        ]
#    ]
#]
def ModifyGridWorkSetsByParameterValue(doc, worksetRules):
    gridsResults = res.Result()
    # loop over grid parameter filter and address one at the time
    # get all grids matching filter
    for defaultWorksetName, paraCondition, paraName, conditionValue  in worksetRules:
        collectorGrids = FilteredElementCollector(doc).OfClass(Grid).Where(lambda e: GridCheckParameterValue(e, paraName, paraCondition, conditionValue))
        grids = rWork.ModifyElementWorkset(doc, defaultWorksetName, collectorGrids, 'grids')
        gridsResults.Update(grids)
    return gridsResults

# modifies worksets of grids as per workset rules
# returns a result object
# doc: the current revit document
# rules format:
#defaultWorksetRulesAll_ = [
#    ['model name',[
#        [ModifyGridWorkSetsDefault,[
#            ['default workset name'] # there should only be one per model
#            ]
#        ]
#        ]
#    ]
#]
def ModifyGridsWorksets(doc, revitFileName, worksetRules):
    gridsResults = res.Result()
    foundMatch = False
    for fileName, worksetModifierList in worksetRules:
        if (revitFileName.startswith(fileName)):
            foundMatch = True
            for worksetModifier, rules in worksetModifierList:
                grids = worksetModifier(doc, rules)
                gridsResults.Update(grids)
            break
    if foundMatch == False:
        gridsResults.UpdateSep(False, 'No grid rules found for file: ' + revitFileName)
    return gridsResults

# ------------------------------------------------------- Grid reporting --------------------------------------------------------------------

# gets grid data ready for being printed to file
# doc: the current revit document
# revitFilePath: fully qualified file path of Revit file
def GetGridReportData(doc, revitFilePath):
    data = []
    for p in FilteredElementCollector(doc).OfClass(Grid):
        data.append([
            util.GetFileNameWithoutExt(revitFilePath), 
            str(p.Id.IntegerValue), 
            util.EncodeAscii(p.Name), 
            rWork.GetWorksetNameById(doc, p.WorksetId.IntegerValue), 
            GetMaxExtentAsString(p)])
    return data

# -------------------------------------------------  purge --------------------------------------------------------------------

# doc             current document
def GetUnusedGridTypesForPurge(doc):
    ''' this will return all ids of unused grid types in the model to be purged'''
    return com.GetUsedUnusedTypeIds(doc, GetAllGridTypeIdsByCategory, 0, 8)

# doc             current document
def GetAllGridHeadFamilyTypeIds(doc):
    ''' this will return all ids grid head family types in the model'''
    ids = []
    filter = ElementCategoryFilter(BuiltInCategory.OST_GridHeads)
    col = FilteredElementCollector(doc).OfClass(FamilySymbol).WherePasses(filter)
    ids = com.GetIdsFromElementCollector(col)
    return ids

# doc             current document
def GetUnusedGridHeadFamilies(doc):
    ''' this will return all ids of unused family symbols (types) of grid head families'''
    usedTypes = com.GetUsedUnusedTypeIds(doc, GetAllGridTypeIdsByCategory, 1, 8)
    headsInUseIds = []
    for Id in usedTypes:
        type = doc.GetElement(Id)
        id = com.GetBuiltInParameterValue(type, BuiltInParameter.GRID_HEAD_TAG)
        if (id != None and id not in headsInUseIds):
            headsInUseIds.append(id)
    allSymbolsInModel = GetAllGridHeadsByCategory(doc)
    unusedSymbolIds = []
    for  symbolInModel in  allSymbolsInModel:
        if(symbolInModel.Id not in headsInUseIds ):
            unusedSymbolIds.append(symbolInModel.Id)
    return unusedSymbolIds 

# doc             current document
def GetUnusedGridHeadFamiliesForPurge(doc):
    ''' this will return all ids of unused grid head symbols and families to be purged'''
    return rFamU.GetUnusedInPlaceIdsForPurge(doc, GetUnusedGridHeadFamilies)