import clr
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import WorksetKind
from Autodesk.Revit.DB import FilteredWorksetCollector as Fwc
from rpw import doc


def get_map(by_id=False):
    if by_id:
        ws_map = {ws.Id:   ws for ws in Fwc(doc).OfKind(WorksetKind.UserWorkset).ToWorksets()}
    else:
        ws_map = {ws.Name: ws for ws in Fwc(doc).OfKind(WorksetKind.UserWorkset).ToWorksets()}
    return ws_map


def get_id(name):
    for ws in Fwc(doc).OfKind(WorksetKind.UserWorkset).ToWorksets():
        if name == ws.Name:
            return ws.Id.IntegerValue
