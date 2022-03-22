#Copyright (c) Cyril.P
def SethiddenCad(viewtoset, viewname, visible_lst, hidden_lst):
    out = None
    TransactionManager.Instance.ForceCloseTransaction()
    TransactionManager.Instance.EnsureInTransaction(doc)
    for _idV in visible_lst:
        viewtoset.SetCategoryHidden(_idV, False)
    for _idH in hidden_lst:
        viewtoset.SetCategoryHidden(_idH, True)
    out = "Etat des calques appliqué sur la vue {}".format(viewname)
    TransactionManager.Instance.TransactionTaskDone()
    return  out
