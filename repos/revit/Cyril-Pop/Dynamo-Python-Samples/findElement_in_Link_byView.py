import clr
clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *

#import Revit API
clr.AddReference('RevitAPI')
import Autodesk
from Autodesk.Revit.DB import *

#import net library
import System
from System.Collections.Generic import List

clr.AddReference('RevitServices')
import RevitServices
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

#Get Important vars
doc = DocumentManager.Instance.CurrentDBDocument

def gen_PairPts(*args):
	"""
	generator for pair loop point
	"""
	for idx, pt in enumerate(args):
		try: yield pt, args[idx + 1]
		except : yield pt, args[0]

def solid_fromBBX(bbox, transform = None):
	"""
	Create Solid from BoundingBox
	"""
	pt0 = XYZ( bbox.Min.X, bbox.Min.Y, bbox.Min.Z )
	pt1 = XYZ( bbox.Max.X, bbox.Min.Y, bbox.Min.Z )
	pt2 = XYZ( bbox.Max.X, bbox.Max.Y, bbox.Min.Z )
	pt3 = XYZ( bbox.Min.X, bbox.Max.Y, bbox.Min.Z )
	#create generator
	pairPts = gen_PairPts(pt0, pt1, pt2, pt3) 
	#Create loop, still in BBox coords
	edges = List[Curve]()
	for pt1, pt2 in pairPts:
		edges.Add(Line.CreateBound( pt1, pt2 ))

	height = bbox.Max.Z - bbox.Min.Z
	baseLoop = CurveLoop.Create( edges )
	loopList = List[CurveLoop]()
	loopList.Add( baseLoop )
	outSolid = GeometryCreationUtilities.CreateExtrusionGeometry( loopList, XYZ.BasisZ, height )
	if transform is not None:
		if transform.Origin != XYZ.Zero: 
			outSolid = SolidUtils.CreateTransformed( outSolid, transform.Inverse )
				
	return outSolid

#Preparing input from dynamo to revit
linkinstance = UnwrapElement(IN[0])

transfLink = linkinstance.GetTotalTransform()
doclink = linkinstance.GetLinkDocument()

activeView = doc.ActiveView
if isinstance(activeView, ViewPlan):
	cropBoxBBX = activeView.CropBox 
	vrange = activeView.GetViewRange()
	bottomLvl = doc.GetElement(vrange.GetLevelId(PlanViewPlane.BottomClipPlane))
	topLvl = doc.GetElement(vrange.GetLevelId(PlanViewPlane.TopClipPlane))
	bottomOffset = vrange.GetOffset(PlanViewPlane.BottomClipPlane)
	topOffset = vrange.GetOffset(PlanViewPlane.TopClipPlane)
	
	#Recreate new BBX 
	cropBoxBBX.Min = XYZ(cropBoxBBX.Min.X, cropBoxBBX.Min.Y, bottomLvl.Elevation + bottomOffset)
	cropBoxBBX.Max = XYZ(cropBoxBBX.Max.X, cropBoxBBX.Max.Y, topLvl.Elevation + topOffset)
	#
	solidbbx = solid_fromBBX(cropBoxBBX, transfLink)
	filterSolid = ElementIntersectsSolidFilter(solidbbx)
	collFilter = FilteredElementCollector(doclink).WhereElementIsNotElementType().WherePasses(filterSolid).ToElements()
	
	OUT =  collFilter
