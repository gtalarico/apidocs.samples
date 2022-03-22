# Written by Cyril P
import clr
clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *

clr.AddReference('RevitAPI')
import Autodesk
from Autodesk.Revit.DB import *

clr.AddReference('RevitAPIUI')
from Autodesk.Revit.UI import *

clr.AddReference('RevitServices')
import RevitServices
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

doc = DocumentManager.Instance.CurrentDBDocument
uidoc = DocumentManager.Instance.CurrentUIApplication.ActiveUIDocument
app = DocumentManager.Instance.CurrentUIApplication.Application


collcad = FilteredElementCollector(doc).OfClass(ImportInstance).ToElements()

collview = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Views).WhereElementIsNotElementType().ToElements()

list_out = []
list_dialog = []

for cad in collcad:
	if not cad.IsLinked:
		temp = []
		for view in collview:		
			try:
				cadinview = FilteredElementCollector(doc, view.Id).OfClass(ImportInstance).ToElements()
				if any([cad.Id == x.Id for x in cadinview]):
					temp.append(view)
			except : pass
	list_out.extend([cad, temp])
	
for item in list_out:
	if isinstance(item, list) :
		lst_temp = [view_.Name for view_ in item]
		list_dialog.extend(lst_temp)
	else:
		name_dwg = x.get_Parameter(BuiltInParameter.IMPORT_SYMBOL_NAME).AsString()
		list_dialog.append('**LE DWG "{}" est vible dans les vues suivantes :**'.format(name_dwg)) 	
		

TaskDialog.Show("Result", "\n".join(list_dialog))
OUT = list_dialog
