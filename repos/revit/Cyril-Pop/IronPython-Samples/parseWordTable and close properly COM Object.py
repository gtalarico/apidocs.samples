import sys
import clr
import System

clr.AddReference("Microsoft.Office.Interop.Word")
import Microsoft.Office.Interop.Word as Word

clr.AddReference("System.Runtime.InteropServices")
import System.Runtime.InteropServices
from System.Runtime.InteropServices import Marshal

clr.AddReference("System.Windows.Forms")
import System.Windows.Forms
from System.Windows.Forms import *

class WordUtils():
    def __init__(self):
        self.error = []
        try:        
            self.interrop = System.Runtime.InteropServices.Marshal.GetActiveObject("Word.Application")  
            self.wapp = self.interrop.Application
            self.document = self.wapp.ActiveDocument
            self.docName = self.document.FullName   
        except Exception as ex: 
            self.error.append(ex)       
            self.wapp = Word.ApplicationClass()
            self.document = self.wapp.ActiveDocument
            self.docName = self.document.FullName


    
    @property   
    def getSelectionTable(self):
        out = []
        select = self.wapp.Selection
        tables = select.Tables
        if tables.Count > 0:
            for tb in tables:
                colCount = tb.Columns.Count
                rowCount = tb.Rows.Count
                for col in range(1, colCount +1):
                    temp = []
                    for row in range(1, rowCount +1):
                        cell = tb.Cell(row, col)
                        valueText = cell.Range.Text.Trim()
                        temp.append(valueText.replace('\r', ''))
                    out.append(temp)        
            return out
        else:
            MessageBox.Show("Wrong Selection select a table", "Selection Error")
            return None
            
    def closeProperly(self):
        if self.document is not None:
            Marshal.ReleaseComObject(self.document)
        if self.wapp is not None:
            Marshal.ReleaseComObject(self.wapp)     
        self.document = None        
        self.wapp = None
            
         
def genChopLst(lst):
    """
    generator to split list at empty item
    """
    out = []
    for x in lst:
        if len(x) == 1 and len(out) > 0:
            yield out
            out = []
        elif len(x) != 1:
            out.append(x)
    yield out       
            
    
    
objWord = WordUtils()   
dataLst = objWord.getSelectionTable
outchop = [[x for x in genChopLst(sublst)] for sublst in dataLst]
OUT =  outchop
objWord.closeProperly()
        
        
        
        
