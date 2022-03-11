#
#License:
#
#
# Revit Batch Processor Sample Code
#
# Copyright (c) 2020  Jan Christel
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
import Result as res

# import Autodesk
from Autodesk.Revit.DB import *

clr.ImportExtensions(System.Linq)

# ------------------------------------------------ DELETE LINE PATTERNS ----------------------------------------------

# deletes all line patterns where the names contains a provided string
def DeleteLinePatternsContains(doc, contains):
    lps = FilteredElementCollector(doc).OfClass(LinePatternElement).ToList()
    ids = list(lp.Id for lp in lps if lp.GetLinePattern().Name.Contains(contains)).ToList[ElementId]()
    result = com.DeleteByElementIds(doc,ids, 'Deleting line patterns where name contains: ' + str(contains),'line patterns containing: ' + str(contains))
    return result

# deletes all line patterns where the name starts with provided string
def DeleteLinePatternStartsWith(doc, startsWith):
    lps = FilteredElementCollector(doc).OfClass(LinePatternElement).ToList()
    ids = list(lp.Id for lp in lps if lp.GetLinePattern().Name.StartsWith(startsWith)).ToList[ElementId]()
    result = com.DeleteByElementIds(doc,ids, 'Delete line patterns where name starts with: ' + str(startsWith),'line patterns starting with: ' + str(startsWith))
    return result

# deletes all line patterns where the name does not contain the provided string
def DeleteLinePatternsWithout(doc, contains):
    lps = FilteredElementCollector(doc).OfClass(LinePatternElement).ToList()
    ids = list(lp.Id for lp in lps).ToList[ElementId]()
    idsContain = list(lp.Id for lp in lps if lp.GetLinePattern().Name.Contains(contains)).ToList[ElementId]()
    deleteids = list(set(ids)-set(idsContain))
    result = com.DeleteByElementIds(doc,deleteids, 'Delete line patterns where name does not contain: ' + str(contains),'line patterns without: ' + str(contains))
    return result

# return all line patterns in the model
# doc:      curren document
def GetAllLinePatterns(doc):
    return FilteredElementCollector(doc).OfClass(LinePatternElement).ToList()


# doc     current model document
def BuildPatternsDictionaryByName(doc):
    '''builds a dictionary wher line pattern name is key, values are all ids of line patterns with the exact same name'''
    lpDic = {}
    lps = FilteredElementCollector(doc).OfClass(LinePatternElement)
    for lp in lps:
        if(lpDic.has_key(lp.GetLinePattern().Name)):
            lpDic[lp.GetLinePattern().Name].append(lp.Id)
        else:
            lpDic[lp.GetLinePattern().Name] = [lp.Id]
    return lpDic

# doc     current model document
def DeleteDuplicatLinePatterNames(doc):
    '''deletes all but the first line pattern by Id with the exact same name'''
    returnvalue = res.Result()
    returnvalue.AppendMessage('Deletes all but the first line pattern by Id with the exact same name...start')
    # get a dictionary: Key pattern name, value all ids of line patterns with the same name
    # anything where the value list is greate then 1 means duplicates of the same name...
    linePatterns = BuildPatternsDictionaryByName(doc)
    for key, value in linePatterns.items():
        if(len(value) > 1):
            # keep the first one (original)
            value.remove(value[0])
            flagDelete = com.DeleteByElementIds(doc,value, 'Deleting duplicate line patterns names: ' + str(key),'line patterns duplicates: ' + str(key))
            returnvalue.Update (flagDelete)
    return returnvalue

# ------------------------------------------------ DELETE LINE STYLES ----------------------------------------------

# deletes all line styles where the name starts with provided string
def DeleteLineStylesStartsWith(doc, startsWith):
    lc = doc.Settings.Categories[BuiltInCategory.OST_Lines]
    ids = list(c.Id for c in lc.SubCategories if c.Name.StartsWith(startsWith)).ToList[ElementId]()
    result = com.DeleteByElementIds(doc,ids, 'Delete line styles where name starts with: ' + str(startsWith),'line styles starting with: ' + str(startsWith))
    return result

# return all line styles ids in the model
# doc:      curren document
def GetAllLineStyleIds(doc):
    lc = doc.Settings.Categories[BuiltInCategory.OST_Lines]
    ids = list(c.Id for c in lc.SubCategories).ToList[ElementId]()
    return ids

# ------------------------------------------------ Fill Patterns ----------------------------------------------

# return all fill pattern ids in the model
# doc:      curren document
def GetAllFillPattern(doc):
    return FilteredElementCollector(doc).OfClass(FillPatternElement).ToList()