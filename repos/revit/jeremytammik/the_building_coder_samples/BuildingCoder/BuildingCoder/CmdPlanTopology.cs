#region Header
//
// CmdPlanTopology.cs - test PlanTopology class
//
// Copyright (C) 2009-2019 by Jeremy Tammik,
// Autodesk Inc. All rights reserved.
//
// Keywords: The Building Coder Revit API C# .NET add-in.
//
#endregion // Header

#region Namespaces
using System;
using Autodesk.Revit.ApplicationServices;
using Autodesk.Revit.Attributes;
using Autodesk.Revit.DB;
using Autodesk.Revit.DB.Architecture;
using Autodesk.Revit.UI;
//using RoomCreationData = Autodesk.Revit.Creation.RoomCreationData;
#endregion // Namespaces

namespace BuildingCoder
{
  [Transaction( TransactionMode.Manual )]
  class CmdPlanTopology : IExternalCommand
  {
    /// <summary>
    /// Return element bounding box centre point
    /// </summary>
    public XYZ GetElementBbCenter( Element e )
    {
      BoundingBoxXYZ bb = e.get_BoundingBox( null );
      XYZ center = Util.Midpoint( bb.Min, bb.Max );
      return center;
    }

    /// <summary>
    /// Return room centre point for placing room tag
    /// </summary>
    public XYZ GetRoomCenter( Room room )
    {
      // cf. https://forums.autodesk.com/t5/revit-api-forum/create-roomtag/m-p/7871671

      // Room location point is not necessarily in the 
      // centre of the room, but the Z elevation is correct.

      LocationPoint locPt = (LocationPoint) room.Location;
      XYZ pr = locPt.Point;

      // Get the room center point X and Y from its bounding box.

      XYZ pbb = GetElementBbCenter( room );
      XYZ roomCenter = new XYZ( pbb.X, pbb.Y, pr.Z );
      return roomCenter;
    }

    /// <summary>
    /// Create a room on a given level.
    /// </summary>
    void CreateRoom(
      Document doc,
      Level level )
    {
      Application app = doc.Application;

      Autodesk.Revit.Creation.Application
        appCreation = app.Create;

      Autodesk.Revit.Creation.Document
        docCreation = doc.Create;

      XYZ pt1 = new XYZ( 0, -5, 0 );
      XYZ pt2 = new XYZ( 0, 5, 0 );
      XYZ pt3 = new XYZ( 8, 5, 0 );
      XYZ pt4 = new XYZ( 8, -5, 0 );

      Line line1 = Line.CreateBound( pt1, pt2 );
      Line line2 = Line.CreateBound( pt2, pt3 );
      Line line3 = Line.CreateBound( pt3, pt4 );
      Line line4 = Line.CreateBound( pt4, pt1 );

      CurveArray curveArr = new CurveArray();

      curveArr.Append( line1 );
      curveArr.Append( line2 );
      curveArr.Append( line3 );
      curveArr.Append( line4 );

      docCreation.NewRoomBoundaryLines(
        doc.ActiveView.SketchPlane,
        curveArr, doc.ActiveView );

      // Create a new room

      UV tagPoint = new UV( 4, 0 );

      Room room = docCreation.NewRoom(
        level, tagPoint );

      if( null == room )
      {
        throw new Exception(
          "Create a new room failed." );
      }
      room.Number = "42";
      room.Name = "Lobby";

      // Creation.Document.NewRoomTag( Room, UV, View) is obsolete.
      // Use the NewRoomTag(LinkElementId, UV, ElementId) overload instead.

      //RoomTag tag = docCreation.NewRoomTag( room, tagPoint, doc.ActiveView ); // 2013

      RoomTag tag = docCreation.NewRoomTag(
        new LinkElementId( room.Id ), tagPoint,
        doc.ActiveView.Id ); // 2014
    }

    public Result Execute(
      ExternalCommandData commandData,
      ref string message,
      ElementSet elements )
    {
      UIApplication app = commandData.Application;
      Document doc = app.ActiveUIDocument.Document;

      FilteredElementCollector levels = Util.GetElementsOfType(
        doc, typeof( Level ), BuiltInCategory.OST_Levels );

      Level level = levels.FirstElement() as Level;

      PlanTopology pt = doc.get_PlanTopology( level );

      // Collect some data on each room in the circuit

      string output = "Rooms on "
        + level.Name + ":"
        + "\n  Name and Number : Area";

      //foreach( Room r in pt.Rooms ) // 2012

      foreach( ElementId id in pt.GetRoomIds() ) // 2013
      {
        Room r = doc.GetElement( id ) as Room;

        output += "\n  " + r.Name + " : "
          + Util.RealString( r.Area ) + " sqf";
      }
      Util.InfoMsg( output );

      output = "Circuits without rooms:"
        + "\n  Number of Sides : Area";

      using( Transaction t = new Transaction( doc ) )
      {
        t.Start( "Create New Rooms" );

        foreach( PlanCircuit pc in pt.Circuits )
        {
          if( !pc.IsRoomLocated ) // this circuit has no room, create one
          {
            output += "\n  " + pc.SideNum + " : "
              + Util.RealString( pc.Area ) + " sqf";

            // Pass null to create a new room;
            // to place an existing unplaced room,
            // pass it in instead of null:

            Room r = doc.Create.NewRoom( null, pc );
          }
        }
        t.Commit();
      }
      Util.InfoMsg( output );

      return Result.Succeeded;
    }
  }
}
