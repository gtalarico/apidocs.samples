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

clr.AddReference("RevitNodes")
import Revit
clr.ImportExtensions(Revit.GeometryConversion)

import sys
sys.path.append(r'C:\Program Files (x86)\IronPython 2.7\Lib')
import os

def readidxfile(file):
	with open(file, "r") as f:
		return int(f.read())

def setidxfile(file, idx):
	with open(file, "w") as f:
		return f.write(str(idx))
		
		
dataEnteringNode = IN
time = IN[0] #input DateTime.Now() node
modelcurve = UnwrapElement(IN[1])
instance = UnwrapElement(IN[2])

pathuser  = os.path.expanduser('~')
fullpath = pathuser + "\\Documents\\objb.txt"

try:
	oldidx = readidxfile(fullpath)
	indx = oldidx + 1
	setidxfile(fullpath, indx)
except:	
	indx = 0
	setidxfile(fullpath, str(indx))
#create range
rangeint = range(1,11,1)
#create simple float range
floatrange = [x * 0.1 for x in rangeint]
curveproto  = modelcurve.GeometryCurve.ToProtoType()
try:
	ptx = curveproto.PointAtParameter(floatrange[indx])
except:
	indx = 0
	setidxfile(fullpath, indx)
	ptx = curveproto.PointAtParameter(floatrange[indx])
TransactionManager.Instance.EnsureInTransaction(doc)
instance.Location.Point = ptx.ToXyz()
TransactionManager.Instance.TransactionTaskDone()
	

OUT = ptx
