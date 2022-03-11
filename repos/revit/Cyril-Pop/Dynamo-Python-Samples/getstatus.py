#Copyright (c) Cyril.P
def getstatus(view, import_instance):
    hidden = []
    visible = []
    catSub = import_instance.Category.SubCategories
    for cat_cad in catSub:
        in_view = view.GetCategoryHidden(cat_cad.Id)
        if in_view:
            hidden.append(cat_cad.Id)
        else:
            visible.append(cat_cad.Id)
    return hidden, visible
