"""Randomly assign colors to rooms based on a selected parameter"""

__title__ = 'Color Rooms\nper Param'
__author__ = 'Petar Mitev'

import sys
pyt_path = r'C:\Program Files (x86)\IronPython 2.7\Lib'
sys.path.append(pyt_path)
import clr

#random
import random
from random import randint

import clr
# Import RevitAPI
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import *

# Import RPW
import rpw
from rpw import revit, db, ui, DB, UI
from rpw.db.element import Element

#document
doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument

#ui
search_param = rpw.ui.forms.TextInput('Input Parameter', default='Department Class', description='Enter a Parameter', sort=True, exit_on_close=True)

#import module for colors
def randColor():
    rand_color = Color(random.randrange(0, 256), random.randrange(0, 256), random.randrange(0, 256))
    return rand_color

#collect rooms
room_collector = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Rooms).WhereElementIsNotElementType()

rooms =[]
unique_departments = []

#check the rooms for department parameter
for room in room_collector:
    department_param = room.LookupParameter(search_param)

    #if there is a department parameter, add it to a list
    if department_param.AsString != None:
        rooms.append(room)

    if department_param.AsString() not in unique_departments:
        unique_departments.append(department_param.AsString())

#colors
graphics_overrides = {}
colors = []

#get hatch pattern from Revit API
ftarget = FillPatternTarget.Drafting
solid_fill = FillPatternElement.GetFillPatternElementByName(doc, ftarget, "Solid fill")

#generate colors based on departments
for d in unique_departments:
    color = randColor()
    graphics_overrides[d] = OverrideGraphicSettings()
    graphics_overrides[d].SetProjectionFillColor(color)
    graphics_overrides[d].SetProjectionFillPatternId(solid_fill.Id)

#transaction start
t = Transaction(doc, "Color Override Rooms")
t.Start()

view = doc.ActiveView

#assign colors
for room in rooms:
    d = room.LookupParameter(search_param).AsString()
    view.SetElementOverrides(room.Id, graphics_overrides[d])

t.Commit()
t.Dispose()