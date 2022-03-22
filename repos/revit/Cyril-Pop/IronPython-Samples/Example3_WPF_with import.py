import sys
import clr
import wpf
clr.AddReference("System.Xml")
clr.AddReference("PresentationFramework")
clr.AddReference("PresentationCore")
import System
from System.IO import StringReader
from System.Xml import XmlReader
from System.Windows.Markup import XamlReader, XamlWriter
from System.Windows import Window, Application


class HelloWorld(Window):
	def __init__(self, xaml):
		self._xaml = xaml	
		xr = XmlReader.Create(StringReader(self._xaml))
		self.winLoad = wpf.LoadComponent(self, xr)
		#self._comboBox = self.winLoad.FindName('_comboBox') # not necessary with wpf IronPython Module Wpf
		for x in range(1,10):
			self._comboBox.Items.Add("Item "+str(x))
		
	def okButtonPressed(self, sender, e):
		System.Windows.MessageBox.Show("HelloWorld")
		
	def CnlButtonPressed(self, sender, e):
		System.Windows.MessageBox.Show("are you leaving us already?")	
		self.Close()	

	def pulldown_SelectionChanged(self, sender, e):
		System.Windows.MessageBox.Show("you have selected {}".format(sender.SelectedItem.ToString()))	

xaml = """
<Window 
       xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation" 
       xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml" 
       Title="PythonGUItest" Height="300" Width="300"> 
       <Grid>
        <Button x:Name="btnOkay" Content="OK" HorizontalAlignment="Left" Margin="127,239,0,0" VerticalAlignment="Top" Width="75" Click="okButtonPressed"/>
        <Button x:Name="btnCancel" Content="Cancel" HorizontalAlignment="Left" Margin="207,239,0,0" VerticalAlignment="Top" Width="75" Click="CnlButtonPressed"/>
        <ComboBox x:Name="_comboBox" HorizontalAlignment="Left" Margin="10,10,0,0" VerticalAlignment="Top" Width="120" SelectionChanged="pulldown_SelectionChanged"/>
    </Grid>
</Window> """

hello = HelloWorld(xaml)
hello.ShowDialog()
