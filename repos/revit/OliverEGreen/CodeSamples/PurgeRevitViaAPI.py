import clr
import sys
sys.path.append('C:\Program Files (x86)\IronPython 2.7\Lib')
import System
from System.Collections.Generic import *

clr.AddReference("RevitNodes")
import Revit

clr.AddReference("RevitServices")
import RevitServices
from RevitServices.Persistence import DocumentManager

clr.AddReference("RevitAPI")
clr.AddReference("RevitAPIUI")
import Autodesk
from Autodesk.Revit.DB import *
from Autodesk.Revit.UI import * 

doc = DocumentManager.Instance.CurrentDBDocument
uiapp = DocumentManager.Instance.CurrentUIApplication
app = uiapp.Application
uidoc = uiapp.ActiveUIDocument

def GetPurgeableElements(doc, rule_id_list):
	failure_messages = PerformanceAdviser.GetPerformanceAdviser().ExecuteRules(doc, rule_id_list)
	if failure_messages.Count > 0:
		purgeable_element_ids = failure_messages[0].GetFailingElements()
		return purgeable_element_ids

#A constant 
PURGE_GUID = "e8c63650-70b7-435a-9010-ec97660c1bda"

#A generic list of PerformanceAdviserRuleIds as required by the ExecuteRules method
rule_id_list = List[PerformanceAdviserRuleId]()

#Iterating through all PerformanceAdviser rules looking to find that which matches PURGE_GUID
for rule_id in PerformanceAdviser.GetPerformanceAdviser().GetAllRuleIds():
	if str(rule_id.Guid) == PURGE_GUID:
		rule_id_list.Add(rule_id)
		break

#Attempting to retrieve the elements which can be purged
purgeable_element_ids = GetPurgeableElements(doc, rule_id_list)

if purgeable_element_ids != None:
	purgeable_elements = [doc.GetElement(id) for id in purgeable_element_ids]
	OUT = purgeable_elements, purgeable_element_ids
else:
	OUT = "No elements left to purge"
