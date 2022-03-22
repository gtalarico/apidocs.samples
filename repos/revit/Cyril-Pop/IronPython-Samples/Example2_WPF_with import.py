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
		#self._stakpanel = self.winLoad.FindName('stackPanel') # not necessary with IronPython Wpf module
		
		## Other Way
		#self._button.Click += self.onClick
		
	def onClick(self, sender, e):

		message = System.Windows.Controls.Label()
		message.FontSize = 16
		message.Content = 'Welcome to Dynamo'
		self._stakpanel.Children.Add(message)
		System.Windows.MessageBox.Show("HelloWorld")

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
			x:Name="_button"
			Click="onClick" />
		<StackPanel
			Grid.Column="0"
			Grid.Row="0"
			HorizontalAlignment="Left"
			VerticalAlignment="Top"
			Margin="24.8,84.8,0,0"
			Width="234.4"
			Height="161.6"
			x:Name="_stakpanel" />
	</Grid>
</Window>"""

hello = HelloWorld(xaml)
hello.ShowDialog()


