#region Header
//
// CmdEditFloor.cs - read existing floor geometry and create a new floor
//
// Copyright (C) 2008-2019 by Jeremy Tammik,
// Autodesk Inc. All rights reserved.
//
// Keywords: The Building Coder Revit API C# .NET add-in.
//
#endregion // Header

#region Namespaces
using System;
using System.Collections.Generic;
using System.Diagnostics;
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
  class CmdEditFloor : IExternalCommand
  {
    #region Super simple floor creation
    Result Execute2(
      ExternalCommandData commandData,
      ref string message,
      ElementSet elements )
    {
      UIApplication uiapp = commandData.Application;
      UIDocument uidoc = uiapp.ActiveUIDocument;
      Document doc = uidoc.Document;

      using( Transaction tx = new Transaction( doc ) )
      {
        tx.Start( "Create a Floor" );

        int n = 4;
        XYZ[] points = new XYZ[n];
        points[0] = XYZ.Zero;
        points[1] = new XYZ( 10.0, 0.0, 0.0 );
        points[2] = new XYZ( 10.0, 10.0, 0.0 );
        points[3] = new XYZ( 0.0, 10.0, 0.0 );

        CurveArray curve = new CurveArray();

        for( int i = 0; i < n; i++ )
        {
          Line line = Line.CreateBound( points[i],
            points[( i < n - 1 ) ? i + 1 : 0] );

          curve.Append( line );
        }

        doc.Create.NewFloor( curve, true );

        tx.Commit();
      }
      return Result.Succeeded;
    }
    #endregion // Super simple floor creation

    /// <summary>
    /// Return the uppermost horizontal face
    /// of a given "horizontal" solid object
    /// such as a floor slab. Currently only
    /// supports planar faces.
    /// </summary>
    PlanarFace GetTopFace( Solid solid )
    {
      PlanarFace topFace = null;
      FaceArray faces = solid.Faces;
      foreach( Face f in faces )
      {
        PlanarFace pf = f as PlanarFace;
        if( null != pf
          && Util.IsHorizontal( pf ) )
        {
          if( ( null == topFace )
            || ( topFace.Origin.Z < pf.Origin.Z ) )
          {
            topFace = pf;
          }
        }
      }
      return topFace;
    }

    #region Attempt to include inner loops
#if ATTEMPT_TO_INCLUDE_INNER_LOOPS
    /// <summary>
    /// Convert an EdgeArrayArray to a CurveArray,
    /// possibly including multiple loops.
    /// All non-linear segments are approximated by
    /// the edge curve tesselation.
    /// </summary>
    CurveArray Convert( EdgeArrayArray eaa )
    {
      CurveArray ca = new CurveArray();
      List<XYZ> pts = new List<XYZ>();

      XYZ q;
      string s;
      int iLoop = 0;

      foreach( EdgeArray ea in eaa )
      {
        q = null;
        s = string.Empty;
        pts.Clear();

        foreach( Edge e in ea )
        {
          IList<XYZ> a = e.Tessellate();
          bool first = true;
          //XYZ p0 = null;

          foreach( XYZ p in a )
          {
            if( first )
            {
              if( null == q )
              {
                s += Util.PointString( p );
                pts.Add( p );
              }
              else
              {
                Debug.Assert( p.IsAlmostEqualTo( q ), "expected connected sequential edges" );
              }
              first = false;
              //p0 = p;
              q = p;
            }
            else
            {
              s += " --> " + Util.PointString( p );
              //ca.Append( Line.get_Bound( q, p ) );
              pts.Add( p );
              q = p;
            }
          }
          //ca.Append( Line.get_Bound( q, p0 ) );
        }

        Debug.Print( "{0}: {1}", iLoop++, s );

        // test case: break after first edge loop,
        // which we assume to be the outer:

        //break;

        {
          // try reversing all the inner loops:

          if( 1 < iLoop )
          {
            pts.Reverse();
          }

          bool first = true;

          foreach( XYZ p in pts )
          {
            if( first )
            {
              first = false;
            }
            else
            {
              ca.Append( Line.get_Bound( q, p ) );
            }
            q = p;
          }
        }
      }
      return ca;
    }
#endif // ATTEMPT_TO_INCLUDE_INNER_LOOPS
    #endregion // Attempt to include inner loops

    public Result Execute(
      ExternalCommandData commandData,
      ref string message,
      ElementSet elements )
    {
      UIApplication app = commandData.Application;
      UIDocument uidoc = app.ActiveUIDocument;
      Document doc = uidoc.Document;

      // Retrieve selected floors, or all floors, if nothing is selected:

      List<Element> floors = new List<Element>();
      if( !Util.GetSelectedElementsOrAll(
        floors, uidoc, typeof( Floor ) ) )
      {
        Selection sel = uidoc.Selection;
        message = ( 0 < sel.GetElementIds().Count )
          ? "Please select some floor elements."
          : "No floor elements found.";
        return Result.Failed;
      }

      // Determine top face of each selected floor:

      int nNullFaces = 0;
      List<Face> topFaces = new List<Face>();
      Options opt = app.Application.Create.NewGeometryOptions();

      foreach( Floor floor in floors )
      {
        GeometryElement geo = floor.get_Geometry( opt );

        //GeometryObjectArray objects = geo.Objects; // 2012

        foreach( GeometryObject obj in geo )
        {
          Solid solid = obj as Solid;
          if( solid != null )
          {
            PlanarFace f = GetTopFace( solid );
            if( null == f )
            {
              Debug.WriteLine(
                Util.ElementDescription( floor )
                + " has no top face." );
              ++nNullFaces;
            }
            topFaces.Add( f );
          }
        }
      }

      using ( Transaction t = new Transaction( doc ) )
      {
        t.Start( "Create Model Lines and Floor" );

        // Create new floors from the top faces found.
        // Before creating the new floor, we would obviously
        // apply whatever modifications are required to the
        // new floor profile:

        Autodesk.Revit.Creation.Application creApp = app.Application.Create;
        Autodesk.Revit.Creation.Document creDoc = doc.Create;

        int i = 0;
        int n = topFaces.Count - nNullFaces;

        Debug.Print(
          "{0} top face{1} found.",
          n, Util.PluralSuffix( n ) );

        foreach ( Face f in topFaces )
        {
          Floor floor = floors[i++] as Floor;

          if ( null != f )
          {
            EdgeArrayArray eaa = f.EdgeLoops;
            CurveArray profile;

            #region Attempt to include inner loops
#if ATTEMPT_TO_INCLUDE_INNER_LOOPS
          bool use_original_loops = true;
          if( use_original_loops )
          {
            profile = Convert( eaa );
          }
          else
#endif // ATTEMPT_TO_INCLUDE_INNER_LOOPS
            #endregion // Attempt to include inner loops

            {
              profile = new CurveArray();

              // Only use first edge array,
              // the outer boundary loop,
              // skip the further items
              // representing holes:

              EdgeArray ea = eaa.get_Item( 0 );
              foreach ( Edge e in ea )
              {
                IList<XYZ> pts = e.Tessellate();
                int m = pts.Count;
                XYZ p = pts[0];
                XYZ q = pts[m - 1];
                Line line = Line.CreateBound( p, q );
                profile.Append( line );
              }
            }
            //Level level = floor.Level; // 2013

            Level level = doc.GetElement( floor.LevelId )
              as Level; // 2014

            // In this case we have a valid floor type given.
            // In general, not that NewFloor will only accept 
            // floor types whose IsFoundationSlab predicate
            // is false.

            floor = creDoc.NewFloor( profile,
              floor.FloorType, level, true );

            XYZ v = new XYZ( 5, 5, 0 );

            //doc.Move( floor, v ); // 2011
            ElementTransformUtils.MoveElement( doc, floor.Id, v ); // 2012
          }
        }
        t.Commit();
      }
      return Result.Succeeded;
    }

    #region Set Floor Level and Offset
    void SetFloorLevelAndOffset( Document doc )
    {
      // Pick first floor found

      Floor floor
        = new FilteredElementCollector( doc )
          .WhereElementIsNotElementType()
          .OfCategory( BuiltInCategory.OST_Floors )
          .OfClass( typeof( Floor ) )
          .FirstElement() as Floor;

      // Get first level not used by floor

      int levelIdInt = floor.LevelId.IntegerValue;

      Element level
        = new FilteredElementCollector( doc )
          .WhereElementIsNotElementType()
          .OfCategory( BuiltInCategory.OST_Levels )
          .OfClass( typeof( Level ) )
          .FirstOrDefault<Element>( e 
            => e.Id.IntegerValue.Equals( 
              levelIdInt ) );

      if( null != level )
      {
        // from https://forums.autodesk.com/t5/revit-api-forum/changing-the-level-id-and-offset-height-of-floors/m-p/8714247

        Parameter p = floor.get_Parameter(
          BuiltInParameter.LEVEL_PARAM );

        Parameter p1 = floor.get_Parameter(
          BuiltInParameter.FLOOR_HEIGHTABOVELEVEL_PARAM );

        using( Transaction tx = new Transaction( doc ) )
        {
          tx.Start( "Set Floor Level" );
          p.Set( level.Id ); // set new level Id
          p1.Set( 2 ); // set new offset from level
          tx.Commit();
        }
      }
    }
    #endregion // Set Floor Level and Offset
  }
}
