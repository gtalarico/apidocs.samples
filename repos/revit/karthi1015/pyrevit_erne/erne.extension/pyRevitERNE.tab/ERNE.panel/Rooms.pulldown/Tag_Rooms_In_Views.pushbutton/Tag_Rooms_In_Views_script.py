"""
Creates a tag for each selected room or all rooms in view or all rooms in all selected views.
Tag type is chosen in dialog.
"""
import clr
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import FilteredElementCollector as Fec
from Autodesk.Revit.DB import BuiltInCategory as Bic
from Autodesk.Revit.DB import CurveArray, ElementId, Options
from Autodesk.Revit.DB import SpatialElementType, XYZ, UV, LinkElementId
from Autodesk.Revit.DB import SpatialElementBoundaryOptions, AreaVolumeSettings
from System.Collections.Generic import List
from System.Diagnostics import Stopwatch
import sys
import os.path as op
from rpw import doc, uidoc, db
from rpw.ui import forms
from rph import param

# DONE case1 active view project browser: tag rooms in selected views
# DONE case2 selection with rooms: tag those rooms
# DONE case3 no selection or active view: tag all rooms in view
# DONE make sure the room is not yet tagged
# DONE choose tag type in dialogue
# DONE set offsets


def get_boundaries_by_length(bound_segments):
    boundaries_by_lengths = {}
    for boundary_list in bound_segments:
        length = 0.0
        for boundary in boundary_list:
            length += boundary.GetCurve().Length
        boundaries_by_lengths[length] = boundary_list
    return boundaries_by_lengths


def get_room_boundaries(room, doc):
    bound_loc = AreaVolumeSettings.GetAreaVolumeSettings(doc).GetSpatialElementBoundaryLocation(SpatialElementType.Room)
    spat_opt = SpatialElementBoundaryOptions()
    spat_opt.SpatialElementBoundaryLocation = bound_loc
    bound_segments = room.GetBoundarySegments(spat_opt)
    if len(bound_segments) > 1:
        print("more than one boundary curve detected - using the longest one!")
    boundaries_by_length = get_boundaries_by_length(bound_segments)
    curve_arrays_by_length = {}
    for length, boundary_loop in boundaries_by_length.items():
        curve_array = CurveArray()
        for boundary in boundary_loop:
            curve_array.Append(boundary.GetCurve())
        curve_arrays_by_length[length] = curve_array
    return curve_arrays_by_length


def get_room_points(room_boundary):
    room_pts = []
    for crv in room_boundary:
        if crv.GetType().Name == "Arc":
            room_pts.extend(crv.Tessellate())
        else:
            room_pts.append(crv.GetEndPoint(0))
    # print(room_pts)
    return room_pts


def get_room_pt_closest_to_bbox_pt(room_pts, bbox_pt):
    points_by_distance = {}
    for pt in room_pts:
        points_by_distance[pt.DistanceTo(bbox_pt)] = pt
    closest_dist = min(sorted(points_by_distance))
    return points_by_distance[closest_dist]


def tag_room(room):
    room_bbox = room.get_BoundingBox(None)
    left_top_bbox = XYZ(room_bbox.Min.X, room_bbox.Max.Y, room_bbox.Min.Z)
    bbox_point = left_top_bbox
    room_boundaries = get_room_boundaries(room, doc)
    outer_room_boundary = room_boundaries[max(room_boundaries)]
    # print(outer_room_boundary, max(room_boundaries))
    room_points = get_room_points(outer_room_boundary)
    tag_pt = get_room_pt_closest_to_bbox_pt(room_points, bbox_point)
    # print("tagging room at: {}".format(tag_pt))
    tag = doc.Create.NewRoomTag(
        LinkElementId(room.Id),
        UV(tag_pt.X, tag_pt.Y) + tag_off_set,
        view.Id,
    )
    tag.RoomTagType = room_tag_types_by_name[selected_room_tag_type]
    return tag


stopwatch = Stopwatch()
stopwatch.Start()

active_view = doc.ActiveView
active_view_type_name = active_view.ViewType.ToString()
multi_view = False

selection     = [doc.GetElement(el_id) for el_id in uidoc.Selection.GetElementIds()]
selection_ids = [el_id for el_id in uidoc.Selection.GetElementIds()]
selected_ids  = List[ElementId](selection_ids)

if active_view_type_name == "ProjectBrowser":
    active_views = Fec(doc, selected_ids).OfCategory(Bic.OST_Views).ToElements()
    multi_view = True
else:
    active_views = [active_view]

if not active_views:
    sys.exit()

tag_off_set = UV(1.0, -2.0)

room_tag_types = Fec(doc).OfCategory(Bic.OST_RoomTags).WhereElementIsElementType().ToElements()
#room_tag_types_by_name = {rtt.LookupParameter("Typname").AsString():rtt.Id for rtt in room_tag_types}
room_tag_types_by_name = {"{} : {}".format(
    rtt.FamilyName,
    param.get_val(rtt, "type_name", bip=True),
    ):rtt for rtt in room_tag_types}
selected_room_tag_type = forms.SelectFromList('Select a RoomTag type', room_tag_types_by_name.keys())
# selected_room_tag_type_id = room_tag_types_by_name.keys()[0]


with db.Transaction("tag rooms"):
    for view in active_views:
        print("__________\nwould tag rooms in this view: {}".format(view.Name))
        if selected_ids and multi_view:
            rooms_in_view = Fec(doc, view.Id).OfCategory(Bic.OST_Rooms).ToElements()
            rooms_to_tag = rooms_in_view
        elif selected_ids and not multi_view:
            rooms_in_selection = Fec(doc, selected_ids).OfCategory(Bic.OST_Rooms).ToElements()
            rooms_to_tag = rooms_in_selection
        else:
            rooms_in_view = Fec(doc, view.Id).OfCategory(Bic.OST_Rooms).ToElements()
            rooms_to_tag = rooms_in_view

        view_room_tags = Fec(doc, view.Id).OfCategory(Bic.OST_RoomTags).WhereElementIsNotElementType().ToElements()
        tagged_room_ids = [t.Room.Id for t in view_room_tags if t.Room.Id]
        print("tagging {} rooms in this view:".format(len(rooms_to_tag)))

        for room in rooms_to_tag:
            if room.Id in tagged_room_ids:
                print("room {} already tagged - skipping it".format(room.Id))
                continue
            print(room.Number)
            tag_room(room)


print("Erne_pyRevit {} run in: ".format(op.basename(__file__)))
stopwatch.Stop()
timespan = stopwatch.Elapsed
print(timespan)
