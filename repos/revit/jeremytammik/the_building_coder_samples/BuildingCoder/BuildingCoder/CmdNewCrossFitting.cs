#region Header
//
// CmdNewCrossFitting.cs - Create a new pipe cross fitting
//
// Copyright (C) 2014-2019 by Joe Ye and Jeremy Tammik, Autodesk Inc. All rights reserved.
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
using Autodesk.Revit.DB.Plumbing;
using Autodesk.Revit.UI;
using Autodesk.Revit.UI.Selection;
using Autodesk.Revit.DB.Mechanical;
#endregion // Namespaces

namespace BuildingCoder
{
  [Transaction( TransactionMode.Manual )]
  class CmdNewCrossFitting : IExternalCommand
  {
    #region Using routing preferences with NewTakeoffFitting
    Connector CreateTemporaryConnectorForTap()
    { 
      return null;
    }
    void SelectAndPlaceTakeOffFitting( Document doc )
    {
      ElementId mainDuctId = ElementId.InvalidElementId;

      // Get DuctType - we need this for its
      // RoutingPreferenceManager. This is how we assign
      // our tap object to be used. This is the settings
      // for the duct object we attach our tap to.

      Duct duct = doc.GetElement( mainDuctId ) as Duct;

      DuctType ductType = duct.DuctType;

      RoutingPreferenceManager routePrefManager
        = ductType.RoutingPreferenceManager;

      // Set Junction Prefernce to Tap.

      routePrefManager.PreferredJunctionType
        = PreferredJunctionType.Tap;

      // For simplicity sake, I remove all previous rules
      // for taps so I can just add what I want here.
      // This will probably vary.

      int initRuleCount = routePrefManager.GetNumberOfRules(
        RoutingPreferenceRuleGroupType.Junctions );

      for( int i = 0; i != initRuleCount; ++i )
      {
        routePrefManager.RemoveRule(
          RoutingPreferenceRuleGroupType.Junctions, 0 );
      }

      // Get FamilySymbol for Tap I want to use.

      FamilySymbol tapSym = null;
      doc.LoadFamilySymbol( "C:/FamilyLocation/MyTap.rfa",
        "MyTap", out tapSym );

      // Symbol needs to be activated before use.

      if( ( !tapSym.IsActive ) && ( tapSym != null ) )
      {
        tapSym.Activate();
        doc.Regenerate();
      }

      // Create Rule that utilizes the Tap. Use the argument
      // MEPPartId = ElementId for the desired FamilySymbol.

      RoutingPreferenceRule newRule
        = new RoutingPreferenceRule( tapSym.Id, "MyTap" );

      routePrefManager.AddRule(
        RoutingPreferenceRuleGroupType.Junctions, newRule );

      // To create a solid tap, we need to use the Revit
      // doc.Create.NewTakeoffFitting routine. For this,
      // we need a connector. If we don't have one, we
      // just create a temporary object with a connector
      // where we want it.

      Connector tmpConn = CreateTemporaryConnectorForTap();

      // Create our tap.

      FamilyInstance tapInst
        = doc.Create.NewTakeoffFitting( tmpConn, duct );
    }
    #endregion // Using routing preferences with NewTakeoffFitting

    /// <summary>
    /// Return the normalised direction of the given pipe.
    /// </summary>
    XYZ GetPipeDirection( Pipe pipe )
    {
      Curve c = pipe.GetCurve();
      XYZ dir = c.GetEndPoint( 1 ) - c.GetEndPoint( 1 );
      dir = dir.Normalize();
      return dir;
    }

    /// <summary>
    /// Are the two given pipes parallel?
    /// </summary>
    bool IsPipeParallel( Pipe p1, Pipe p2 )
    {
      Line c1 = p1.GetCurve() as Line;
      Line c2 = p2.GetCurve() as Line;
      return Math.Sin( c1.Direction.AngleTo(
        c2.Direction ) ) < 0.01;
    }

