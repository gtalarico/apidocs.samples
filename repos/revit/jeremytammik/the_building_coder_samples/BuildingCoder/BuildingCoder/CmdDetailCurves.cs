#region Header
//
// CmdDetailCurves.cs - create detail curves
//
// Copyright (C) 2009-2019 by Jeremy Tammik,
// Autodesk Inc. All rights reserved.
//
// Keywords: The Building Coder Revit API C# .NET add-in.
//
#endregion // Header

#region Namespaces
using System.Collections.Generic;
using System.Linq;
using Autodesk.Revit.ApplicationServices;
using Autodesk.Revit.Attributes;
using Autodesk.Revit.DB;
using Autodesk.Revit.UI;
using Autodesk.Revit.UI.Selection;
#endregion // Namespaces

namespace BuildingCoder
{
  [Transaction( TransactionMode.Manual )]
  class CmdDetailCurves : IExternalCommand
  {
    /// <summary>
    /// Return a point projected onto a plane defined by its normal.
    /// http://www.euclideanspace.com/maths/geometry/elements/plane
    /// Case 1259133 [Curve must be in the plane]
    /// </summary>
    XYZ ProjectPointOntoPlane(
      XYZ point,
      XYZ planeNormal )
    {
      double a = planeNormal.X;
      double b = planeNormal.Y;
      double c = planeNormal.Z;

      double dx = ( b * b + c * c ) * point.X - ( a * b ) * point.Y - ( a * c ) * point.Z;
      double dy = -( b * a ) * point.X + ( a * a + c * c ) * point.Y - ( b * c ) * point.Z;
      double dz = -( c * a ) * point.X - ( c * b ) * point.Y + ( a * a + b * b ) * point.Z;
      return new XYZ( dx, dy, dz );
    }

    public Result Execute(
      ExternalCommandData commandData,
      ref string message,
      ElementSet elements )
    {
      UIApplication app = commandData.Application;
      UIDocument uidoc = app.ActiveUIDocument;
      Document doc = uidoc.Document;
      View view = doc.ActiveView;

      Autodesk.Revit.Creation.Document creDoc
        = doc.Create;

      #region Check for pre-selected wall element
      Selection sel = uidoc.Selection;
      ICollection<ElementId> ids = sel.GetElementIds();

      if( 1 == ids.Count )
      {
        Element e = doc.GetElement( ids.First<ElementId>() );
        if( e is Wall )
        {
          LocationCurve lc = e.Location as LocationCurve;
          Curve curve = lc.Curve;

          using( Transaction tx = new Transaction( doc ) )
          {
            tx.Start( "Create Detail Line in Wall Centre" );
            creDoc.NewDetailCurve( view, curve );
            tx.Commit();
          }
          return Result.Succeeded;
        }
      }
      #endregion // Check for pre-selected wall element

      // Create a geometry line

      XYZ startPoint = new XYZ( 0, 0, 0 );
      XYZ endPoint = new XYZ( 10, 10, 0 );

      //Line geomLine = creApp.NewLine( startPoint, endPoint, true ); // 2013

      Line geomLine = Line.CreateBound( startPoint, endPoint ); // 2014

      // Create a geometry arc

      XYZ end0 = new XYZ( 0, 0, 0 );
      XYZ end1 = new XYZ( 10, 0, 0 );
      XYZ pointOnCurve = new XYZ( 5, 5, 0 );

      //Arc geomArc = creApp.NewArc( end0, end1, pointOnCurve ); // 2013

      Arc geomArc = Arc.Create( end0, end1, pointOnCurve ); // 2014

#if NEED_PLANE
      // Create a geometry plane

      XYZ origin = new XYZ( 0, 0, 0 );
      XYZ normal = new XYZ( 1, 1, 0 );

      Plane geomPlane = creApp.NewPlane(
        normal, origin );

      // Create a sketch plane in current document

      SketchPlane sketch = creDoc.NewSketchPlane(
        geomPlane );
#endif // NEED_PLANE

      using( Transaction tx = new Transaction( doc ) )
      {
        tx.Start( "Create Detail Line and Arc" );

        // Create a DetailLine element using the
        // newly created geometry line and sketch plane

        DetailLine line = creDoc.NewDetailCurve(
          view, geomLine ) as DetailLine;

        // Create a DetailArc element using the
        // newly created geometry arc and sketch plane

        DetailArc arc = creDoc.NewDetailCurve(
          view, geomArc ) as DetailArc;

        // Change detail curve colour.
        // Initially, this only affects the newly
        // created curves. However, when the view
        // is refreshed, all detail curves will
        // be updated.

        GraphicsStyle gs = arc.LineStyle as GraphicsStyle;

        gs.GraphicsStyleCategory.LineColor
          = new Color( 250, 10, 10 );

        tx.Commit();
      }
      return Result.Succeeded;
    }
  }
}
