# Activer la prise en charge de Python et charger la bibliothèque DesignScript
import clr
clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *

clr.AddReference('RevitAPI')
import Autodesk
from Autodesk.Revit.DB import *

clr.AddReference('RevitAPIUI')
from Autodesk.Revit.UI import *
from Autodesk.Revit.UI.Selection import *

clr.AddReference('RevitServices')
import RevitServices
from RevitServices.Persistence import DocumentManager

doc = DocumentManager.Instance.CurrentDBDocument
uiapp = DocumentManager.Instance.CurrentUIApplication
app = uiapp.Application
uidoc = uiapp.ActiveUIDocument

clr.AddReference('RevitNodes')
import Revit
clr.ImportExtensions(Revit.Elements)

ueWrapper = None
wrappers = clr.GetClrType(Revit.Elements.ElementWrapper).GetMethods()
for w in wrappers:
	if w.ToString().startswith("Revit.Elements.UnknownElement"):
		ueWrapper = w
		break

currentSel = uidoc.Selection
out = []
debug = []
selectElemId = currentSel.GetElementIds()
selectElem = [doc.GetElement(xId) for xId in selectElemId]

for i in selectElem:
	try:
		check = Revit.Elements.ElementWrapper.Wrap(i, True)
	except:
		check = None
	debug.append(check)	
	if check is None:
		out.append(ueWrapper.Invoke(None, (i, False)))
	else:
		out.append(i) 

OUT = out, debug
