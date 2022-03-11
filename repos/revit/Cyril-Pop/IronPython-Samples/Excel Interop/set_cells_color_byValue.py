import sys
import clr
clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *

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
xlDirecUp = System.Enum.Parse(Excel.XlDirection, "xlUp")
xlDirecLeft = System.Enum.Parse(Excel.XlDirection, "xlToLeft")


class Lst_Xls():
	def __init__(self, path, lstValue, sheetName):
		self.setValue = set([int(x) for x in lstValue])
		self.lsta = []
		ex = Excel.ApplicationClass()
		ex.Visible = True
		lst_xls = []

		workbook = ex.Workbooks.Open(path)
		ws = workbook.Worksheets[sheetName]
		
		##get number of Rows not empty ##
		rowCountF = max(ws.Range(i).End(xlDirecUp).Row for i in ["A65536", "B65536", "C65536", "D65536", "E65536", "F65536", "G65536", "H65536"])
		##get number of Coloun not empty ##
		colCountF = max(ws.Range(i).End(xlDirecLeft).Column for i in ["ZZ1", "ZZ2", "ZZ3", "ZZ4", "ZZ5", "ZZ6", "ZZ7", "ZZ8", "ZZ9"])
		self.fullrange = ws.Range[ws.Cells(1, 1), ws.Cells(rowCountF, colCountF)]
		#self.fullvalue = self.fullrange.Value2
		self.fullvalue = list(self.fullrange.Value2)
		#split list into sublist with number of colum
		n = colCountF
		self.datas = list(self.fullvalue[i:i+n] for i in range(0, len(self.fullvalue ), n))
		
				
	def setCellColor(self):	
		strRgb = "128,0,64"
		for row in self.fullrange.Rows:
			rangerow = row.Value2
			set_rangeRow = set()
			for i in rangerow:
				try:
					set_rangeRow.add(int(i))
				except:
					pass
			print(set_rangeRow)
			checkSetAB = set_rangeRow & self.setValue
			if len(checkSetAB) > 0:
				for i in range(row.Columns.Count):
					cellRg = row.Cells[1, i + 1]
					value = cellRg.Value2
					print(value)
					if value is not None:
						# cellRg.Interior.Color = eval("ColorTranslator.ToOle(Color.FromArgb(" + strRgb + "))")
						cellRg.Interior.Color = System.Drawing.ColorTranslator.ToOle(System.Drawing.Color.Yellow)

			

xlspath = r'‪C:\Users\myxlsFile.xls' #IN[0]	
lstValue = ["05001", 12011, "20001", "40003", 05511 ] #IN[1]
sheetName = "Feuil1" #IN[2]

obj_xl_lst = Lst_Xls(xlspath, lstValue, sheetName)
obj_xl_lst.setCellColor()

OUT =  obj_xl_lst.datas
