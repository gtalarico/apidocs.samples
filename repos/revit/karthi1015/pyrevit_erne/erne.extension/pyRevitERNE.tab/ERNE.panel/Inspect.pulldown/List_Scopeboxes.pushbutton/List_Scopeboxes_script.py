"""
Lists scope boxes in project
"""
# -*- coding: utf-8 -*-
from Autodesk.Revit.DB import FilteredElementCollector as Fec
from Autodesk.Revit.DB import BuiltInCategory as Bic
from rpw import doc, uidoc
from rph.worksharing import get_elem_creator

selection = [doc.GetElement(elId) for elId in uidoc.Selection.GetElementIds()]

scopeboxes = Fec(doc).OfCategory(Bic.OST_VolumeOfInterest).WhereElementIsNotElementType().ToElements()
scopeboxes_by_name = {}

for scopebox in scopeboxes:
    scopeboxes_by_name[scopebox.Name] = scopebox

for name in sorted(scopeboxes_by_name):
    creator = get_elem_creator(scopeboxes_by_name[name])
    info = "Scopebox: {} created by:{}".format(
        str(name).rjust(30),
        creator.rjust(15),
    )
    print(info)
