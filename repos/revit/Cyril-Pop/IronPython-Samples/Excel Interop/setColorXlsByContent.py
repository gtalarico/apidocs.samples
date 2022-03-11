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
from Microsoft.Office.Interop import Excel
from System.Runtime.InteropServices import Marshal

xlDirecDown = System.Enum.Parse(Excel.XlDirection, "xlDown")
xlDirecRight = System.Enum.Parse(Excel.XlDirection, "xlToRight")


class Lst_Xls():
	def __init__(self, path, dictcolor):
		self.dictcolor = dictcolor
		self.lsta = []
		ex = Excel.ApplicationClass()
		ex.Visible = True
		lst_xls = []

		workbook = ex.Workbooks.Open(path)
		ws = workbook.Worksheets[1]
		
		##get number of Rows not empty ##
		rowCountF = ws.Columns[1].End(xlDirecDown).Row
		##get number of Coloun not empty ##
		colCountF = ws.Rows[1].End(xlDirecRight).Column
		self.fullrange = ws.Range[ws.Cells(1, 1), ws.Cells(rowCountF, colCountF)]
		self.fullvalue = self.fullrange.Value2
		
	def setCellColorbyDict(self):	
		for cellRg in self.fullrange:
			if cellRg.Value2 in self.dictcolor:
				strRgb = dictcolor.get(cellRg.Value2)
				cellRg.Interior.Color = eval("ColorTranslator.ToOle(Color.FromArgb(" + strRgb + "))")
				
	def setRowColorbyDict(self):	
		for row in self.fullrange.Rows:
			rangerow = row.Value2
			firstvalue = rangerow.GetValue(1,1)
			if firstvalue in self.dictcolor:
				strRgb = dictcolor.get(firstvalue)
				row.Interior.Color = eval("ColorTranslator.ToOle(Color.FromArgb(" + strRgb + "))")
				self.lsta.append([firstvalue, strRgb])				
			

#dictionary to complete
dictcolor = {"CW_CP":"192,192,255", "CW_SP":"85,168,255", "CW_GL":"0,0,255", "FC_XX":"128,0,64"}		
xlspath = IN[0]	

obj_xl_lst = Lst_Xls(xlspath, dictcolor)
#obj_xl_lst.setCellColorbyDict()
obj_xl_lst.setRowColorbyDict()

OUT =  obj_xl_lst.lsta
