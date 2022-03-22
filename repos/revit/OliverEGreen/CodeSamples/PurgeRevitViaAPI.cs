using System;
using System.Collections.Generic;
using System.Linq;
using Autodesk.Revit.DB;

internal static class PurgeDocument
{
    internal static List<ElementId> GetPurgeableElements(Document doc, List<PerformanceAdviserRuleId> performanceAdviserRuleIds)
    {
        List<FailureMessage> failureMessages = PerformanceAdviser.GetPerformanceAdviser().ExecuteRules(doc, performanceAdviserRuleIds).ToList();
        if(failureMessages.Count > 0)
        {
            List<ElementId> purgeableElementIds = failureMessages[0].GetFailingElements().ToList();
            return purgeableElementIds;
        }
        return null;
    }

    public static void Purge(Document doc)
    {
        //The internal GUID of the Performance Adviser Rule 
        const string PurgeGuid = "e8c63650-70b7-435a-9010-ec97660c1bda";

        List<PerformanceAdviserRuleId> performanceAdviserRuleIds = new List<PerformanceAdviserRuleId>();

        //Iterating through all PerformanceAdviser rules looking to find that which matches PURGE_GUID
        foreach(PerformanceAdviserRuleId performanceAdviserRuleId in PerformanceAdviser.GetPerformanceAdviser().GetAllRuleIds())
        {
            if(performanceAdviserRuleId.Guid.ToString() == PurgeGuid)
            {
                performanceAdviserRuleIds.Add(performanceAdviserRuleId);
                break;
            }
        }

        //Attempting to recover all purgeable elements and delete them from the document
        List<ElementId> purgeableElementIds = GetPurgeableElements(doc, performanceAdviserRuleIds);
        if(purgeableElementIds != null) { doc.Delete(purgeableElementIds); }
    }
}
