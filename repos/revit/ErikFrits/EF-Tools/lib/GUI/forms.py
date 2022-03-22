from WPF_Base import my_WPF
from FindReplace import FindReplace
from SelectFromDict import select_from_dict


class ListItem:
    """Helper Class for displaying selected sheets in my custom GUI."""
    def __init__(self,  Name='Unnamed', element = None):
        self.Name       = Name
        self.IsChecked  = False
        self.element    = element