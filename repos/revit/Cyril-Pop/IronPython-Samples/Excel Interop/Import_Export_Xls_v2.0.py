# coding: utf-8 
import clr
clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *

import System
from System import Array
from System.Collections.Generic import *

clr.AddReference('System.Drawing')
import System.Drawing
from System.Drawing import *


clr.AddReferenceByName('Microsoft.Office.Interop.Excel, Version=11.0.0.0, Culture=neutral, PublicKeyToken=71e9bce111e9429c' )
"""
try:
	clr.AddReferenceByName('Microsoft.Office.Interop.Excel, Version=11.0.0.0, Culture=neutral, PublicKeyToken=71e9bce111e9429c' )
except:
	clr.AddReference('Microsoft.Office.Interop.Excel')
"""
from Microsoft.Office.Interop import Excel
from System.Runtime.InteropServices import Marshal

xlDirecDown = System.Enum.Parse(Excel.XlDirection, "xlDown")
xlDirecRight = System.Enum.Parse(Excel.XlDirection, "xlToRight")
xlDirecUp = System.Enum.Parse(Excel.XlDirection, "xlUp")
xlDirecLeft = System.Enum.Parse(Excel.XlDirection, "xlToLeft")


class ExcelUtils():
	def __init__(self, lstData, filepath):
		self.lstData = lstData
		self.filepath = filepath

		print self.filepath
		
		
	def exportXls(self):
		
		ex = Excel.ApplicationClass()
		ex.Visible = True
		ex.DisplayAlerts = False
		workbook = ex.Workbooks.Add()
		workbook.SaveAs(self.filepath)
		ws = workbook.Worksheets[1]	
		nbr_row = len(self.lstData)
		nbr_colum = len(self.lstData[0])
		xlrange  = ws.Range[ws.Cells(1, 1), ws.Cells(nbr_row, nbr_colum)]
		a = Array.CreateInstance(object, nbr_row, nbr_colum)
		for indexR, row in enumerate(self.lstData):
			for indexC , value in  enumerate(row):
				a[indexR,indexC] = value
				
		#copy Array in range			
		xlrange.Value2 = a		
		used_range = ws.UsedRange	
		for column in used_range.Columns:
			column.AutoFit()
		# apply style
		missing = System.Type.Missing
		try:
			currentWs.ListObjects.Add(Excel.XlListObjectSourceType.xlSrcRange, xlrange, missing, Excel.XlYesNoGuess.xlGuess, missing).Name = "WFTableStyle"
			currentWs.ListObjects["WFTableStyle"].TableStyle = "TableStyleMedium6"
		except:pass
			
			
	def importXls(self):
		ex = Excel.ApplicationClass()
		ex.Visible = False
		lst_xls = []
		workbook = ex.Workbooks.Open(self.filepath)
		ws = workbook.Worksheets[1]
		##get number of Rows not empty ##
		rowCountF = max(ws.Range(i).End(xlDirecUp).Row for i in ["A65536", "B65536", "C65536", "D65536", "E65536", "F65536", "G65536", "H65536"])
		# other method if column A is empty
		# rowCountF = ws.Range("B65536").End(xlDirecUp).Row
		# rowCountF = ws.Columns[1].End(xlDirecDown).Row
		##get number of Coloun not empty ##
		colCountF = max(ws.Range(i).End(xlDirecLeft).Column for i in ["ZZ1", "ZZ2", "ZZ3", "ZZ4", "ZZ5", "ZZ6", "ZZ7", "ZZ8", "ZZ9"])
		# other methods
		#colCountF = ws.Range("ZZ9").End(xlDirecLeft).Column
		# colCountF = ws.Rows[1].End(xlDirecRight).Column
		self.fullrange = ws.Range[ws.Cells(1, 1), ws.Cells(rowCountF, colCountF)]
		self.fullvalue = list(self.fullrange.Value2)
		#split list into sublist with number of colum
		n = colCountF					
		self.datas = list(self.fullvalue [i:i+n] for i in range(0, len(self.fullvalue ), n))
		self.first_flst = [x for x in self.datas [0]] 
		ex.Workbooks.Close()
		ex.Quit()
    		#other proper way to make sure that you really closed and released all COM objects 
		if workbook is not None:
			Marshal.ReleaseComObject(workbook)
		if ex is not None:
			Marshal.ReleaseComObject(ex)     
		workbook = None        
		ex = None
