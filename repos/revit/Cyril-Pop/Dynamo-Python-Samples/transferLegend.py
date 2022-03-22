
#Copyright(c) 2019 Cyril.P
import clr
clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *

# Import DocumentManager and TransactionManager
clr.AddReference("RevitServices")
import RevitServices
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

# Import python library
import sys
pyt_path = r'C:\Program Files (x86)\IronPython 2.7\Lib'
sys.path.append(pyt_path)

# Import RevitAPI
clr.AddReference("RevitAPI")
import Autodesk
from Autodesk.Revit.DB import *

# Import RevitAPI
clr.AddReference("RevitAPIUI")
from Autodesk.Revit.UI import *

import System
from System.Collections.Generic import List

current_doc = DocumentManager.Instance.CurrentDBDocument
current_uiapp = DocumentManager.Instance.CurrentUIApplication
current_app = current_uiapp.Application
current_uidoc = DocumentManager.Instance.CurrentUIApplication.ActiveUIDocument

class CustomCopyHandler(IDuplicateTypeNamesHandler):
	def OnDuplicateTypeNamesFound(self, args):
		return DuplicateTypeAction.UseDestinationTypes
		
def copyLegendView(souceDoc, current_doc):	
	error = []
	lst_viewname = []
	lstViews = FilteredElementCollector(souceDoc).OfClass(View).WhereElementIsNotElementType().ToElements()
	viewsproject = [view for view in lstViews if not view.IsTemplate ]
	legendview = [ view for view in viewsproject if view.ViewType == ViewType.Legend ]

	TransactionManager.Instance.ForceCloseTransaction()
	TransactionManager.Instance.EnsureInTransaction(current_doc)
	for v in legendview:
		try:
			tmpIlst = List[ElementId]()
			tmpIlst.Add(v.Id)
			copyOptions = CopyPasteOptions()
			copyOptions.SetDuplicateTypeNamesHandler(CustomCopyHandler())	
			newViewCollId = ElementTransformUtils.CopyElements(souceDoc, tmpIlst, current_doc, None , copyOptions)
			current_doc.Regenerate()
			newViewId = list(newViewCollId)[0] 
			newView = current_doc.GetElement(newViewId)
			elementsInLegendId =  FilteredElementCollector(souceDoc, v.Id).ToElementIds()
			newelemId = ElementTransformUtils.CopyElements(v, List[ElementId](elementsInLegendId), newView, None, copyOptions)
			lst_viewname.append(newView.Name)
			#delete duplicate view
			current_doc.Delete(newViewId)
		except:
			import traceback
			error.append(traceback.format_exc())			
	TransactionManager.Instance.TransactionTaskDone()
	
	return lst_viewname , error
	
oOptions = OpenOptions()
oOptions.DetachFromCentralOption = DetachFromCentralOption.DetachAndPreserveWorksets
oOptions.Audit = True

dialog = FileOpenDialog("Revit Projet and Template (*.rvt, *.rte)|*.rvt;*.rte")
dialog.Show()
mpath = dialog.GetSelectedModelPath()
filepath = ModelPathUtils.ConvertModelPathToUserVisiblePath(mpath)

modelpath = FilePath(filepath)
souceDoc = current_app.OpenDocumentFile(modelpath, oOptions)
newLegendViews, error = copyLegendView(souceDoc, current_doc)
souceDoc.Close(False)

OUT =  newLegendViews, error
