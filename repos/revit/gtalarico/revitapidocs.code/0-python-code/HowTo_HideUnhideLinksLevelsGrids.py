"""
HIDE / UNHIDE - LEVELS AND GRIDS FROM LINKS DOCUMENTS

TESTED REVIT API: 2017, 2018

Author: min.naung@https://twentytwo.space/contact | https://github.com/mgjean

This file is shared on www.revitapidocs.com
For more information visit http://github.com/gtalarico/revitapidocs
License: http://github.com/gtalarico/revitapidocs/blob/master/LICENSE.md
"""

import System
from System.Collections.Generic import List
from Autodesk.Revit.DB import Transaction
from Autodesk.Revit.DB import *

doc = __revit__.ActiveUIDocument.Document
active_view = doc.ActiveView

# filter name "can name anything"
ifilter = "GiveFilterAName"

endWiths = "Anything"

# filter check
found = False

unhide = False # Edit here to hide/unhide
msg = "Unhide" if unhide else "Hide"
trans = Transaction(doc,"%s links levels grids" %(msg))
trans.Start()

# collect all filter elements
allFilters = FilteredElementCollector(doc).OfClass(FilterElement).ToElements()

# get filters from current view
viewFilters = active_view.GetFilters()
# collect filters' names
viewFiltersName = [doc.GetElement(i).Name.ToString() for i in viewFilters]

# loop each filter
for fter in allFilters:
	# filter already have in doc but not in current view
	if ifilter == fter.Name.ToString() and ifilter not in viewFiltersName:
		# add filter
		active_view.AddFilter(fter.Id)
		# set filter visibility
		active_view.SetFilterVisibility(fter.Id, unhide)
		found = True
	# filter already have in doc and current view
	if ifilter == fter.Name.ToString() and ifilter in viewFiltersName:
		# set filter visibility
		active_view.SetFilterVisibility(fter.Id, unhide)
		found = True
		
# if filter not found in doc
if not found:
	# all grids in doc
	grids = FilteredElementCollector(doc).OfClass(Grid).ToElements()
	# all levels in doc
	levels = FilteredElementCollector(doc).OfClass(Level).ToElements()
	# collect category id from grid and level
	CateIds = List[ElementId]([grids[0].Category.Id,levels[0].Category.Id])
	
	# type ids from grids 
	gridTypeIds = set([i.GetTypeId() for i in grids])
	# type ids from levels
	levelTypeIds = set([i.GetTypeId() for i in levels])
	
	# get grid type element
	type_elems = [doc.GetElement(i) for i in gridTypeIds]
	# get level type element
	type_elems.extend([doc.GetElement(l) for l in levelTypeIds])
	
	# loop type elements
	for elem in type_elems:
		# if endwiths not include in type name
		if not endWiths in elem.LookupParameter("Type Name").AsString():
			# add endwiths in type name
			elem.Name = elem.LookupParameter("Type Name").AsString() + endWiths
	# get type names
	type_names = [i.LookupParameter("Type Name").AsString() for i in type_elems]
	# type name parameter id
	paramId = type_elems[0].LookupParameter("Type Name").Id
	# create a "not ends with" filter rule
	notendswith = ParameterFilterRuleFactory.CreateNotEndsWithRule(paramId,endWiths,False)
	# create parameter filter element
	paramFilterElem = ParameterFilterElement.Create(doc, ifilter,CateIds,[notendswith])
	# set filter overrides (same with add filter to current)
	active_view.SetFilterOverrides(paramFilterElem.Id, OverrideGraphicSettings())
	# set filter visibility
	active_view.SetFilterVisibility(paramFilterElem.Id, unhide)
	
print "DONE!"
trans.Commit()