import System

from Autodesk.Revit.DB import *
from Autodesk.Revit.DB.Architecture import *
from Autodesk.Revit.DB.Analysis import *
from Autodesk.Revit.UI import *
from Autodesk.Revit.UI.Selection import *

from pyrevit import revit, DB, UI
from pyrevit import forms, script

from rpw.ui.forms import (FlexForm, Label, ComboBox, Separator, Button, TextBox)

#set the active Revit application and document
app = __revit__.Application
doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument
active_view = doc.ActiveView

# Category Ban List
cat_ban_list = [
    -2000260,   # dimensions
    -2000261,   # Automatic Sketch Dimensions
    -2000954,   # railing path extension lines
    -2000045,   # <Sketch>
    -2000067,   # <Stair/Ramp Sketch: Boundary>
    -2000262,   # Constraints
    -2000920,   # Landings
    -2000919,   # Stair runs
    -2000123,   # Supports
    -2000173,   # curtain wall grids
    -2000171,   # curtain wall mullions
    -2000530,   # reference places
    -2000127,   # Balusters
    -2000947,   # Handrail
    -2000946,   # Top Rail
    -2002000,    # Detail Items
    -2000150,    # Generic Annotations
    -2001260,    # Site
    -2000280,    # Title Blocks
    # -2000170,   # curtain panels
]

# Selection Filter
class CustomISelectionFilter(ISelectionFilter):
    def __init__(self, cat):
        self.cat = cat

    def AllowElement(self, e):
        if e.Category.Id.IntegerValue == int(self.cat):
            return True
        else:
            return False

    @staticmethod
    def AllowReference(ref, point):
        return True

def GetBICFromCat(_cat):
    # Convert categoryId to BuiltInCategory https://git.io/J1d6O @Gui Talarico    
    bic = System.Enum.ToObject(DB.BuiltInCategory, _cat.Id.IntegerValue)  
    return bic

def GetInstanceParameters(_cat):  
    el = DB.FilteredElementCollector(doc) \
    .WhereElementIsNotElementType() \
    .OfCategory(_cat) \
    .ToElements() 

    if not el:
        forms.alert("No elements of this category found in the project.")
        script.exit()

    parameters = [p.Definition.Name for p in el[0].Parameters \
        if p.StorageType == DB.StorageType.String and \
         p.Definition.ParameterType == DB.ParameterType.Text and \
         not p.IsReadOnly]

    return parameters

family_instances = DB.FilteredElementCollector(doc).OfClass(DB.FamilyInstance).ToElements() # get all family instance categories

# {key: value for value in list}
cat_dict1 = {f.Category.Name: f.Category \
        for f in [fam for fam in family_instances] \
        if f.Category.Id.IntegerValue not in cat_ban_list \
        and f.LevelId and f.get_Geometry(DB.Options())} 

cat_rooms = DB.Category.GetCategory(doc, DB.BuiltInCategory.OST_Rooms)
cat_dict1[cat_rooms.Name] = cat_rooms   # Add Rooms to the list of Categories

# construct rwp UI for Category
components = [
    Label("Pick Category:"),
    ComboBox(name="cat_combobox", options=cat_dict1, sorted=True),
    Button("Select")
]
form = FlexForm("Select", components)
form.show()

cat_name = ''

try:    
    # assign chosen parameters  
    cat_name = form.values["cat_combobox"].Name
except:
    forms.alert_ifnot(cat_name, "No selection", exitscript=True)


cat = GetBICFromCat(form.values["cat_combobox"])    #BuiltInCategory
param_dict1 = GetInstanceParameters(cat)

# construct rwp UI for Parameter and Prefix
components = [
    Label("Pick Parameter:"),
    ComboBox(name="param_combobox", options=param_dict1, sorted=True),
    Label("Prefix"),
    TextBox(name="prefix_box", Text="X00_", description ="Any prefix that you would like your numbering to have, such as 'ID_' for Interior Door"),
    Label("Leading zeroes"),
    TextBox(name="leading_box", Text="3"),
    Label("Starting element number"),
    TextBox(name="count_start", Text="1"),
    Button("Select")
]
form = FlexForm("Select", components)
form.show()

parameter = None
prefix = None
leading = None
start_count = None

try:    
    parameter = form.values["param_combobox"]
    prefix = form.values["prefix_box"]
    leading = int(form.values["leading_box"])    
    start_count = int(form.values["count_start"])    
except:
    if leading == None or prefix == None or start_count == None:
        if prefix == None:
            prefix = ""
        if leading == None:
            leading = 0
        if start_count == None:
            start_count = 1
    else:
        forms.alert("Bad selection, something's off")
        script.exit()

if not parameter:
    forms.alert("Bad parameter selection")
    script.exit()


try:
    TaskDialog.Show("Select Spline", "Select a spline, start of spline defines first")
    spline = doc.GetElement(uidoc.Selection.PickObject(UI.Selection.ObjectType.Element, \
        CustomISelectionFilter(DB.BuiltInCategory.OST_Lines), \
            "Select Spline"))
except:
    forms.alert("Aborted by User, no spline selected")
    script.exit()

try:
    TaskDialog.Show("Select Elements", "Select all the elements you want to renumber")
    elements = uidoc.Selection.PickObjects(UI.Selection.ObjectType.Element, CustomISelectionFilter(cat), \
            "Select Elements")
except:
    forms.alert("Aborted by User, no element selected")
    script.exit()

# The dictionary containing all keys=elements + values=location
el_dict = {}
sorted_el_dict = {}
parameters = []

for e in elements:
    el = doc.GetElement(e)
    loc = el.Location
    if loc:
        el_dict[el] = loc.Point
    else:
        el_dict[el] = el.get_BoundingBox(doc.ActiveView).Min

for dr, pt in el_dict.items():
    crv = spline.GeometryCurve
    param = crv.ComputeNormalizedParameter(crv.Project(pt).Parameter)
    sorted_el_dict[dr] = param
    parameters.append(param)

sorted = sorted(sorted_el_dict, key=sorted_el_dict.get)

counter = start_count

with revit.Transaction("Renumber Elements", doc):
    for el in sorted:
        value = \
            str(prefix + str(counter).zfill(leading)) \
            if (leading and leading > 0) else \
            str(prefix + str(counter))
        
        el.LookupParameter(parameter).Set(value)
        counter += 1

TaskDialog.Show("Success", "{0} {1} renumbered.".format(len(sorted), cat_name))