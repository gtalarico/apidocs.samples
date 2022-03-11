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


class ExcelUtils():
	def __init__(self, filepath, nameSheets):
		self.filepath = filepath
		self.nameSheets = nameSheets if hasattr(nameSheets, '__iter__') and not isinstance(nameSheets, (str, System.String)) else [nameSheets]
		self.ex = Excel.ApplicationClass()
		self.ex.Visible = False
		self.workbook = self.ex.Workbooks.Open(self.filepath)

	
	def ExitExcel(self):
			self.workbook.Close()
			self.ex.Workbooks.Close()
			self.ex.Quit()
			#other proper way to make sure that you really closed and released all COM objects 
			if self.workbook is not None:
				Marshal.ReleaseComObject(self.workbook)
			if self.ex is not None:
				Marshal.ReleaseComObject(self.ex)
			self.workbook = None
			self.ex = None
			
	def ImportXls(self):
		lst_xls = []
		for wsMame in self.nameSheets:
			ws = self.workbook.Worksheets[wsMame]
			##get number of Rows not empty ##
			rowCountF = max(ws.Range(i).End(xlDirecUp).Row for i in ["A65536", "B65536", "C65536", "D65536", "E65536", "F65536", "G65536", "H65536"])
			##get number of Coloun not empty ##
			colCountF = max(ws.Range(i).End(xlDirecLeft).Column for i in ["ZZ1", "ZZ2", "ZZ3", "ZZ4", "ZZ5", "ZZ6", "ZZ7", "ZZ8", "ZZ9"])
			# other methods
			self.fullrange = ws.Range[ws.Cells(1, 1), ws.Cells(rowCountF, colCountF)]
			self.fullvalue = list(self.fullrange.Value2)
			#split list into sublist with number of colum
			n = colCountF
			datas = list(self.fullvalue [i:i+n] for i in range(0, len(self.fullvalue ), n))
			lst_xls.append(datas)
			
		self.ExitExcel()
		return lst_xls
		
filePath = IN[0]
lstSheetName = IN[1]

objxls = ExcelUtils(filePath, lstSheetName)

fullDatas = objxls.ImportXls()

