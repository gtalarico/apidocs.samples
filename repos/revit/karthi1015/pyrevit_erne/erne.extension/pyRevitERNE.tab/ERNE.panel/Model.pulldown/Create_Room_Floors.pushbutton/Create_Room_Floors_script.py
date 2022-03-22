"""
Creates a floor for each selected room or all rooms.
FloorType is selected from room parameter "Floor Finish" or first FloorType.
"""
import clr
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import FilteredElementCollector as Fec
from Autodesk.Revit.DB import BuiltInCategory as Bic
from Autodesk.Revit.DB import CurveArray, ElementId, Options, Line
from Autodesk.Revit.DB import SpatialElementType, JoinGeometryUtils
from Autodesk.Revit.DB import SpatialElementBoundaryOptions, AreaVolumeSettings
from Autodesk.Revit.DB import XYZ, Outline, BoundingBoxIntersectsFilter
from System.Collections.Generic import List
from System.Diagnostics import Stopwatch
from collections import defaultdict
from rpw import doc, uidoc, db
from rph import param, bbx


def create_floor(floor_boundary, floor_type, level, set_params=None):
    print("room {}: creating floor object".format(room_id))
    floor = doc.Create.NewFloor(
        floor_boundary,
        floor_type,
        level,
        STRUCTURAL,
    )
    if set_params:
        for key, val in set_params.items():
            # floor.get_Parameter(param.bip_map["comments"]).Set(comments)
            param.set_val(floor, key, val)
    return floor


def create_doors_floors(room, floor_type):
    door_floors = []
    room_level = doc.GetElement(room.LevelId)
    room_guid = room.UniqueId
    room_bbox = bbx.get(room)
    outline = Outline(room_bbox.Min, room_bbox.Max)
    cx_filter = BoundingBoxIntersectsFilter(outline)
    cx_filter.Tolerance = -0.1
    cx_elems = Fec(doc, door_ids).OfCategory(Bic.OST_Doors).WherePasses(cx_filter).ToElements()
    for cx_door in cx_elems:
        print(cx_door.Name)
        cx_door_id = cx_door.Id.IntegerValue

        exclude_door = param.get_val(cx_door, exclude_param_name)
        if exclude_door:
            print("door: {} to be excluded skipped!".format(cx_door_id))
            continue

        if cx_door_id not in door_ids_by_room[room_id.IntegerValue]:
            continue

        door_bbx = bbx.get(cx_door)
        wall = cx_door.Host
        wall_bbx = bbx.get(wall)
        combined_bbx = bbx.get_bbox_intersection(door_bbx, wall_bbx)
        z_min_pts = bbx.bbox_xy_zmin_points(combined_bbx)
        room_level_z_pts = [XYZ(pt.X, pt.Y, room_level.Elevation) for pt in z_min_pts]

        crv_array = CurveArray()
        last_pt = room_level_z_pts[-1]
        for pt in room_level_z_pts:
            # print(str(last_pt), str(pt))
            line = Line.CreateBound(last_pt, pt)
            last_pt = pt
            crv_array.Append(line)

        door_floor = create_floor(
            crv_array,
            floor_type,
            room_level,
            set_params={room_guid_param_name: room_guid},
        )
        door_floors.append(door_floor)

    return door_floors


def add_opening(floor, curve_array):
    opening = doc.Create.NewOpening(
        floor,
        curve_array,
        True,
    )
    return opening


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


stopwatch = Stopwatch()
stopwatch.Start()

# ::_Required_SP_:: T:YesNo; TI:Instance; G:Data; C:Doors, Rooms; SPG:GENERAL
exclude_param_name = "Exclude_from_floor_creation"
# ::_Required_SP_:: T:Text; TI:Instance; G:Data; C:Rooms; SPG:GENERAL
room_target_floor_type_param_name = "Floor_create_with_target_floor_type"
# ::_Required_SP_:: T:Text; TI:Instance; G:Data; C:Floors; SPG:GENERAL
room_guid_param_name = "Belongs_to_room"

last_phase = None
for phase in doc.Phases:
    last_phase = phase
print("using phase: {}".format(getattr(last_phase, "Name")))

selection = [doc.GetElement(el_id) for el_id in uidoc.Selection.GetElementIds()]
selection_ids = [el_id for el_id in uidoc.Selection.GetElementIds()]
selected_ids = List[ElementId](selection_ids)

if not selection:
    floor_rooms = Fec(doc).OfCategory(Bic.OST_Rooms).ToElements()
else:
    floor_rooms = Fec(doc, selected_ids).OfCategory(Bic.OST_Rooms).ToElements()

STRUCTURAL = False
geo_opt = Options()

doors = Fec(doc).OfCategory(Bic.OST_Doors ).WhereElementIsNotElementType().ToElements()
door_ids = List[ElementId]([door.Id for door in doors])
door_bboxes_by_id = {door.Id.IntegerValue:bbx.get(door) for door in doors}

