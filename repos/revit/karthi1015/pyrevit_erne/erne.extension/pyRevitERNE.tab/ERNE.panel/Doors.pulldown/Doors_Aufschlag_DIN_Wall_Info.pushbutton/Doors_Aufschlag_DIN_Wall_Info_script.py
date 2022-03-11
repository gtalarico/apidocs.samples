"""
set Aufschlagrichtung_DIN parameter on all appropriate doors
"""
from Autodesk.Revit.DB import BuiltInCategory as Bic
from Autodesk.Revit.DB import FilteredElementCollector as Fec
from System.Diagnostics import Stopwatch
from rpw import doc, db
from rph import param

stopwatch = Stopwatch()
stopwatch.Start()

family_hinges_side   = "Operation"
# ::_Required_SP_:: T:Text; TI:Instance; G:Data; C:Doors; SPG:GENERAL
instance_hinges_side_DIN = "Opening_side_DIN"
# ::_Required_SP_:: T:Text; TI:Instance; G:Data; C:Floors,Walls,Rooms,Doors,Windows; SPG:GENERAL
rvt_id = "Revit_Id"

hinges_side = {
    "L": "L",
    "R": "R",
    "LEFT" : "L",
    "RIGHT": "R",
    "-": "-",
}
mirrored_hinges_side = {
    "L": "R",
    "R": "L",
    "LEFT" : "R",
    "RIGHT": "L",
    "-": "-",
}
doors = Fec(doc).OfCategory(Bic.OST_Doors).WhereElementIsNotElementType().ToElements()

with db.Transaction('doors Aufschlagrichtung_DIN'):
    for door in doors:
        default_hinges_side = param.get_val(door.Symbol, family_hinges_side)
        default_hinges_side = default_hinges_side.split("_")[-1]
        if not default_hinges_side:
            continue

        door_type = doc.GetElement(door.GetTypeId())
        door_instance_is_mirrored = door.Mirrored
        print("________\ndoor_id: {} family hinges side: {}".format(
            door.Id, default_hinges_side))

        if door_instance_is_mirrored:
            side_value_DIN =          hinges_side.get(default_hinges_side) or ""
            print("is mirrored, instance hinges side: {}".format(side_value_DIN))

        else:
            side_value_DIN = mirrored_hinges_side.get(default_hinges_side) or ""
            print("not mirrored, instance hinges side: {}".format(side_value_DIN))

        param.set_val(door, instance_hinges_side_DIN, side_value_DIN)
        param.set_val(door, rvt_id, str(door.Id.IntegerValue))

        if door.Host:
            host_type = doc.GetElement(door.Host.GetTypeId())
            host_wall_description = param.get_val(host_type, "Description")
            if host_wall_description:
                print(host_wall_description)
                param.set_val(door, "Wandtyp", host_wall_description)

print("{} updated in: ".format(__file__))

stopwatch.Stop()
print(stopwatch.Elapsed)
