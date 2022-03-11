#written by Cyril.P
import clr
clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *

clr.AddReference('RevitAPI')
import Autodesk
from Autodesk.Revit.DB import *
clr.AddReference('RevitServices')
import RevitServices
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager
doc = DocumentManager.Instance.CurrentDBDocument

import sys
sys.path.append(r'C:\Program Files (x86)\IronPython 2.7\Lib')
import random

def nearCond(lstelemb, elema):
    """
    checking if the duct or element base line is close to the previous ones
    """
    global margin
    check = False
    curva = elema.Location.Curve
    midpta = elema.Location.Curve.Evaluate(0.5, True) 
    for elemb in lstelemb:
        curvb = elemb.Location.Curve
        if curvb.Project(midpta).Distance < margin:
            check = True
            break
    return check    

def getConduitParallal(collCond, conda):
    """
    get all conduits or elements parallel by vectors
    """
    outLst = []
    curva = conda.Location.Curve
    vecta = conda.Location.Curve.Direction
    midptfun = lambda x : x.Location.Curve.Evaluate(0.5, True) 
    midpta = midptfun(conda)
    for condb in collCond:
        if conda.Id != condb.Id :
            vectb = condb.Location.Curve.Direction
            if vecta.IsAlmostEqualTo(vectb, 0.15) or vecta.IsAlmostEqualTo(vectb.Negate(), 0.15) :
                outLst.append(condb)
    if outLst:
        #sort element by distance
        outLst.sort(key = lambda x : curva.Project(midptfun(x)).Distance )  
    return outLst                       
    
def colorRamdom(elements, view):
    """
    random function to color the elements in the view
    """
    TransactionManager.Instance.EnsureInTransaction(doc)
    rvtcolor = Color(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    gSettings = OverrideGraphicSettings()
    gSettings.SetProjectionFillColor(rvtcolor)
    gSettings.SetProjectionLineColor(rvtcolor)
    gSettings.SetCutLineColor(rvtcolor)
    gSettings.SetCutFillColor(rvtcolor) 
    for element in elements:
        view.SetElementOverrides(element.Id, gSettings)
    TransactionManager.Instance.TransactionTaskDone()


margin = IN[0] #max margin between conduits
collCond = UnwrapElement(IN[1])
if not hasattr(collCond, "__iter__"):
	collCond = [collCond]
#OR
#collCond = FilteredElementCollector(doc, doc.ActiveView.Id).OfCategory(BuiltInCategory.OST_Conduit).WhereElementIsNotElementType().ToElements()


finalgroups = []
filterPassId = []
for conda in collCond:
    if conda.Id not in filterPassId:
        filterPassId.append(conda.Id)
        vecta = conda.Location.Curve.Direction
        templst = [conda]
        elemsParall = getConduitParallal(collCond, conda)
        for condb in elemsParall:
            if nearCond(templst, condb):
                templst.append(condb)
                filterPassId.append(condb.Id)       
        finalgroups.append(templst)     
        colorRamdom(templst, doc.ActiveView)

OUT = finalgroups
