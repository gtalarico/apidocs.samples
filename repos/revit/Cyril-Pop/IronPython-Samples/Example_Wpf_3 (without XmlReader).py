import clr	
import sys
sys.path.append(r'C:\Program Files (x86)\IronPython 2.7\Lib')
sys.path.append(r'C:\Program Files (x86)\IronPython 2.7\DLLs')

try:
	clr.AddReference("IronPython.Wpf")
	clr.AddReference('System.Core')
	clr.AddReference('System.Xml')
	clr.AddReference('PresentationCore')
	clr.AddReference('PresentationFramework')
except IOError:
	raise
	
from System.IO import StringReader
from System.Windows.Markup import XamlReader, XamlWriter
from System.Windows import Window, Application


try:
	import wpf
except ImportError:
	raise
	
class DropdownInput(Window):

	LAYOUT = """
			<Window
				xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
				xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
				xmlns:d="http://schemas.microsoft.com/expression/blend/2008"
				xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006"
				xmlns:local="clr-namespace:WpfApplication1"
				mc:Ignorable="d" 
				Height="140.139" 
				Width="325" 
				ResizeMode="NoResize"
				Title="" 
				WindowStartupLocation="CenterScreen" 
				Topmost="True" 
				SizeToContent="WidthAndHeight">
				<Grid Margin="10,0,10,10">
					<Label x:Name="selection_label" Content="Select Item" HorizontalAlignment="Left" Height="30"
						VerticalAlignment="Top" Width="299"/>
					<ComboBox x:Name="combo_data" HorizontalAlignment="Left" Margin="0,30,0,0"
						VerticalAlignment="Top" Width="299"/>
					<Button x:Name="button_select" Content="Select" HorizontalAlignment="Left" Height="26"
					Margin="0,63,0,0" VerticalAlignment="Top" Width="299"/>
				</Grid>
			</Window>"""
				
	def __init__(self, title, options, description=None):
		self.selected = None
		self.ui = wpf.LoadComponent(self, StringReader(DropdownInput.LAYOUT))
		self.ui.Title = title
	
		if description is not None:
			self.ui.selection_label.Content = description
		self.ui.button_select.Click += self.select_click
	
		self.ui.combo_data.Items.Clear()
		self.ui.combo_data.ItemsSource = options
		self.ui.combo_data.SelectedItem = options[0]
	
	def select_click(self, sender, e):
		self.selected = self.ui.combo_data.SelectedItem
		self.DialogResult = True
		self.Close()
	
	
	
	
run = IN[0]
keys = IN[1]
values = IN[2]
description = IN[3]

if values:
	if len(values) != len(keys):
		raise Exception('Length of Values and Keys must match')
	dropdown_options = {k:v for k, v in zip(keys, values)}
else:
	dropdown_options = {k:k for k in keys}
	
if run:
	form = DropdownInput('Dynamo Form Input', dropdown_options.keys(), description=description)
	form.ShowDialog()
	if form.selected is not None:
		OUT = dropdown_options[form.selected]
else:
	OUT = 'Set RUN to True'
