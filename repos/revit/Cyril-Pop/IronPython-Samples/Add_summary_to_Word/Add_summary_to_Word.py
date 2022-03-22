import sys
import clr
import System

clr.AddReference('RevitAPI')
import Autodesk
from Autodesk.Revit.DB import *

clr.AddReference('RevitServices')
import RevitServices
from RevitServices.Persistence import DocumentManager
doc = DocumentManager.Instance.CurrentDBDocument

clr.AddReference('System.Drawing')
import System.Drawing
clr.AddReference('System.Windows.Forms')
from System.Windows.Forms import Clipboard

clr.AddReference("Microsoft.Office.Interop.Word")
import Microsoft.Office.Interop.Word as Word

clr.AddReference("System.Runtime.InteropServices")
import System.Runtime.InteropServices

source_filenamePath = IN[0] 

# clear session
word_application = Word.ApplicationClass()
word_application.Quit()
word_application = None
#
word_application = Word.ApplicationClass()
word_application.visible = True
doc_word = word_application.Documents.Open(source_filenamePath)
fecSymb = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Doors).WhereElementIsElementType().ToElements()
imgSize = System.Drawing.Size( 100, 100 )
for symb in fecSymb:
	# add Image
	bitm = symb.GetPreviewImage(imgSize) 
	Clipboard.SetDataObject(bitm)
	doc_end1 = doc_word.Content.End -1
	doc_end2 = doc_word.Content.End
	rng = doc_word.Range(doc_end1, doc_end2)
	rng.Paste()
	# add NAme and Description 
	doc_end1 = doc_word.Content.End -1
	doc_end2 = doc_word.Content.End
	rng = doc_word.Range(doc_end1, doc_end2)
	famName = symb.Family.Name
	symbName = Element.Name.GetValue(symb)
	description = symb.get_Parameter(BuiltInParameter.ALL_MODEL_DESCRIPTION).AsString()
	rng.Text += "Family : {}\nType : {}\nDescription : {}\n".format(famName, symbName, description)
	
OUT = 0
