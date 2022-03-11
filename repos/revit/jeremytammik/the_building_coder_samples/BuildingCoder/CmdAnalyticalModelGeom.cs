#region Header

//
// CmdAnalyticalModelGeom.cs - retrieve analytical model geometry
//
// Copyright (C) 2011-2021 by Jeremy Tammik, Autodesk Inc. All rights reserved.
//
// Keywords: The Building Coder Revit API C# .NET add-in.
//

#endregion // Header

#region Namespaces

using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using Autodesk.Revit.Attributes;
using Autodesk.Revit.DB;
using Autodesk.Revit.DB.Structure;
using Autodesk.Revit.UI;

#endregion // Namespaces

namespace BuildingCoder
{
    [Transaction(TransactionMode.Manual)]
    internal class CmdAnalyticalModelGeom : IExternalCommand
    {
        /// <summary>
        ///     A list of all analytical curve types.
        /// </summary>
        private static readonly IEnumerable<AnalyticalCurveType>
            CurveTypes = Enum.GetValues(typeof(AnalyticalCurveType)).Cast<AnalyticalCurveType>();

        /// <summary>
        ///     Offset at which to create a model curve copy
        ///     of all analytical model curves.
        /// </summary>
        private static readonly XYZ Offset = new(100, 0, 0);

        /// <summary>
        ///     Translation transformation to apply to create
        ///     model curve copy of analytical model curves.
        /// </summary>
        //static Transform _t = Transform.get_Translation( _offset ); // 2013
        private static readonly Transform T = Transform.CreateTranslation(Offset); // 2014

        public Result Execute(
            ExternalCommandData commandData,
            ref string message,
            ElementSet elements)
        {
            var uiapp = commandData.Application;
            var uidoc = uiapp.ActiveUIDocument;
            var app = uiapp.Application;
            var doc = uidoc.Document;

            var walls = new List<Element>();

            //XYZ p;
            //List<XYZ> wall_start_points
            //  = walls.Select<Element, XYZ>( e => {
            //    Util.GetElementLocation( out p, e );
            //      return p; } )
            //        .ToList<XYZ>();

            if (!Util.GetSelectedElementsOrAll(
                walls, uidoc, typeof(Wall)))
            {
                var sel = uidoc.Selection;
                //message = ( 0 < sel.Elements.Size ) // 2014
                message = 0 < sel.GetElementIds().Count // 2015
                    ? "Please select some wall elements."
                    : "No wall elements found.";
                return Result.Failed;
            }


            using var tx = new Transaction(doc);
            tx.Start("Create model curve copies of analytical model curves");

            var creator = new Creator(doc);

            foreach (Wall wall in walls)
            {
                var am = wall.GetAnalyticalModel();

                foreach (var ct in CurveTypes)
                {
                    var curves = am.GetCurves(ct);

                    var n = curves.Count;

                    Debug.Print("{0} {1} curve{2}.",
                        n, ct, Util.PluralSuffix(n));

                    foreach (var curve in curves)
                        //creator.CreateModelCurve( curve.get_Transformed( _t ) ); // 2013

                        creator.CreateModelCurve(curve.CreateTransformed(T)); // 2014
                }
            }

            tx.Commit();

            return Result.Succeeded;
        }
    }
}
