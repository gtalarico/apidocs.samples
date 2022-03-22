#Copyright(c) Cyril P.
#More Infos http://www.ironpython.info/index.php?title=Interacting_with_Excel
import clr

import System
from System import Array
from System.Collections.Generic import *

clr.AddReferenceByName('Microsoft.Office.Interop.Excel, Version=11.0.0.0, Culture=neutral, PublicKeyToken=71e9bce111e9429c' )
from Microsoft.Office.Interop import Excel
from System.Runtime.InteropServices import Marshal

xlDirecDown = System.Enum.Parse(Excel.XlDirection, "xlDown")
xlDirecRight = System.Enum.Parse(Excel.XlDirection, "xlToRight")
xlDirecLeft = System.Enum.Parse(Excel.XlDirection, "xlToLeft")

input = r'C:\My Excel Files\Book1.xls'

class Lst_Xls():
	def __init__(self, path):
		ex = Excel.ApplicationClass()
		ex.Visible = False
		lst_xls = []
		workbook = ex.Workbooks.Open(path)
		ws = workbook.Worksheets[1]
		
		rowCountF = max(ws.Range(i).End(xlDirecUp).Row for i in ["A65536", "B65536", "C65536", "D65536", "E65536", "F65536", "G65536", "H65536"])
		# other method if column A is empty
		# rowCountF = ws.Range("B65536").End(xlDirecUp).Row
		# rowCountF = ws.Columns[1].End(xlDirecDown).Row
		##get number of Coloun not empty ##
		colCountF = max(ws.Range(i).End(xlDirecLeft).Column for i in ["ZZ1", "ZZ2", "ZZ3", "ZZ4", "ZZ5", "ZZ6", "ZZ7", "ZZ8", "ZZ9"])
		# other methods
		#colCountF = ws.Range("ZZ9").End(xlDirecLeft).Column
		# colCountF = ws.Rows[1].End(xlDirecRight).Column
		
		for i in range(1,rowCountF+1):
			temp_lst = []
			for j in range(1,colCountF+1):
				try:
					temp_lst.append(ws.Cells[i,j].Value2.ToString())
				except:
					temp_lst.append(ws.Cells[i,j].Value2)		
			lst_xls.append(temp_lst)
		self.datas = lst_xls
		self.first_flst = [x for x in lst_xls[0]] # or lst_xls[0] 
		#Get the specify index
		self.type_fidx = self.first_flst.index("Type")
		ex.Workbooks.Close()
		ex.Quit()
    		#other proper way to make sure that you really closed and released all COM objects 
		Marshal.ReleaseComObject(workbook)
		Marshal.ReleaseComObject(ex)
		
obj_xl_lst = Lst_Xls(input)		
