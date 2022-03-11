import clr
clr.AddReference("RevitAPI")
from pyrevit import script
from rpw.ui.forms import Console

__fullframeengine__ = True

__doc__ = "welcome to pyRevit sandbox find mechanisms on how to treat output in the script"

print("hello world!")
print("hello sandbox..")
output = script.get_output()
output.update_progress(50, 100)
output.set_font("System", 32)
output.print_md("Lines in view:")
output.print_md("<pre> Lines   in   view:</pre>")
output.print_md("####LINE COUNT IN CURRENT VIEW:")
output.print_md("**Lines in view:**")
output.print_md("foo <font color='red'>bar</font> foo")
output.print_code("import os  # testing markup")
output.print_code("os.getcwd()  # testing markup")
output.update_progress(90, 100)
# some comment
print(__doc__)
output.update_progress(100, 100)

# uncomment to get a rpw console: (handy for exploring)
# Console()
