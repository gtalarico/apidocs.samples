import sys
import clr
import System

clr.AddReference("Microsoft.Office.Interop.Word")
import Microsoft.Office.Interop.Word as Word

clr.AddReference("System.Runtime.InteropServices")
import System.Runtime.InteropServices

    
def find_replace(objRng, search_txt, replce_txt):
	missing = System.Type.Missing
	replaceAll = Word.WdReplace.wdReplaceAll
	objRng.Find.Execute(
	search_txt, # search text
	True, # match case
	missing, # match whole word
	missing, # match wildcards
	missing, # match sounds like
	missing, # match all word forms
	True, # forward?
	Word.WdFindWrap.wdFindContinue, # wrap enum
	missing, # format?
	replce_txt, # replace with
	replaceAll, # replace enum
	missing, # match Kashida (arabic letters)
	missing, # diatrics?
	missing, # match other Arabic letters
	missing # support right to left
	)
    
def doc_replace_text(source_filename, tokens, values):
	global errors

	word_application = Word.ApplicationClass()
	word_application.visible = True
	document = word_application.Documents.Open(source_filename)
	#Find and Replace Process
	for _find, _replace in zip(tokens,values):
		for myStoryRange  in document.StoryRanges:
			find_replace(myStoryRange , _find, _replace)
			try:
				while myStoryRange.NextStoryRange is not  None:
					q = myStoryRange.NextStoryRange 
					find_replace(q, _find, _replace)
			except:
				import traceback
				errors.append(traceback.format_exc())
			#Find and replace in TextBox(shapes)
			try:	
				for shape in document.Shapes:
					initialText = shape.TextFrame
					if initialText.HasText:
						rangeobj = initialText.TextRange 
						find_replace(rangeobj, _find, _replace)

			except:
				import traceback
				errors.append(traceback.format_exc())
								

filename = IN[0]
tokens = IN[1]
values = IN[2]
errors = []    
word_application = Word.ApplicationClass()
word_application.Quit()
word_application = None
doc_replace_text(filename, tokens, values) 

OUT = errors
