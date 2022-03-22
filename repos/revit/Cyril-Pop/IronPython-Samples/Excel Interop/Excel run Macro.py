import clr
import time
clr.AddReferenceByName('Microsoft.Office.Interop.Excel, Version=11.0.0.0, Culture=neutral, PublicKeyToken=71e9bce111e9429c')
from Microsoft.Office.Interop import Excel
from System.Runtime.InteropServices import Marshal
#time.sleep(3)

dirfichier = IN[0]
ex = Excel.ApplicationClass()
ex.Visible = True
ex.DisplayAlerts = False

wb = ex.Workbooks.Open(dirfichier)
ws = wb.Worksheets[1]
#time.sleep(3)
# run macro named 'Dynamo'
ex.Application.Run("Dynamo")
wb.SaveAs(dirfichier)

ex.Workbooks.Close()
ex.Quit()

if wb is not None:
	Marshal.ReleaseComObject(wb)
if ex is not None:
	Marshal.ReleaseComObject(ex)     
wb = None        
ex = None

OUT = "Dynamo Ok !"
