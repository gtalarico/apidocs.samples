"""
Lists skewed view directions
"""
from Autodesk.Revit.DB import View, ViewType
from Autodesk.Revit.DB import FilteredElementCollector as Fec
from rpw import doc


def print_view_stats(view, view_dir, up_dir, right_dir):
    print("_" * 50)
    print(view.Name)
    print(view.ViewType)
    print("is view template: " + str(view.IsTemplate))
    print("Id: " + str(view.Id.IntegerValue))
    print(view_dir)
    print(view_dir[0])
    print(up_dir)
    print(up_dir[0])
    print(right_dir)
    print(right_dir[0])


views = Fec(doc).OfClass(View).WhereElementIsNotElementType().ToElements()

for i, view in enumerate(views):
    if not view.IsTemplate:
        if view.ViewType != ViewType.ThreeD:

            v_vw_dir = view.ViewDirection
            v_up_dir = view.UpDirection
            v_ri_dir = view.RightDirection

            if not v_up_dir[0].is_integer():
                print_view_stats(view, v_vw_dir, v_up_dir, v_ri_dir)

            elif not v_ri_dir[0].is_integer():
                print_view_stats(view, v_vw_dir, v_up_dir, v_ri_dir)
