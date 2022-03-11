#Written By CP


import sys
import clr
import System

from System import DateTime

clr.AddReference("Microsoft.Office.Interop.Word")
import Microsoft.Office.Interop.Word as Word

clr.AddReference("System.Runtime.InteropServices")
import System.Runtime.InteropServices


sys.path.append(r'C:\Program Files (x86)\IronPython 2.7\Lib')
import os
from os import walk

    
def doc_replace_text(source_filename, tokens, values):
	try:	
		missing = System.Type.Missing
		replaceAll = Word.WdReplace.wdReplaceAll
	
		word_application = Word.ApplicationClass()
		word_application.visible = False
		document = word_application.Documents.Open(source_filename)
		#Find and Replace Process
		for _find, _replace in zip(tokens,values):
			for myStoryRange in document.StoryRanges:
				myStoryRange.Find.Execute(
				_find, # search text
				True, # match case
				missing, # match whole word
				missing, # match wildcards
				missing, # match sounds like
				missing, # match all word forms
				True, # forward?
				Word.WdFindWrap.wdFindContinue, # wrap enum
				missing, # format?
				_replace, # replace with
				replaceAll, # replace enum
				missing, # match Kashida (arabic letters)
				missing, # diatrics?
				missing, # match other Arabic letters
				missing # support right to left
				)
				try:
					while myStoryRange.NextStoryRange is not None:
						q = myStoryRange.NextStoryRange 
						q.Find.Execute(
						_find, # search text
						True, # match case
						missing, # match whole word
						missing, # match wildcards
						missing, # match sounds like
						missing, # match all word forms
						True, # forward?
						Word.WdFindWrap.wdFindContinue, # wrap enum
						missing, # format?
						_replace, # replace with
						replaceAll, # replace enum
						missing, # match Kashida (arabic letters)
						missing, # diatrics?
						missing, # match other Arabic letters
						missing # support right to left
						)
				except: pass
				#Find and replace in TextBox(shapes)
				try:	
					for shape in document.Shapes:
						initialText = shape.TextFrame
						if initialText.HasText and _find == "PHASE EXE":
							rangeobj = initialText.TextRange 
							rangeobj.Find.Execute(
							_find, # search text
							True, # match case
							missing, # match whole word
							missing, # match wildcards
							missing, # match sounds like
							missing, # match all word forms
							True, # forward?
							Word.WdFindWrap.wdFindContinue, # wrap enum
							missing, # format?
							_replace, # replace with
							replaceAll, # replace enum
							missing, # match Kashida (arabic letters)
							missing, # diatrics?
							missing, # match other Arabic letters
							missing # support right to left
							)
							#OTHER METHOD
							#resultingText = initialText.TextRange.Text.Replace(_find, _replace)
							#shape.TextFrame.TextRange.Text = resultingText
				except: pass
								
		print source_filename + ": success"
		pdf_path =  source_filename + ".pdf"  	            
	
		document.Save()
		document.SaveAs2(pdf_path, Word.WdSaveFormat.wdFormatPDF)
		document.Close()
		document = None
	
		word_application.Quit()
		word_application = None 
		#Marshal.ReleaseComObject(app)
	except:
		# if error occurs anywhere in the process catch it
		import traceback
		errorReport = traceback.format_exc()
		print errorReport
		document.Close()
		document = None
		word_application.Quit()
		word_application = None		
    
    


tokens = ["EXE", "PHASE EXE"] # etc...
values = ["DOE", "PHASE DOE"]
    
#doc_replace_text(source_filename, tokens, values, destination_filename)
word_application = Word.ApplicationClass()
word_application.Quit()
word_application = None
monRepertoire = "C:\\Users\\userName\\Documents\\Proposées"
for (repertoire, sousRepertoires, fichiers) in walk(monRepertoire):
	for file in fichiers:
		if file.endswith(".docx"):
			filename = (os.path.join(repertoire, file))
			doc_replace_text(filename, tokens, values) 

