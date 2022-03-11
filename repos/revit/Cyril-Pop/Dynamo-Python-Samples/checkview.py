#Copyright(c) 2019 Cyril.P
def checkview(view, import_inst):
    if not view.IsTemplate:
        #get importinstance in each view
        lst_inst = FilteredElementCollector(doc, view.Id).OfClass(ImportInstance).ToElements()
        #if import is in this wiew and the view is depend of a viewtemplate
        if any([import_inst.Id == x.Id for x in lst_inst]) and doc.GetElement(view.ViewTemplateId) is not None:
            #get the view template
            viewtempl = doc.GetElement(view.ViewTemplateId)
            lstnotcontrol = viewtempl.GetNonControlledTemplateParameterIds()
            #if the category is control by the viewtemplate
            if any([BuiltInParameter.VIS_GRAPHICS_IMPORT.value__ == x.IntegerValue for x in lstnotcontrol]):
                return view
            #if the category is not control by the viewtemplate    
            else:
                return  viewtempl
        #else import is in this wiew and the view is not depend of a viewtemplate        
        elif any([import_inst.Id == x.Id for x in lst_inst]):
            return view
        else:
            return None
    else:
        return None
