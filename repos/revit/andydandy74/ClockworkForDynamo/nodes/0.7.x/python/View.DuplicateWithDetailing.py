import clr
clr.AddReference('RevitAPI')
from Autodesk.Revit.DB import *
import Autodesk

clr.AddReference("RevitServices")
import RevitServices
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

doc = DocumentManager.Instance.CurrentDBDocument
views = UnwrapElement(IN[0])
elementlist = list()
dupopt = Autodesk.Revit.DB.ViewDuplicateOption.WithDetailing

TransactionManager.Instance.EnsureInTransaction(doc)
for view in views:
	newview = view.Duplicate(dupopt)
	elementlist.append(doc.GetElement(newview))
TransactionManager.Instance.TransactionTaskDone()
	
OUT = elementlist