import clr
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import WorksharingUtils
from rpw import doc as DOC


def get_elem_creator(elem, doc=None, elem_id=None):
    if not doc:
        doc = DOC
    if not elem_id:
        elem_id = elem.Id
    return WorksharingUtils.GetWorksharingTooltipInfo(doc, elem_id).Creator

