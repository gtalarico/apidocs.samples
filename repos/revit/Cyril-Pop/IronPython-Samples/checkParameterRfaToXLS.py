# Copyright (c) 20119- POUPIN.C
import clr
import re
clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *
clr.AddReference('RevitAPI')
import Autodesk
from Autodesk.Revit.DB import *
clr.AddReference('RevitServices')
import RevitServices
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager
app = DocumentManager.Instance.CurrentUIApplication.Application

clr.AddReference('System.Drawing')
from System import Array
from System.Drawing import *

clr.AddReferenceByName('Microsoft.Office.Interop.Excel, Version=11.0.0.0, Culture=neutral, PublicKeyToken=71e9bce111e9429c')
from Microsoft.Office.Interop import Excel
from System.Runtime.InteropServices import Marshal
import sys
sys.path.append(r'C:\Program Files (x86)\IronPython 2.7\Lib')
import os
		
class ParameterProp():
	def __init__(self, para):
		self._para = para
		self._pname = para.Definition.Name
		self._pisinstance = para.IsInstance
	
class FamiliesCheck():
	def __init__(self, dirpath):
		self.dirpath = dirpath
		self.full_lstP = []	
		for dir, subdir, files in os.walk(dirpath):
			for file in files:
				if file.endswith(".rfa") and re.search(r'\.\d+.rfa$', file) is None and re.search(r'[aA]ncien', dir) is None:
					famDoc = app.OpenDocumentFile(dir + '\\' + file)
					if famDoc.IsFamilyDocument:
						famManager = famDoc.FamilyManager
						lst_para = [ ParameterProp(x) for x in famManager.Parameters]
						lst_para.sort(key = lambda x : x._pname)
						lst_para[0:0] = [file]
						self.full_lstP.append(lst_para)				
					famDoc.Close(False)		
	
	def XlsWriter(self):
		ex = Excel.ApplicationClass()
		ex.Visible = True
		ex.DisplayAlerts = False
		workbook = ex.Workbooks.Add()
		workbook.SaveAs(self.dirpath + "\\reportFamilies.xlsx")
		ws = workbook.Worksheets[1]		
		nbr_row = 1
		for sub_lst in self.full_lstP:
			nbr_col = len(sub_lst)
			xlrange  = ws.Range[ws.Cells(nbr_row, 1), ws.Cells(nbr_row, len(sub_lst))]
			a = Array.CreateInstance(object, 1, len(sub_lst))
			b = Array.CreateInstance(object, 1, len(sub_lst))
			for index, i in enumerate(sub_lst):
				# if i is string
				if isinstance(i, str):
					a[0,index] = i
				#else i is a ParameterProp objet	
				else:
					a[0,index] = i._pname
					if i._pisinstance == False:
						b[0,index] = 6
					elif i._pisinstance == True:
						b[0,index] = 8		
					else:
						b[0,index] = None
			#copy Array in range			
			xlrange.Value2 = a	
			for cell, color_index in zip(xlrange, b):
				cell.Interior.ColorIndex = color_index
			nbr_row += 1
		used_range = ws.UsedRange	
		for column in used_range.Columns:
			column.AutoFit()
		workbook.Save()	
			
dirpath = IN[0]
obj_check = FamiliesCheck(dirpath)
obj_check.XlsWriter()
OUT = obj_check.full_lstP