    /// <summary>
    /// External command mainline. Run in the 
    /// sample model TestCrossFitting.rvt, e.g.
    /// </summary>
    public Result Execute(
      ExternalCommandData commandData,
      ref string message,
      ElementSet elements )
    {
      UIApplication app = commandData.Application;
      UIDocument uidoc = app.ActiveUIDocument;
      Document doc = uidoc.Document;

      IList<Element> pipes = null;
      int n = 0;

      // Ensure that 2, 3 or 4 pipes are selected.

      while( n < 2 || 4 < n )
      {
        if( 0 != n )
        {
          Util.InfoMsg( string.Format(
            "You picked {0} pipe{1}. "
            + "Please only pick 2, 3 or 4.",
            n, Util.PluralSuffix( n ) ) );
        }

        try
        {
          Selection sel = app.ActiveUIDocument.Selection;

          pipes = sel.PickElementsByRectangle(
            new JtElementsOfClassSelectionFilter<Pipe>(),
            "Please pick some pipes." );
        }
        catch( Autodesk.Revit.Exceptions
          .InvalidOperationException )
        {
          return Result.Cancelled;
        }
        n = pipes.Count;
      }

      XYZ pt = null;

      using( Transaction tx = new Transaction( doc ) )
      {
        tx.Start( "CreateConnector" );
        if( pipes.Count() <= 1 )
          return Result.Cancelled;

        Pipe pipe1 = pipes[0] as Pipe;
        Pipe pipe2 = pipes[1] as Pipe;

        Curve curve1 = pipe1.GetCurve();
        Curve curve2 = pipe2.GetCurve();

        XYZ p1 = curve1.GetEndPoint( 0 );
        XYZ q1 = curve1.GetEndPoint( 1 );

        XYZ p2 = curve2.GetEndPoint( 0 );
        XYZ q2 = curve2.GetEndPoint( 1 );

        if( q1.DistanceTo( p2 ) < 0.1 )
        {
          pt = ( q1 + p2 ) * 0.5;
        }
        else if( q1.DistanceTo( q2 ) < 0.1 )
        {
          pt = ( q1 + q2 ) * 0.5;
        }
        else if( p1.DistanceTo( p2 ) < 0.1 )
        {
          pt = ( p1 + p2 ) * 0.5;
        }
        else if( p1.DistanceTo( q2 ) < 0.1 )
        {
          pt = ( p1 + q2 ) * 0.5;
        }
        else
        {
          message = "Please select two pipes "
            + "with near-by endpoints.";

          return Result.Failed;
        }

        Connector c1 = Util.GetConnectorClosestTo(
          pipe1, pt );

        Connector c2 = Util.GetConnectorClosestTo(
          pipe2, pt );

        if( pipes.Count() == 2 )
        {
          if( IsPipeParallel( pipe1, pipe2 ) == true )
          {
            doc.Create.NewUnionFitting( c1, c2 );
          }
          else
          {
            doc.Create.NewElbowFitting( c1, c2 );
          }
        }
        else if( pipes.Count() == 3 )
        {
          Pipe pipe3 = pipes[2] as Pipe;

          XYZ v1 = GetPipeDirection( pipe1 );
          XYZ v2 = GetPipeDirection( pipe2 );
          XYZ v3 = GetPipeDirection( pipe3 );

          Connector c3 = Util.GetConnectorClosestTo(
            pipe3, pt );

          if( Math.Sin( v1.AngleTo( v2 ) ) < 0.01 ) //平行
          {
            doc.Create.NewTeeFitting( c1, c2, c3 );
          }
          else //v1, 和v2 垂直.
          {
            if( Math.Sin( v3.AngleTo( v1 ) ) < 0.01 ) //v3, V1 平行
            {
              doc.Create.NewTeeFitting( c3, c1, c2 );
            }
            else //v3, v2 平行
            {
              doc.Create.NewTeeFitting( c3, c2, c1 );
            }
          }
        }
        else if( pipes.Count() == 4 )
        {
          Pipe pipe3 = pipes[2] as Pipe;
          Pipe pipe4 = pipes[3] as Pipe;

          Connector c3 = Util.GetConnectorClosestTo(
            pipe3, pt );

          Connector c4 = Util.GetConnectorClosestTo(
            pipe4, pt );

          //以从哪c1为入口.

          // The required connection order for a cross 
          // fitting is main – main – side - side.

          if( IsPipeParallel( pipe1, pipe2 ) )
          {
            doc.Create.NewCrossFitting(
              c1, c2, c3, c4 );
          }
          else if( IsPipeParallel( pipe1, pipe3 ) )
          {
            try
            {
              doc.Create.NewCrossFitting(
                c1, c3, c2, c4 );
            }
            catch( Exception ex )
            {
              TaskDialog.Show(
                "Cannot insert cross fitting",
                ex.Message );
            }
          }
          else if( IsPipeParallel( pipe1, pipe4 ) )
          {
            doc.Create.NewCrossFitting(
              c1, c4, c2, c3 );
          }
        }
        tx.Commit();
      }
      return Result.Succeeded;
    }
  }
}
