#Copyright(c) Cyril P.
#Read xls file data with filter on view (read only cells selected)

import clr
clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *

#import Revit API
clr.AddReference('RevitAPI')
import Autodesk
from Autodesk.Revit.DB import *

clr.AddReference('RevitAPIUI')
from Autodesk.Revit.UI import *
from Autodesk.Revit.UI.Selection import *


clr.AddReference('RevitServices')
import RevitServices
from RevitServices.Persistence import DocumentManager
doc = DocumentManager.Instance.CurrentDBDocument
uiapp = DocumentManager.Instance.CurrentUIApplication
uidoc = uiapp.ActiveUIDocument

import System
from System.Collections.Generic import List
clr.AddReferenceByName('Microsoft.Office.Interop.Excel, Version=11.0.0.0, Culture=neutral, PublicKeyToken=71e9bce111e9429c' )
from Microsoft.Office.Interop import Excel
from System.Runtime.InteropServices import Marshal

refreshBoolean = IN[0]

def checkInteger(val):
    try:
        check = int(val)
        return True
    except: return False 
    
class OpenFileException(Exception):
    pass

class Lst_Xls():
    def __init__(self):
        try:   
            ex = System.Runtime.InteropServices.Marshal.GetActiveObject("Excel.Application")
        except: 
            ex = Excel.ApplicationClass()   
        ex.Visible = True
        self.app = ex 
        self.error = None
        self.data = []  
        self.workbook = ex.ActiveWorkbook
        ws = ex.ActiveSheet
        selectRange = ex.Selection   
        for r in selectRange:
            self.data.append(r.Value2)
            
    def closeProperly(self):
        if self.workbook is not None:
            Marshal.ReleaseComObject(self.workbook)
        if self.app is not None:
            Marshal.ReleaseComObject(self.app)     
        self.workbook = None        
        self.app = None
            
        
objxls = Lst_Xls()  
if objxls.error is None:
    iLstId = List[ElementId]()
    outElem = []
    for val in objxls.data:
        if checkInteger(val):
            elemId = ElementId(int(val))
            elem = doc.GetElement(elemId)
            if elem is not None:
                outElem.append(elem)
                iLstId.Add(elem.Id)
    uidoc.Selection.SetElementIds(iLstId)           
    OUT = outElem
    
else: 
    OUT = "Error "
objxls.closeProperly()  
