#Copyright(c) Cyril P.
#Read xls file data with filter on view (read only cells visible)
#More Infos http://www.ironpython.info/index.php?title=Interacting_with_Excel
import clr

clr.AddReferenceByName('Microsoft.Office.Interop.Excel, Version=11.0.0.0, Culture=neutral, PublicKeyToken=71e9bce111e9429c' )
from Microsoft.Office.Interop import Excel
from System.Runtime.InteropServices import Marshal

import System
specsVisu = System.Enum.Parse(Excel.XlCellType, "xlCellTypeVisible")

path = IN[0]

class Lst_Xls():
	def __init__(self, path):
		ex = Excel.ApplicationClass()
		ex.Visible = False
		lst_xls = []
		workbook = ex.Workbooks.Open(path)
		#get worksheet at index (start at 1)
		ws = workbook.Worksheets[1]
		ws.Activate
		#plagefiltrevisible = ws.UsedRange.SpecialCells(Excel.XlCellType.xlCellTypeVisible).Rows
		#or
		plagefiltrevisible = ws.UsedRange.SpecialCells(specsVisu).Rows
		for row in plagefiltrevisible:
			lst_xls.append(row.Value2)
		self.datas = lst_xls
		ex.Workbooks.Close()
		ex.Quit()
		Marshal.ReleaseComObject(workbook)
		Marshal.ReleaseComObject(ex)
		
objxls = Lst_Xls(path)	

OUT = objxls.datas
