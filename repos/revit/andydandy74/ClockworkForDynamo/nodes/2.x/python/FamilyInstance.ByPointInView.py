import clr
clr.AddReference('RevitAPI')
from Autodesk.Revit.DB import *

clr.AddReference("RevitNodes")
import Revit
clr.ImportExtensions(Revit.Elements)
clr.ImportExtensions(Revit.GeometryConversion)

clr.AddReference("RevitServices")
import RevitServices
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

doc = DocumentManager.Instance.CurrentDBDocument
points = UnwrapElement(IN[0])
famtype = UnwrapElement(IN[1])
lvl = UnwrapElement(IN[2])
elementlist = list()
counter = 0

TransactionManager.Instance.EnsureInTransaction(doc)
# make sure familysymbol is active
if famtype.IsActive == False:
	famtype.Activate()
	doc.Regenerate()
for point in points:
	newobj = doc.Create.NewFamilyInstance(point.ToXyz(),famtype,lvl)
	elementlist.append(newobj.ToDSType(False))
TransactionManager.Instance.TransactionTaskDone()
OUT = elementlist