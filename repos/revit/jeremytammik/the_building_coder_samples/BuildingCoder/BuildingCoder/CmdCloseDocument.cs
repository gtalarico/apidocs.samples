#region Header
//
// CmdCloseDocument.cs - close active document by sending Windows message
//
// Copyright (C) 2010-2019 by Jeremy Tammik,
// Autodesk Inc. All rights reserved.
//
// Keywords: The Building Coder Revit API C# .NET add-in.
//
#endregion // Header

#region Namespaces
using System;
using System.Threading;
using System.Windows.Forms;
using Autodesk.Revit.Attributes;
using Autodesk.Revit.DB;
using Autodesk.Revit.UI;
#endregion // Namespaces

namespace BuildingCoder
{
  [Transaction( TransactionMode.ReadOnly )]
  class CmdCloseDocument : IExternalCommand
  {
    public Result Execute(
      ExternalCommandData commandData,
      ref string message,
      ElementSet elements )
    {
      ThreadPool.QueueUserWorkItem(
        new WaitCallback( CloseDocProc ) );

      return Result.Succeeded;
    }

    static void CloseDocProc( object stateInfo )
    {
      try
      {
        // maybe we need some checks for the right
        // document, but this is a simple sample...

        SendKeys.SendWait( "^{F4}" );
      }
      catch (Exception ex)
      {
        Util.ErrorMsg( ex.Message );
      }
    }

    static void CloseDocByCommand( UIApplication uiapp )
    {
      RevitCommandId closeDoc
        = RevitCommandId.LookupPostableCommandId(
          PostableCommand.Close );

      uiapp.PostCommand( closeDoc );
    }
  }
}
