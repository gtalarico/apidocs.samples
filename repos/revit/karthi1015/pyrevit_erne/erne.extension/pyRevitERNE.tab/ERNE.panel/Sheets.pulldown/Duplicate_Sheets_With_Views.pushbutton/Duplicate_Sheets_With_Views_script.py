"""
Your active Sheet View with placed views will be duplicated.
If multiple sheets are selected in project browser, all of those get duplicated.
If view with name collision exist, this will not work - please clean them up first
"""

import clr
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import FilteredElementCollector as Fec
from Autodesk.Revit.DB import BuiltInCategory as Bic
from Autodesk.Revit.DB import ElementTransformUtils, XYZ, Viewport, ViewSheet, ViewType
from Autodesk.Revit.DB import ViewDuplicateOption, ScheduleSheetInstance
from rpw.ui.selection import Selection
from rpw.ui.forms import SelectFromList
from rpw import db, doc
from System.Diagnostics import Stopwatch
import os.path as op


def match_bbox(source, target, source_sheet, target_sheet):
    source_bbox = source.get_BoundingBox(source_sheet)
    orig_center = (source_bbox.Max + source_bbox.Min) / 2
    target_bbox = target.get_BoundingBox(target_sheet)
    new_center = (target_bbox.Max + target_bbox.Min) / 2
    return ElementTransformUtils.MoveElement(doc, target.Id,
                                             XYZ(orig_center.X - new_center.X, orig_center.Y - new_center.Y, 0))


def match_box_center(viewport_source, viewport_target):
    orig_center = viewport_source.GetBoxCenter()
    return viewport_target.SetBoxCenter(orig_center)


def dup_sheet_with_views(sheet):
    titleblocks = Fec(doc, sheet.Id).OfCategory(Bic.OST_TitleBlocks).ToElements()

    if len(titleblocks) == 1:
        print("ok, only one titleblock used. Attempt to duplicate sheet: {}".format(sheet.Name))

        new_sheet_name = sheet.Name
        new_sheet_number = sheet.SheetNumber + "_dup"

        placed_views = sheet.GetAllPlacedViews()
        viewports = Fec(doc, sheet.Id).OfClass(Viewport).ToElements()

        new_sheet = ViewSheet.Create(doc, titleblocks[0].GetTypeId())
        new_sheet.Name = new_sheet_name
        new_sheet.SheetNumber = new_sheet_number

        for view_id in placed_views:
            view = doc.GetElement(view_id)

            # legends -> only duplicate viewport
            if view.ViewType == ViewType.Legend:
                print(view.Name + " is a legend view -> only viewport gets duplicated")

                dup_view_id = view_id
                dup_view = view

            # non-legend plan views -> duplicate
            else:
                dup_view_name = view.Name + "_dup"
                print(view.Name + " is a non-legend plan view -> attempt to duplicate it as: {}".format(dup_view_name))
                print(view_id)
                dup_view_id = view.Duplicate(dup_opt)
                print(dup_view_id)
                dup_view = doc.GetElement(dup_view_id)
                dup_view.Name = dup_view_name

            for viewport in viewports:
                if viewport.ViewId == view.Id:
                    dup_viewport = Viewport.Create(doc, new_sheet.Id, dup_view_id, XYZ.Zero)
                    doc.Regenerate()
                    print("regenerating to get accurate viewport placement")

                    if int(doc.Application.VersionNumber) < 2017:
                        match_bbox(viewport, dup_viewport, sheet, new_sheet)
                    else:
                        match_box_center(viewport, dup_viewport)

                    orig_vp_type = viewport.GetTypeId()
                    dup_viewport.ChangeTypeId(orig_vp_type)

        # non-revision schedules -> only duplicate schedule instance
        placed_schedules = Fec(doc, sheet.Id).OfClass(
            ScheduleSheetInstance).WhereElementIsNotElementType().ToElements()

        for placed_schedule in placed_schedules:
            if not placed_schedule.IsTitleblockRevisionSchedule:
                print("placed schedule: {} -> only viewport gets duplicated".format(placed_schedule.Name))

                schedule_view = doc.GetElement(placed_schedule.ScheduleId)
                dup_schedule = ScheduleSheetInstance.Create(doc, new_sheet.Id, schedule_view.Id, XYZ.Zero)

                match_bbox(placed_schedule, dup_schedule, sheet, new_sheet)



active_view = doc.ActiveView

dup_opts = {
    "with detailing": ViewDuplicateOption.WithDetailing,
    "without detailing": ViewDuplicateOption.Duplicate,
    "as dependent": ViewDuplicateOption.AsDependent,
}
dup_opt = dup_opts[SelectFromList('Select Sheet Duplicate Mode', dup_opts.keys())]
selection = Selection()

stopwatch = Stopwatch()
stopwatch.Start()

if doc.ActiveView.ViewType.ToString() == "DrawingSheet":
    print(" active view is a sheet!")

    with db.Transaction('duplicate sheet with views'):
        if active_view.Category.Name == "Sheets":
            dup_sheet_with_views(active_view)
        else:
            print("an error occurred - your active view is a non-sheet view,"
                  "please retry focused on a sheet as active view.")

elif doc.ActiveView.ViewType.ToString() == "ProjectBrowser":
    with db.Transaction('duplicate sheets with views'):
        for elem in selection:
            if not elem.Category.Name == "Sheets":
                continue
            dup_sheet_with_views(doc.GetElement(elem.Id))

else:
    print("an error occurred - please retry focused on a sheet as active view.")

print("Erne_pyRevit {} run in: ".format(op.basename(__file__)))
stopwatch.Stop()
timespan = stopwatch.Elapsed
print(timespan)
