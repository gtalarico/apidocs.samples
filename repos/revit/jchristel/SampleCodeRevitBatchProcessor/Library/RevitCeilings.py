﻿#
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
import RevitFamilyUtils as rFam
import RevitGeometry as rGeo
import RevitDesignSetOptions as rDesignO
import DataCeiling as dCeiling
import Utility as util
import DataGeometry as dGeometry


# import Autodesk
from Autodesk.Revit.DB import *

clr.ImportExtensions(System.Linq)

# -------------------------------------------- common variables --------------------
# header used in reports
REPORT_CEILINGS_HEADER = ['HOSTFILE', 'CEILINGTYPEID', 'CEILINGTYPENAME']

COMPOUND_CEILING_FAMILY_NAME = 'Compound Ceiling'
BASIC_CEILING_FAMILY_NAME = 'Basic Ceiling'
ROOF_SOFFIT_FAMILY_NAME = 'Roof Soffit'

BUILTIN_CEILING_TYPE_FAMILY_NAMES = [
    COMPOUND_CEILING_FAMILY_NAME,
    BASIC_CEILING_FAMILY_NAME,
    ROOF_SOFFIT_FAMILY_NAME
]

# --------------------------------------------- utility functions ------------------

# doc:   current model document
def GetAllCeilingTypesByCategory(doc):
    ''' this will return a filtered element collector of all ceiling types in the model:
    - Compound Ceiling
    - In place families or loaded families
    - Basic Ceiling
    it will therefore not return any in roof soffit types ..
    '''
    collector = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Ceilings).WhereElementIsElementType()
    return collector

# doc   current model document
def GetCeilingTypesByClass(doc):
    ''' this will return a filtered element collector of all ceiling types in the model:
    - Roof Soffit
    - Compound Ceiling
    - Basic Ceiling
    it will therefore not return any in place family types ...'''
    return  FilteredElementCollector(doc).OfClass(CeilingType)

# collector   filtered element collector containing ceiling type elments of family symbols representing in place families
# dic         dictionary containing key: ceiling type family name, value: list of ids
def BuildCeilingTypeDictionary(collector, dic):
    '''returns the dictioanry passt in with keys and or values added retrieved from collector passt in'''
    for c in collector:
        if(dic.has_key(c.FamilyName)):
            if(c.Id not in dic[c.FamilyName]):
                dic[c.FamilyName].append(c.Id)
        else:
            dic[c.FamilyName] = [c.Id]
    return dic

# doc   current model document
def SortCeilingTypesByFamilyName(doc):
    # get all ceiling Type Elements
    wts = GetCeilingTypesByClass(doc)
    # get all ceiling types including in place ceiling families
    wts_two = GetAllCeilingTypesByCategory(doc)
    usedWts = {}
    usedWts = BuildCeilingTypeDictionary(wts, usedWts)
    usedWts = BuildCeilingTypeDictionary(wts_two, usedWts)
    return usedWts

# -------------------------------- none in place ceiling types -------------------------------------------------------

# doc   current model document
def GetAllCeilingInstancesInModelByCategory(doc):
    ''' returns all ceiling elements placed in model...ignores roof soffits'''
    return FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Ceilings).WhereElementIsNotElementType()
    
# doc   current model document
def GetAllCeilingInstancesInModelByClass(doc):
    ''' returns all ceiling elements placed in model...ignores in place'''
    return FilteredElementCollector(doc).OfClass(Ceiling).WhereElementIsNotElementType()

# doc   current model document
def GetAllCeilingTypeIdsInModelByCategory(doc):
    ''' returns all ceiling element type ids available placed in model '''
    ids = []
    colCat = GetAllCeilingTypesByCategory(doc)
    ids = com.GetIdsFromElementCollector(colCat)
    return ids

# doc   current model document
def GetAllCeilingTypeIdsInModelByClass(doc):
    ''' returns all ceiling element type ids available in model '''
    ids = []
    colClass = GetCeilingTypesByClass(doc)
    ids = com.GetIdsFromElementCollector(colClass)
    return ids

# doc   current document
def GetUsedCeilingTypeIds(doc):
    ''' returns all used in ceiling type ids '''
    ids = com.GetUsedUnusedTypeIds(doc, GetAllCeilingTypeIdsInModelByCategory, 1)
    return ids

# famTypeIds        symbol(type) ids of a family
# usedTypeIds       symbol(type) ids in use in a project
def FamilyNoTypesInUse(famTypeIds,unUsedTypeIds):
    ''' returns false if any symbols (types) of a family are in use in a model'''
    match = True
    for famTypeId in famTypeIds:
        if (famTypeId not in unUsedTypeIds):
            match = False
            break
    return match
 
# doc   current document
def GetUnusedNonInPlaceCeilingTypeIdsToPurge(doc):
    ''' returns all unused ceiling type ids for:
    - Roof Soffit
    - Compound Ceiling
    - Basic Ceiling
    it will therefore not return any in place family types ...'''
    # get unused type ids
    ids = com.GetUsedUnusedTypeIds(doc, GetAllCeilingTypeIdsInModelByClass, 0)
    # make sure there is at least on ceiling type per system family left in model
    ceilingTypes = SortCeilingTypesByFamilyName(doc)
    for key, value in ceilingTypes.items():
        if(key in BUILTIN_CEILING_TYPE_FAMILY_NAMES):
            if(FamilyNoTypesInUse(value,ids) == True):
                # remove one type of this system family from unused list
                ids.remove(value[0])
    return ids
 
# -------------------------------- In place ceiling types -------------------------------------------------------

