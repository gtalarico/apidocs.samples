# coding : utf-8
import clr

clr.AddReference('RevitAPI')
import Autodesk
from Autodesk.Revit.DB import *

clr.AddReference('RevitServices')
import RevitServices
from RevitServices.Persistence import DocumentManager
doc = DocumentManager.Instance.CurrentDBDocument


class ParaProj():
	def __init__(self, definition, binding):
		self.defName = definition.Name
		self.binding = binding 
		self.thesecats = []
		self.group = LabelUtils.GetLabelFor(definition.ParameterGroup)
		self.type = "Instance" if isinstance(binding, InstanceBinding) else "Type"
		
	@property	
	def categories(self):
		thesecats = []	
		for cat in self.binding.Categories:
	 		try:
				thesecats.append(cat.Name)
			except SystemError:
				pass  
		return thesecats
		
	@property					
	def isShared(self):
		collSharP = FilteredElementCollector(doc).OfClass(SharedParameterElement)
		paraSharPara = [x.GetDefinition().Name for x in collSharP]	
		return 	True if self.defName in paraSharPara else False	
				

paraName = []
paraGroup = []
paraCategories = [] 
paraType = []
paraIsShared = []
iterator =  doc.ParameterBindings.ForwardIterator()
while iterator.MoveNext():
    objBind = ParaProj(iterator.Key, iterator.Current)
    paraName.append(objBind.defName)
    paraGroup.append(objBind.group)
    paraType.append(objBind.type)
    paraIsShared.append(objBind.isShared)
    paraCategories.append(objBind.categories)
  

OUT = paraName, paraGroup, paraType, paraIsShared, paraCategories
