﻿#!/usr/bin/python
# -*- coding: utf-8 -*-
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

# sample description
# how to report on grids and levels properties

# ---------------------------------
# default path locations
# ---------------------------------
# path to library modules
commonLibraryLocation_ = r'C:\temp'
# path to directory containing this script (in case there are any other modules to be loaded from here)
scriptLocation_ = r'C:\temp'
# debug mode revit project file name
debugRevitFileName_ = r'C:\temp\Test_grids.rvt'

import clr
import System

# set path to library and this script
import sys
sys.path += [commonLibraryLocation_, scriptLocation_]

# import common libraries
import RevitCommonAPI as com
import RevitGrids as rGrid
import RevitLevels as rLevel
import Utility as util

# autodesk API
from Autodesk.Revit.DB import *

clr.AddReference('System.Core')
clr.ImportExtensions(System.Linq)

# flag whether this runs in debug or not
debug_ = False

# Add batch processor scripting references
if not debug:
    import revit_script_util
    import revit_file_util
    clr.AddReference('RevitAPI')
    clr.AddReference('RevitAPIUI')
    # NOTE: these only make sense for batch Revit file processing mode.
    doc = revit_script_util.GetScriptDocument()
    revitFilePath_ = revit_script_util.GetRevitFilePath()
else:
    # get default revit file name
    revitFilePath_ = debugRevitFileName_

# -------------
# my code here:
# -------------

# output messages either to batch processor (debug = False) or console (debug = True)
def Output(message = ''):
    if not debug_:
        revit_script_util.Output(str(message))
    else:
        print (message)

# method writing out grid information
def writeGridData(doc, fileName):
    status = True
    try:
        status = util.writeReportData(
            fileName, 
            rGrid.REPORT_GRIDS_HEADER, 
            rGrid.GetGridReportData(doc, revitFilePath_))
    except Exception as e:
        status = False
        Output('Failed to write data file!' + fileName)
        Output (str(e))
    return status

# method writing out level information
def writeLevelData(doc, fileName):
    status = True
    try:
        status = util.writeReportData(
            fileName, 
            rLevel.REPORT_LEVELS_HEADER, 
            rLevel.GetLevelReportData(doc, revitFilePath_))
    except Exception as e:
        status = False
        Output('Failed to write data file!' + fileName)
        Output (str(e))
    return status

# -------------
# main:
# -------------

# store output here:
rootPath_ = r'C:\temp'

# build output file names
fileNameGrid_ = rootPath_ + '\\'+ util.GetOutPutFileName(revitFilePath_,'.txt', '_grids')
fileNameLevel_ = rootPath_ + '\\'+ util.GetOutPutFileName(revitFilePath_,'.txt', '_levels')

#write out grid data
Output('Writing Grid Data.... start')
result_ = writeGridData(doc, fileNameGrid_)
Output('Writing Grid Data.... status: ' + str(result_))
Output('Writing Grid Data.... finished ' + fileNameGrid_)

#write out Level data
Output('Writing Level Data.... start')
result_ = writeLevelData(doc, fileNameLevel_)
Output('Writing Level Data.... status: ' + str(result_))
Output('Writing Level Data.... finished ' + fileNameLevel_)