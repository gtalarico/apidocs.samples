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
import Result as res
import Utility as util

# import Autodesk
from Autodesk.Revit.DB import *

clr.ImportExtensions(System.Linq)

# -------------------------------------------- common variables --------------------
# header used in reports
REPORT_WARNINGS_HEADER = ['HOSTFILE','ID', 'NAME', 'WARNING TYPE', 'NUMBER OF WARNINGS']

# --------------------------------------------- utility functions ------------------


# doc   current document
def GetWarnings(doc):
    '''returns a list of warnings from the model'''
    return doc.GetWarnings()

# doc   current document
# guid of failure definitions of which to return the warning of
def GetWarningsByGuid(doc, guid):
    '''returns al failur message objects where failure definition has matching GUID'''
    filteredWarnings = []
    warnings = doc.GetWarnings()
    for warning in warnings:
        if(str(warning.GetFailureDefinitionId().Guid) == guid):
            filteredWarnings.append(warning)
    return filteredWarnings

