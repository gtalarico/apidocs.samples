import clr
clr.AddReference('RevitAPI')
from Autodesk.Revit.DB import *

clr.AddReference("RevitNodes")
import Revit

def GetDependentViews(view):
	return [view.Document.GetElement(x) for x in view.GetDependentViewIds()]

views = UnwrapElement(IN[0])

if isinstance(IN[0], list):
	OUT = [GetDependentViews(x) for x in views]
else:
	OUT = GetDependentViews(views)