floors = Fec(doc).OfCategory(Bic.OST_Floors).WhereElementIsNotElementType().ToElements()
#floors_by_room_guid = {fl.get_Parameter(param.bip_map["comments"]).AsString(): fl for fl in floors}
floors_by_room_guid = defaultdict(list)
for floor in floors:
    # floor_belongs_to_room_guid = floor.get_Parameter(param.bip_map["comments"]).AsString()
    floor_belongs_to_room_guid = param.get_val(floor, room_guid_param_name)
    if floor_belongs_to_room_guid:
        floors_by_room_guid[floor_belongs_to_room_guid].append(floor)

floor_types = Fec(doc).OfCategory(Bic.OST_Floors).WhereElementIsElementType().ToElements()
floor_types_by_name = {ft.get_Parameter(param.bip_map["type_name"]).AsString(): ft for ft in floor_types}

floor_openings_to_add = defaultdict(list)

door_ids_by_room = defaultdict(list)
use = "FromRoom" # "ToRoom"

for door in doors:
    door_room = getattr(door, use)[last_phase]
    if not door_room:
        continue
    door_ids_by_room[door_room.Id.IntegerValue].append(door.Id.IntegerValue)


print("processing {} rooms.".format(len(floor_rooms)))

with db.Transaction("create/update:room_floors,door_floors"):
    for room in floor_rooms:
        print(35 * "-")
        room_id = room.Id
        room_guid = room.UniqueId
        room_level = doc.GetElement(room.LevelId)
        room_boundaries = get_room_boundaries(room, doc)
        room_excluded = param.get_val(room, exclude_param_name)
        if room_excluded:
            print("room {} skipped!!: excluded by parameter {}".format(room_id, exclude_param_name))
            continue
        if not room_boundaries:
            print("room {} skipped!!: no room boundaries found creating floor object".format(room_id))
            continue
        longest_room_boundary = room_boundaries[max(room_boundaries.keys())]
        # target_floor_type_from_room = room.get_Parameter(param.bip_map["room_floor_finish"]).AsString()
        target_floor_type_from_room = param.get_val(room, room_target_floor_type_param_name)

        target_floor_type = floor_types[0]
        # print(room_guid, floors_by_room_guid.get(room_guid))

        if room_guid in floors_by_room_guid:
            existing_room_floors = floors_by_room_guid[room_guid]
            print("room {}: floor for this room already exists - replacing it.".format(room_id))
            # could we instead just update? replace floor curve loop(s)?
            # https://thebuildingcoder.typepad.com/blog/2008/11/editing-a-floor-profile.html
            # this adds only floor openings not additional curve_arrays
            # https://thebuildingcoder.typepad.com/blog/2013/07/create-a-floor-with-an-opening-or-complex-boundary.html
            # -> Jeremy: "There is no way to create an exact copy of a floor with holes using API as in the UI."
            for ex_floor in existing_room_floors:
                doc.Delete(ex_floor.Id)

        if target_floor_type_from_room:
            print("room {}: found floor finish: {}".format(room_id, target_floor_type_from_room))
            if floor_types_by_name.get(target_floor_type_from_room):
                print("found appropriate floor type: {}".format(target_floor_type_from_room))
                target_floor_type = floor_types_by_name[target_floor_type_from_room]

        if longest_room_boundary:
            new_room_floor = create_floor(
                longest_room_boundary,
                target_floor_type,
                room_level,
                set_params={room_guid_param_name: room_guid},
            )
            door_floors = create_doors_floors(
                room,
                target_floor_type,
            )
        doc.Regenerate()

        if door_floors and new_room_floor:
            for door_floor in door_floors:
                print("room_floor joined {} with door_floor {}".format(new_room_floor.Id, door_floor.Id))
                JoinGeometryUtils.JoinGeometry(doc, new_room_floor, door_floor)

        if len(room_boundaries) > 1:
            opening_curve_array_lengths = sorted(room_boundaries.keys())[:-1]
            opening_curve_arrays = [room_boundaries[l] for l in opening_curve_array_lengths]
            for curve_array in opening_curve_arrays:
                floor_openings_to_add[new_room_floor].append(curve_array)

with db.Transaction("add_floor_openings"):
    for room in floor_rooms:
        room_id = room.Id
        print("room {}: adding openings:".format(room_id))
        for floor, openings in floor_openings_to_add.items():
            print(35 * "-")
            print("to floor: {}".format(floor.Id.IntegerValue))
            for curve_array in openings:
                add_opening(floor, curve_array)

print("\n{} updated {} floor rooms in: ".format(__file__, len(floor_rooms)))

stopwatch.Stop()
print(stopwatch.Elapsed)