# doc   current document
def GetInPlaceCeilingFamilyInstances(doc):
    ''' returns all instances in place families of category ceiling'''
    # built in parameter containing family name when filtering familyInstance elements:
    # BuiltInParameter.ELEM_FAMILY_PARAM
    # this is a faster filter in terms of performance then LINQ query refer to:
    # https://jeremytammik.github.io/tbc/a/1382_filter_shortcuts.html
    filter = ElementCategoryFilter(BuiltInCategory.OST_Ceilings)
    return FilteredElementCollector(doc).OfClass(FamilyInstance).WherePasses(filter)

# doc   current document
def GetAllInPlaceCeilingTypeIdsInModel(doc):
    ''' returns type ids off all available in place families of category ceiling'''
    ids = rFam.GetAllInPlaceTypeIdsInModelOfCategory(doc, BuiltInCategory.OST_Ceilings)
    return ids

# doc   current document
def GetUsedInPlaceCeilingTypeIds(doc):
    ''' returns all used in place type ids '''
    ids = com.GetUsedUnusedTypeIds(doc, GetAllInPlaceCeilingTypeIdsInModel, 1)
    return ids

# doc   current document
def GetUnusedInPlaceCeilingTypeIds(doc):
    ''' returns all unused in place type ids '''
    ids = com.GetUsedUnusedTypeIds(doc, GetAllInPlaceCeilingTypeIdsInModel, 0)
    return ids

# doc   current document
def GetUnusedInPlaceCeilingIdsForPurge(doc):
    '''returns symbol(type) ids and family ids (when no type is in use) of in place ceiling familis which can be purged'''
    ids = rFam.GetUnusedInPlaceIdsForPurge(doc, GetUnusedInPlaceCeilingTypeIds)
    return ids

# -------------------------------- ceiling geometry -------------------------------------------------------

# ceiling       Revit Ceiling element
def Get2DPointsFromRevitCeiling(ceiling):
    '''
    Returns a list of lists of points representing the flattened(2D geometry) of the ceiling
    List of Lists because a ceiling can be made up of multiple sketches. Each nested list represents one ceiling sketch.
    Does not work with in place ceilings
    '''
    allCeilingPoints = []
    # get geometry from ceiling
    opt = Options()
    fr1_geom = ceiling.get_Geometry(opt)
    solids = []
    # check geometry for Solid elements
    # todo check for FamilyInstance geometry ( in place families!)
    for item in fr1_geom:
        if(type(item) is Solid):
            solids.append(item)
   
    # process solids to points 
    # in place families may have more then one solid
    for s in solids:
        pointPerCeilings = rGeo.ConvertSolidToFlattened2DPoints(s)
        if(len(pointPerCeilings) > 0):
            for pLists in pointPerCeilings:
                allCeilingPoints.append(pLists)
    return allCeilingPoints

# doc       current model document
def Get2DPointsFromRevitCeilingsInModel(doc):
    '''
    Returns a list of lists of points representing the flattened(2D geometry) of each ceiling in the model
    List of Lists because a ceiling can be made up of multiple sketches. Each nested list represents one ceiling sketch.
    Does not work with in place ceilings
    '''
    ceilingInstances =  GetAllCeilingInstancesInModelByCategory(doc)
    allCeilingPoints = []
    for cI in ceilingInstances:
       ceilingPoints = Get2DPointsFromRevitCeiling(cI)
       if(len(ceilingPoints) > 0 ):
           allCeilingPoints.append (ceilingPoints)
    return allCeilingPoints

# -------------------------------- ceiling data -------------------------------------------------------

# doc       current model document
def GetAllCeilingData(doc):
    '''
    returns a list of ceiling data objects for each ceiling element in the model
    '''
    allCeilingData = []
    ceilings = GetAllCeilingInstancesInModelByCategory(doc)
    for ceiling in ceilings:
        cd = PopulateDataCeilingObject(doc, ceiling)
        if(cd is not None):
            allCeilingData.append(cd)
    return allCeilingData

# doc                   current revit document
# revitCeiling          Revit ceiling element
def PopulateDataCeilingObject(doc, revitCeiling):
    '''
    returns a custom ceiling data objects populated with some data from the revit model ceiling passt in
    '''
    # set up data class object
    dataC = dCeiling.DataCeiling() 
    # get ceiling geometry (boundary points)
    revitGeometryPointGroups = Get2DPointsFromRevitCeiling(revitCeiling)
    if(len(revitGeometryPointGroups) > 0):
        ceilingPointGroupsAsDoubles = []
        for allCeilingPointGroups in revitGeometryPointGroups:
            dgeoConverted = rGeo.ConvertXYZInDataGeometry(doc, allCeilingPointGroups)
            ceilingPointGroupsAsDoubles.append(dgeoConverted)
        dataC.geometry = ceilingPointGroupsAsDoubles
        # get other data
        dataC.designSetAndOption = rDesignO.GetDesignSetOptionInfo(doc, revitCeiling)
        ceilingTypeId = revitCeiling.GetTypeId()
        ceilingType = doc.GetElement(ceilingTypeId)
        dataC.id = revitCeiling.Id.IntegerValue
        dataC.typeName = Element.Name.GetValue(revitCeiling).encode('utf-8')
        dataC.mark = com.GetBuiltInParameterValue(revitCeiling, BuiltInParameter.ALL_MODEL_MARK)  # need to get the mark here...
        dataC.typeMark = com.GetBuiltInParameterValue(ceilingType, BuiltInParameter.ALL_MODEL_TYPE_MARK)
        dataC.levelName = Element.Name.GetValue(doc.GetElement(revitCeiling.LevelId)).encode('utf-8')
        dataC.levelId = revitCeiling.LevelId.IntegerValue
        dataC.offsetFromLevel = com.GetBuiltInParameterValue(revitCeiling, BuiltInParameter.CEILING_HEIGHTABOVELEVEL_PARAM)   # offset from level
        return dataC
    else:
        return None