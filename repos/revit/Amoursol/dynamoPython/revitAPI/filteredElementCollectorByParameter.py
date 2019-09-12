"""
FILTERED ELEMENT COLLECTOR - ANALYTICAL MODEL PARAMETER ELEMENTS ONLY
"""
__author__ = 'Sol Amour - amoursol@gmail.com'
__twitter__ = '@solamour'
__version__ = '1.0.0'


# Importing Reference Modules
import clr # CLR ( Common Language Runtime Module )
clr.AddReference("RevitServices") # Adding the RevitServices.dll special Dynamo 
# module to deal with Revit
import RevitServices # Importing RevitServices
from RevitServices.Persistence import DocumentManager # From RevitServices 
# import the Document Manager
clr.AddReference("RevitAPI") # Adding the RevitAPI.dll module to access the Revit 
# API
import Autodesk # Here we import the Autodesk namespace
# From the Autodesk namespace - derived down to the Revit Database, we import only 
# the Filtered Element Collector and BuiltInCategory classes
from Autodesk.Revit.DB import *

# Here we give the Revit Document a nickname of 'doc' which allows us to simply 
# call 'doc' later without having to type the long namespace name 
doc = DocumentManager.Instance.CurrentDBDocument

# Here we use the Built In Parameter method to choose the parameter (yes/no tickbox) 
# of 'Enable Analytical Model' across all Elements inside of the Revit Document
param = BuiltInParameter.STRUCTURAL_ANALYTICAL_MODEL
# Once we have our BuiltInParameter, we need to get it's Element Id and convert it 
# to a Parameter Value Provider in order to use it inside of our filter
provider = ParameterValueProvider( ElementId( param ) )

# We then set up an empty instance of a Filter Numeric Equals to test against a set 
# value (In this case - whether or not the Element has the box ticked for 'Enable 
# Analytical Model'
evaluator = FilterNumericEquals()
# After we have the empty instance set up as our evaluator, we run a Filter Integer 
# Rule that checks the chosen parameter (Enable Anyalytical Model), runs against the 
# evaluator (Does this Number equal) and our value (1 which correlates to the tick 
# inside of our yes/no tickbox)
rule = FilterIntegerRule( provider, evaluator, 1 )
# After we have generated our Rule, we can generate a filter based off this rule
filter = ElementParameterFilter( rule )

# Now we have a valid rule to run against our Filtered Element Collector. So in this 
# case we pull everything inside the document - but only if it passes our filter (i.e 
# has the box ticked on for 'Enable Analytical Model') then make sure we return the 
# elements themselves. 
analyticalCollector = FilteredElementCollector( doc ).WherePasses( filter ).ToElements()

# To get our results back inside of Dynamo, we need to append a list to the OUT port
OUT = analyticalCollector
