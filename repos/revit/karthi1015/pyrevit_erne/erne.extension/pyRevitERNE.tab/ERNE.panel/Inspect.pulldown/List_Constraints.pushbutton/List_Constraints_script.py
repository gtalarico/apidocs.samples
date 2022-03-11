"""
Lists constraints in current model
"""
from Autodesk.Revit.DB import FilteredElementCollector as Fec
from Autodesk.Revit.DB import BuiltInCategory as Bic
from rpw import doc

constraints = Fec(doc).OfCategory(Bic.OST_Constraints).WhereElementIsNotElementType().ToElements()

for i, constraint in enumerate(constraints):
    print(50 * "_" + "{}:".format(i))
    print("{} constraint: between these elements: ".format(constraint.Id))
    for ref in constraint.References:
        category = doc.GetElement(ref.ElementId).Category.Name
        name = doc.GetElement(ref.ElementId).Name
        elem_id = ref.ElementId.IntegerValue
        print("{} - {} - {}".format(elem_id, category, name))

print(50 * "_")
print("{} constraints found in model.".format(constraints.Count))
