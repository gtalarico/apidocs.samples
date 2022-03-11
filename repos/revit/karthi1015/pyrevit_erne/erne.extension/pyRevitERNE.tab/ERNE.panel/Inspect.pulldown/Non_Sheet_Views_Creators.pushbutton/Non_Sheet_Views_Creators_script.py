"""
Lists views not on sheets
"""
import clr
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import FilteredElementCollector as Fec
from Autodesk.Revit.DB import ViewType, View
from rpw import doc
from rph.worksharing import get_elem_creator

views = Fec(doc).OfClass(View).WhereElementIsNotElementType().ToElements()

plan_views = []
not_sheeted_views = {}

for view in views:
    if not view.IsTemplate:
        if view.ViewType == ViewType.AreaPlan:
            plan_views.append(view)
        elif view.ViewType == ViewType.CeilingPlan:
            plan_views.append(view)
        elif view.ViewType == ViewType.Detail:
            plan_views.append(view)
        elif view.ViewType == ViewType.DraftingView:
            plan_views.append(view)
        elif view.ViewType == ViewType.Elevation:
            plan_views.append(view)
        elif view.ViewType == ViewType.FloorPlan:
            plan_views.append(view)
        elif view.ViewType == ViewType.Section:
            plan_views.append(view)

for view in plan_views:
    sheet_numbers = view.GetParameters("Sheet Number")
    for number in sheet_numbers:
        if number.AsString() == "---":
            not_sheeted_views[view.Name] = get_elem_creator(view)

for view_name, creator in not_sheeted_views.items():
    print(view_name, creator)

print("{} views not on sheets".format(not_sheeted_views))
