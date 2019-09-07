#region Header
//
// CmdAnalyticalModelGeom.cs - retrieve analytical model geometry
//
// Copyright (C) 2011-2019 by Jeremy Tammik, Autodesk Inc. All rights reserved.
//
// Keywords: The Building Coder Revit API C# .NET add-in.
//
#endregion // Header

#region Namespaces
using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Text;
using System.Linq;
using Autodesk.Revit.ApplicationServices;
using Autodesk.Revit.Attributes;
using Autodesk.Revit.DB;
using Autodesk.Revit.DB.Structure;
using Autodesk.Revit.UI;
using Autodesk.Revit.UI.Selection;
using Autodesk.Revit.DB.PointClouds;
using System.IO;
using System.Xml;
using Autodesk.Revit.DB.Analysis;
#endregion // Namespaces

namespace BuildingCoder
{
  [Transaction( TransactionMode.Manual )]
  class CmdAnalyticalModelGeom : IExternalCommand
  {
    /// <summary>
    /// A list of all analytical curve types.
    /// </summary>
    static IEnumerable<AnalyticalCurveType>
      _curveTypes
        = Enum.GetValues( typeof( AnalyticalCurveType ) )
          .Cast<AnalyticalCurveType>();

    /// <summary>
    /// Offset at which to create a model curve copy
    /// of all analytical model curves.
    /// </summary>
    static XYZ _offset = new XYZ( 100, 0, 0 );

    /// <summary>
    /// Translation transformation to apply to create
    /// model curve copy of analytical model curves.
    /// </summary>
    //static Transform _t = Transform.get_Translation( _offset ); // 2013
    static Transform _t = Transform.CreateTranslation( _offset ); // 2014

    public Result Execute(
      ExternalCommandData commandData,
      ref string message,
      ElementSet elements )
    {
      UIApplication uiapp = commandData.Application;
      UIDocument uidoc = uiapp.ActiveUIDocument;
      Application app = uiapp.Application;
      Document doc = uidoc.Document;

      List<Element> walls = new List<Element>();

      //XYZ p;
      //List<XYZ> wall_start_points
      //  = walls.Select<Element, XYZ>( e => {
      //    Util.GetElementLocation( out p, e );
      //      return p; } )
      //        .ToList<XYZ>();

      if( !Util.GetSelectedElementsOrAll(
        walls, uidoc, typeof( Wall ) ) )
      {
        Selection sel = uidoc.Selection;
        //message = ( 0 < sel.Elements.Size ) // 2014
        message = ( 0 < sel.GetElementIds().Count ) // 2015
          ? "Please select some wall elements."
          : "No wall elements found.";
        return Result.Failed;
      }


      using( Transaction tx = new Transaction( doc ) )
      {
        tx.Start( "Create model curve copies of analytical model curves" );

        Creator creator = new Creator( doc );

        foreach( Wall wall in walls )
        {
          AnalyticalModel am = wall.GetAnalyticalModel();

          foreach( AnalyticalCurveType ct in _curveTypes )
          {
            IList<Curve> curves = am.GetCurves( ct );

            int n = curves.Count;

            Debug.Print( "{0} {1} curve{2}.",
              n, ct, Util.PluralSuffix( n ) );

            foreach( Curve curve in curves )
            {
              //creator.CreateModelCurve( curve.get_Transformed( _t ) ); // 2013

              creator.CreateModelCurve( curve.CreateTransformed( _t ) ); // 2014
            }
          }
        }
        tx.Commit();
      }
      return Result.Succeeded;
    }
  }
}
