#
#License:
#
#
# Revit Batch Processor Sample Code
#
# Copyright (c) 2020  Jan Christel
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#

import clr
clr.AddReference('System.Windows.Forms')
clr.AddReference('IronPython.Wpf')

# import WPF creator and base window
import wpf
from System import Windows
import ctypes

# import settings class
import FileSelectSettings as set

# simple message box
def Mbox(title, text, style):
        return ctypes.windll.user32.MessageBoxW(0, text, title, style)

# UI class
class MyWindow (Windows.Window):
    def __init__(self, xamlFullFileName, revitFiles, settings):
        
        wpf.LoadComponent(self,xamlFullFileName)

        # populate fields
        self.selectedFiles = []
        self.revitfiles = revitFiles
        self.files.ItemsSource = revitFiles
        self.tbSourceFolder.Text = settings.inputDir
        self.tbDestinationFolder.Text = settings.outputDir
        self.tbFileType.Text = settings.revitFileExtension
        self.tbNoOfFiles.Text = str(settings.outputFileNum)
        self.cbInclSubDirs.IsChecked = settings.inclSubDirs
        
    def BtnOK(self, sender, EventArgs):
        # get selected items
        rows = self.files.SelectedItems
        if(rows != None and len(rows) > 0):
            self.selectedFiles = []
            for row in rows:
                # get the original file element
                for oRev in self.revitfiles:
                    if(oRev.name == row.name):
                        self.selectedFiles.append(oRev)
                        break
            # Mbox('ok',str(len(self.selectedFiles)), 1)
            self.DialogResult = True
            self.Close()
        else:
            Mbox('Attention','No files selected', 1)
    
    def BtnCancel(self, sender, EventArgs):
        #print('cancel')
        self.DialogResult = False
        self.Close()