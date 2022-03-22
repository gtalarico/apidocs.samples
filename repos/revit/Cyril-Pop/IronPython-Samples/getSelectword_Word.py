import sys
import clr
import System

clr.AddReference("Microsoft.Office.Interop.Word")
import Microsoft.Office.Interop.Word as Word

clr.AddReference("System.Runtime.InteropServices")
import System.Runtime.InteropServices


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
    def getSelection(self):
        return self.wapp.Selection.Text
    
    def closeProperly(self):
        if self.document is not None:
            Marshal.ReleaseComObject(self.document)
        if self.wapp is not None:
            Marshal.ReleaseComObject(self.wapp)     
        self.document = None        
        self.wapp = None         
        
objWord = WordUtils()   

OUT = objWord.getSelection
objWord.closeProperly()
