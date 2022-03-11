﻿using Autodesk.Revit.Attributes;
using Autodesk.Revit.DB;
using Autodesk.Revit.UI;
using System.Collections.Generic;
using System.Windows;

namespace BIMiconToolbar.MatchGrids
{
    [TransactionAttribute(TransactionMode.Manual)]
    class MatchGrids : IExternalCommand
    {
        public Result Execute(ExternalCommandData commandData, ref string message, ElementSet elements)
        {
            Document doc = commandData.Application.ActiveUIDocument.Document;

            // Variables to store user input
            View selectedView;
            bool copyDims;
            List<int> selectedIntIds;

            // Prompt window to collect user input
            using (MatchGridsWPF customWindow = new MatchGridsWPF(commandData))
            {
                customWindow.ShowDialog();
                copyDims = customWindow.copyDim;
                selectedView = customWindow.SelectedComboItem.Tag as View;
                selectedIntIds = customWindow.IntegerIds;
            }

            // Check that elements have been selected
            if (selectedIntIds == null)
            {
                return Result.Cancelled;
            }
            else if (selectedIntIds.Count == 0)
            {
                TaskDialog.Show("Warning", "No views have been selected");
                return Result.Cancelled;
            }
            else if (selectedIntIds.Count != 0)
            {
                // Collect grids visible in view
                FilteredElementCollector gridsCollector = new FilteredElementCollector(doc, selectedView.Id)
                                                        .OfCategory(BuiltInCategory.OST_Grids)
                                                        .WhereElementIsNotElementType();

                // Grid Ids
                ICollection<ElementId> gridIds = gridsCollector.ToElementIds();

                // Template for grids display
                var gridsTemplate = new Dictionary<ElementId, bool[]>();

                // Check each grid
                foreach (Grid g in gridsCollector)
                {
                    bool end0 = g.IsBubbleVisibleInView(DatumEnds.End0, selectedView);
                    bool end1 = g.IsBubbleVisibleInView(DatumEnds.End1, selectedView);

                    bool[] endSettings = { end0, end1 };

                    gridsTemplate[g.Id] = endSettings;
                }

                // Retrieve views to be matched
                List<View> viewsToMatch = new List<View>();

                foreach (int intId in selectedIntIds)
                {
                    ElementId eId = new ElementId(intId);
                    View view = doc.GetElement(eId) as View;

                    viewsToMatch.Add(view);
                }

                // Transaction
                using (Transaction gridTransacation = new Transaction(doc, "Match grids"))
                {
                    gridTransacation.Start();

                    foreach (View vMatch in viewsToMatch)
                    {
                        // Collect grids visible in view
                        FilteredElementCollector gridsMatchCollector = new FilteredElementCollector(doc, vMatch.Id)
                                                                .OfCategory(BuiltInCategory.OST_Grids)
                                                                .WhereElementIsNotElementType();

                        // Match each visible grid in view
                        foreach (Grid gMatch in gridsMatchCollector)
                        {
                            ElementId gId = gMatch.Id;

                            if (gridIds.Contains(gId))
                            {
                                bool end0GridMatch = gMatch.IsBubbleVisibleInView(DatumEnds.End0, vMatch);
                                bool end1GridMatch = gMatch.IsBubbleVisibleInView(DatumEnds.End1, vMatch);

                                bool end0Temp = gridsTemplate[gId][0];
                                bool end1Temp = gridsTemplate[gId][1];

                                // Match End0
                                if (end0Temp == true && end0GridMatch == false)
                                {
                                    gMatch.ShowBubbleInView(DatumEnds.End0, vMatch);
                                }
                                else if (end0Temp == false && end0GridMatch)
                                {
                                    gMatch.HideBubbleInView(DatumEnds.End0, vMatch);
                                }

                                // Match End1
                                if (end1Temp == true && end1GridMatch == false)
                                {
                                    gMatch.ShowBubbleInView(DatumEnds.End1, vMatch);
                                }
                                else if (end1Temp == false && end1GridMatch)
                                {
                                    gMatch.HideBubbleInView(DatumEnds.End1, vMatch);
                                }
                            }
                        }
                    }

                    // Copy grid dimensions
                    if (copyDims)
                    {
                        // Collect dimensions in selected view
                        FilteredElementCollector dimensionsCollector = new FilteredElementCollector(doc, selectedView.Id)
                                                                .OfCategory(BuiltInCategory.OST_Dimensions)
                                                                .WhereElementIsNotElementType();

                        // Dimensions to copy
                        List<ElementId> dimsToCopy = new List<ElementId>();

                        // Check dimensions only take grids as references 
                        foreach (Dimension d in dimensionsCollector)
                        {
                            ReferenceArray dReferences = d.References;
                            bool gridDim = true;

                            foreach (Reference dRef in dReferences)
                            {
                                ElementId dRefId = dRef.ElementId;

                                if (!gridIds.Contains(dRefId))
                                {
                                    gridDim = false;
                                    break;
                                }
                            }

                            if (gridDim)
                            {
                                dimsToCopy.Add(d.Id);
                            }
                        }

                        // Copy dimensions
                        if (dimsToCopy.Count > 0)
                        {
                            CopyPasteOptions cp = new CopyPasteOptions();

                            foreach (View v in viewsToMatch)
                            {
                                ElementTransformUtils.CopyElements(selectedView, dimsToCopy, v, null, cp);
                            }
                        }
                    }

                    gridTransacation.Commit();
                }
            }

            return Result.Succeeded;
        }
    }
}
