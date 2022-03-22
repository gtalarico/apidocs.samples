# based on building coder article:
# https://thebuildingcoder.typepad.com/blog/2012/04/adding-a-category-to-a-shared-parameter-binding.html

from Autodesk.Revit.DB import *

# custom result class
import Result as res
# import InTransaction from common module
import RevitCommonAPI as com

# opens a shared parameter file
def LoadSharedParameterFile(doc, path):
    app = doc.Application
    app.SharedParametersFilename = path
    return app.OpenSharedParameterFile()


# binds a shared parameter to a revit category
# refer building coder articel referenced in header
# parameterGrouping : where parameter appears in properties section in UI
# groupName: name of group parameter is under in Shared Parameter file
# category: expects built in category, to which the parameter will be bound
def BindSharedParameter(doc, category, parameterName, groupName, parameterType, isVisible, isInstance, parameterGrouping, sharedParameterFilepath):
    
    returnvalue = res.Result()
    try:
    
        app = doc.Application
    
        # This is needed already here to 
        # store old ones for re-inserting
        catSet = app.Create.NewCategorySet()
 
        # Loop all Binding Definitions
        # IMPORTANT NOTE: Categories.Size is ALWAYS 1 !?
        # For multiple categories, there is really one 
        # pair per each category, even though the 
        # Definitions are the same...
 
        iter = doc.ParameterBindings.ForwardIterator()
        iter.Reset()
        while iter.MoveNext():
            if(iter.Key != None):
                definition = iter.Key
                elemBind = iter.Current
                # check parameter name match
                if(parameterName == definition.Name):
                    try: 
                        cat = doc.Settings.Categories.get_Item(category)
                        if(elemBind.Categories.Contains(cat)):
                            # check parameter type
                            if(definition.ParameterType != parameterType):
                                returnvalue.status = False
                                returnvalue.message = parameterName + ': wrong paramter type: '+ str(definition.ParameterType)
                                return returnvalue
                            #check binding type
                            if(isInstance):
                                if(elemBind.GetType() != InstanceBinding):
                                    returnvalue.status = False
                                    returnvalue.message = parameterName + ': wrong binding type (looking for instance but got type)'
                                    return returnvalue
                            else:
                                if(elemBind.GetType() != TypeBinding):
                                    returnvalue.status = False
                                    returnvalue.message = parameterName + ': wrong binding type (looking for type but got instance)'
                                    return returnvalue
                    
                            # Check Visibility - cannot (not exposed)
                            # If here, everything is fine, 
                            # ie already defined correctly
                            returnvalue.message = parameterName + ': Parameter already bound to category: ' + str(cat.Name)
                            return returnvalue
                    except Exception as e:
                        print(parameterName + ' : Failed to check parameter binding' + str(e))
                    # If here, no category match, hence must 
                    # store "other" cats for re-inserting
                    else:
                        for catOld in elemBind.Categories:
                            catSet.Insert(catOld)

        # If here, there is no Binding Definition for 
        # it, so make sure Param defined and then bind it!
        defFile = LoadSharedParameterFile(doc,sharedParameterFilepath)
        defGroup = defFile.Groups.get_Item(groupName)
        if defGroup == None:
            defGroup = defFile.Groups.Create(groupName)
        if defGroup.Definitions.Contains(defGroup.Definitions.Item[parameterName]):
            definition = defGroup.Definitions.Item[parameterName]
        else:
            opt = ExternalDefinitionCreationOptions(parameterName, parameterType)
            opt.Visible = isVisible
            definition = defGroup.Definitions.Create(opt)

        #get category from builtin category
        catSet.Insert(doc.Settings.Categories.get_Item(category))

        bind = None
        if(isInstance):
            bind = app.Create.NewInstanceBinding(catSet)
        else:
            bind = app.Create.NewTypeBinding(catSet)
    
        # There is another strange API "feature". 
        # If param has EVER been bound in a project 
        # (in above iter pairs or even if not there 
        # but once deleted), Insert always fails!? 
        # Must use .ReInsert in that case.
        # See also similar findings on this topic in: 
        # http://thebuildingcoder.typepad.com/blog/2009/09/adding-a-category-to-a-parameter-binding.html 
        # - the code-idiom below may be more generic:

        def action():
            actionReturnValue = res.Result()
            try:
                if(doc.ParameterBindings.Insert(definition, bind, parameterGrouping)):
                    actionReturnValue.message =  parameterName + ' : parameter succesfully bound'
                    return actionReturnValue
                else:
                    if(doc.ParameterBindings.ReInsert(definition, bind, parameterGrouping)):
                        actionReturnValue.message = parameterName + ' : parameter succesfully bound'
                        return actionReturnValue
                    else:
                        actionReturnValue.status = False
                        actionReturnValue.message = parameterName + ' : failed to bind parameter!'
            except Exception as e:
                actionReturnValue.status = False
                actionReturnValue.message = parameterName + ' : Failed to bind parameter with exception: ' + str(e)
            return actionReturnValue
        transaction = Transaction(doc,'Binding parameter')
        returnvalue = com.InTransaction(transaction, action)    
        return returnvalue

    except Exception as e:
        returnvalue.status = False
        returnvalue.message = parameterName + ' : Failed to bind parameter with exception: ' + str(e)
    return returnvalue
