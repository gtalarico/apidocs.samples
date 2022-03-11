
import sys
if 'win' in sys.platform:
 import pythoncom
 pythoncom.CoInitialize()

import clr
clr.AddReference("System.Xml")
clr.AddReference("PresentationFramework")
clr.AddReference("PresentationCore")
import System
from System.IO import StringReader
from System.Xml import XmlReader
from System.Windows.Markup import XamlReader, XamlWriter
from System.Windows import Window, Application


class HelloWorld():
	def __init__(self, xaml):
		self._xaml = xaml
		xr = XmlReader.Create(StringReader(xaml))
		self.winLoad = XamlReader.Load(xr)
		self._button = self.winLoad.FindName('button')
		self._stakpanel = self.winLoad.FindName('stackPanel')
		self._button.Click += self.onClick
		
	def onClick(self, sender, e):
		message = System.Windows.Controls.Label()
		message.FontSize = 16
		message.Content = 'Welcome to Dynamo'
		self._stakpanel.Children.Add(message)
		System.Windows.MessageBox.Show("HelloWorld")

xaml2 = """<Window xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation" xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"    
	Title="Welcome to IronPython" Width="450"    
	SizeToContent="Height">   
	<StackPanel Margin="15" x:Name="stackPanel">     
	<Button FontSize="24" x:Name="button">       
	<Button.BitmapEffect>         
	<DropShadowBitmapEffect />       
	</Button.BitmapEffect>       
	Push Me     
	</Button>   
	</StackPanel> 
	</Window>"""
xaml = """
<Window xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation" xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
	Title="Window3"
	Height="300"
	Width="300">
	<Grid>
		<Grid.Background>
			<LinearGradientBrush
				StartPoint="0.508727532464109,1"
				EndPoint="0.491272467535891,0">
				<LinearGradientBrush.GradientStops>
					<GradientStop
						Color="#FFF97777"
						Offset="0.0021186440677966119" />
					<GradientStop
						Color="#FFFFFFFF"
						Offset="0.9978813559322034" />
				</LinearGradientBrush.GradientStops>
			</LinearGradientBrush>
		</Grid.Background>
		<Button
			Content="Button"
			Grid.Column="0"
			Grid.Row="0"
			HorizontalAlignment="Left"
			VerticalAlignment="Top"
			Margin="101.6,42.4,0,0"
			Width="75.2"
			Height="23.2"
			x:Name="button" />
		<StackPanel
			Grid.Column="0"
			Grid.Row="0"
			HorizontalAlignment="Left"
			VerticalAlignment="Top"
			Margin="24.8,84.8,0,0"
			Width="234.4"
			Height="161.6"
			x:Name="stackPanel" />
	</Grid>
</Window>"""
try:
	hello = HelloWorld(xaml)
	print dir(hello)
	Application().Run(hello.winLoad)
	raw_input() #for debug in SharpDevelop	
	
except Exception as ex:
	print ex
	raw_input() #for debug in SharpDevelop	
