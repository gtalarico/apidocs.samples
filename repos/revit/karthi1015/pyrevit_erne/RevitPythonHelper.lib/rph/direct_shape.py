import clr
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import Curve, CurveLoop, DirectShape, ElementId, Line, XYZ
from Autodesk.Revit.DB import SolidOptions, GeometryCreationUtilities
from Autodesk.Revit.DB import BuiltInCategory as Bic
from System.Collections.Generic import List
from rpw import db, doc


def solidify_bbox(bbox, bottom_z_offset=0.0):
    """
    Creates a solid Generic Model DirectShape from given BoundingBox.
    :param bbox: BoundingBox
    :return: DirectShape
    """
    solid_opt = SolidOptions(ElementId.InvalidElementId, ElementId.InvalidElementId)

    bbox.Min = XYZ(bbox.Min.X, bbox.Min.Y, bbox.Min.Z - bottom_z_offset)
    b1 = XYZ(bbox.Min.X, bbox.Min.Y, bbox.Min.Z)
    b2 = XYZ(bbox.Max.X, bbox.Min.Y, bbox.Min.Z)
    b3 = XYZ(bbox.Max.X, bbox.Max.Y, bbox.Min.Z)
    b4 = XYZ(bbox.Min.X, bbox.Max.Y, bbox.Min.Z)
    bbox_height = bbox.Max.Z - bbox.Min.Z

    lines = List[Curve]()
    lines.Add(Line.CreateBound(b1, b2))
    lines.Add(Line.CreateBound(b2, b3))
    lines.Add(Line.CreateBound(b3, b4))
    lines.Add(Line.CreateBound(b4, b1))
    rectangle = [CurveLoop.Create(lines)]

    extrusion = GeometryCreationUtilities.CreateExtrusionGeometry(List[CurveLoop](rectangle),
                                                                  XYZ.BasisZ,
                                                                  bbox_height,
                                                                  solid_opt)

    category_id = ElementId(Bic.OST_GenericModel)

    with db.Transaction("solid_bbox_direct_shape"):
        direct_shape = DirectShape.CreateElement(doc, category_id, "A", "B")
        direct_shape.SetShape([extrusion])

        return direct_shape


def location_box(loc_point):
    """
    Creates a solid Generic Model DirectShape box from given LocationPoint.
    :param loc_point: XYZ
    :return: DirectShape
    """
    solid_opt = SolidOptions(ElementId.InvalidElementId,
                             ElementId.InvalidElementId)
    offset = 0.1
    b1 = XYZ(loc_point.X - offset,
             loc_point.Y - offset,
             loc_point.Z - offset)
    b2 = XYZ(loc_point.X + offset,
             loc_point.Y - offset,
             loc_point.Z - offset)
    b3 = XYZ(loc_point.X + offset,
             loc_point.Y + offset,
             loc_point.Z - offset)
    b4 = XYZ(loc_point.X - offset,
             loc_point.Y + offset,
             loc_point.Z - offset)
    height = 1.0

    rect = List[Curve]()
    rect.Add(Line.CreateBound(b1, b2))
    rect.Add(Line.CreateBound(b2, b3))
    rect.Add(Line.CreateBound(b3, b4))
    rect.Add(Line.CreateBound(b4, b1))
    loop = [CurveLoop.Create(rect)]

    loc_box = GeometryCreationUtilities.CreateExtrusionGeometry(List[CurveLoop](loop), XYZ.BasisZ, height, solid_opt)

    category_id = ElementId(Bic.OST_GenericModel)

    with db.Transaction("solid_loc_box_direct_shape"):
        ds = DirectShape.CreateElement(doc, category_id, "A", "B")
        ds.SetShape([loc_box])
