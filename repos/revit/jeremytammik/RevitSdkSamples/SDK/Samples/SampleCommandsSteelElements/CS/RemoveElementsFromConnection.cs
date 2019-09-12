//
// (C) Copyright 2003-2019 by Autodesk, Inc.
//
// Permission to use, copy, modify, and distribute this software in
// object code form for any purpose and without fee is hereby granted,
// provided that the above copyright notice appears in all copies and
// that both that copyright notice and the limited warranty and
// restricted rights notice below appear in all supporting
// documentation.
//
// AUTODESK PROVIDES THIS PROGRAM "AS IS" AND WITH ALL FAULTS.
// AUTODESK SPECIFICALLY DISCLAIMS ANY IMPLIED WARRANTY OF
// MERCHANTABILITY OR FITNESS FOR A PARTICULAR USE. AUTODESK, INC.
// DOES NOT WARRANT THAT THE OPERATION OF THE PROGRAM WILL BE
// UNINTERRUPTED OR ERROR FREE.
//
// Use, duplication, or disclosure by the U.S. Government is subject to
// restrictions set forth in FAR 52.227-19 (Commercial Computer
// Software - Restricted Rights) and DFAR 252.227-7013(c)(1)(ii)
// (Rights in Technical Data and Computer Software), as applicable.
//


using Autodesk.Revit.DB;
using Autodesk.Revit.DB.Structure;
using Autodesk.Revit.UI;
using System.Collections.Generic;
using System.Linq;


namespace Revit.SDK.Samples.SampleCommandsSteelElements.RemoveElementsFromConnection.CS
{
   /// <summary>
   /// Implements the Revit add-in interface IExternalCommand
   /// </summary>
   [Autodesk.Revit.Attributes.Transaction(Autodesk.Revit.Attributes.TransactionMode.Manual)]
   [Autodesk.Revit.Attributes.Regeneration(Autodesk.Revit.Attributes.RegenerationOption.Manual)]
   [Autodesk.Revit.Attributes.Journaling(Autodesk.Revit.Attributes.JournalingMode.NoCommandData)]
   public class Command : IExternalCommand
   {
      /// <summary>
      /// Implement this method as an external command for Revit.
      /// </summary>
      /// <param name="commandData">An object that is passed to the external application 
      /// which contains data related to the command, 
      /// such as the application object and active view.</param>
      /// <param name="message">A message that can be set by the external application 
      /// which will be displayed if a failure or cancellation is returned by 
      /// the external command.</param>
      /// <param name="elements">A set of elements to which the external application 
      /// can add elements that are to be highlighted in case of failure or cancellation.</param>
      /// <returns>Return the status of the external command. 
      /// A result of Succeeded means that the API external method functioned as expected. 
      /// Cancelled can be used to signify that the user cancelled the external operation 
      /// at some point. Failure should be returned if the application is unable to proceed with 
      /// the operation.</returns>
      public virtual Result Execute(ExternalCommandData commandData
          , ref string message, ElementSet elements)
      {
         // Get the document from external command data.
         UIDocument activeDoc = commandData.Application.ActiveUIDocument;
         Autodesk.Revit.DB.Document doc = activeDoc.Document;

         if (null == doc)
         {
            return Result.Failed;
         }
         // The transaction and its status, using Revit's Transaction class
         Autodesk.Revit.DB.Transaction trans = new Autodesk.Revit.DB.Transaction(doc, "Remove element(s) from structural connection");
         TransactionStatus ts = TransactionStatus.Uninitialized;

         try
         {
            // Select the connection we need to remove elements from.
            // We use Revit's StructuralConnectionHandler class for the connection.
            // for more details, please consult http://www.autodesk.com/adv-steel-api-walkthroughs-2019-enu
            StructuralConnectionHandler conn = Utilities.Functions.SelectConnection(activeDoc);

            if (null == conn)
            {
               return Result.Failed;
            }
            // Select elements to remove from connection.
            IList<ElementId> ids = Utilities.Functions.SelectConnectionElements(activeDoc, "Select elements to remove from connection :");

            if (ids.Count() <= 0)
            {
               return Result.Failed;
            }

            // Starting the transaction
            trans.Start();
            // Removing the elements from the connection
            conn.RemoveElementIds(ids);
            // Committing the transaction
            ts = trans.Commit();

            if (ts != TransactionStatus.Committed)
            {
               message = "Failed to commit the current transaction !";
               if (ts != TransactionStatus.Uninitialized) trans.RollBack();
               return Result.Failed;
            }
         }

         catch (Autodesk.Revit.Exceptions.OperationCanceledException)
         {
            if (ts != TransactionStatus.Uninitialized)
            {
               trans.RollBack();
            }
            trans.Dispose();
            return Result.Cancelled;
         }

         catch (Autodesk.Revit.Exceptions.ArgumentException)
         {
            if (ts != TransactionStatus.Uninitialized)
            {
               trans.RollBack();
            }
            trans.Dispose();
            message = "Invalid elements selected!";
            return Result.Failed;
         }
         return Result.Succeeded;
      }
   }
}

