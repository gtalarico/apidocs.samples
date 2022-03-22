import System.Drawing
import System.Windows.Forms

from System.Drawing import *
from System.Windows.Forms import *

class MainForm(Form):
	def __init__(self):
		self.InitializeComponent()
	
	def InitializeComponent(self):
		self._richTextBox1 = System.Windows.Forms.RichTextBox()
		self._OKbutton = System.Windows.Forms.Button()
		self._labelCP = System.Windows.Forms.Label()
		self._label2 = System.Windows.Forms.Label()
		self.SuspendLayout()
		# 
		# richTextBox1
		# 
		self._richTextBox1.Location = System.Drawing.Point(24, 54)
		self._richTextBox1.Name = "richTextBox1"
		self._richTextBox1.Size = System.Drawing.Size(305, 198)
		self._richTextBox1.TabIndex = 0
		self._richTextBox1.Text = """ggjgjkgk
uguootott"""
		self._richTextBox1.TextChanged += self.RichTextBox1TextChanged
		# 
		# OKbutton
		# 
		self._OKbutton.Location = System.Drawing.Point(219, 274)
		self._OKbutton.Name = "OKbutton"
		self._OKbutton.Size = System.Drawing.Size(110, 40)
		self._OKbutton.TabIndex = 1
		self._OKbutton.Text = "OK/Continuer"
		self._OKbutton.UseVisualStyleBackColor = True
		self._OKbutton.Click += self.Button1Click
		# 
		# labelCP
		# 
		self._labelCP.BorderStyle = System.Windows.Forms.BorderStyle.Fixed3D
		self._labelCP.Location = System.Drawing.Point(37, 285)
		self._labelCP.Name = "labelCP"
		self._labelCP.Size = System.Drawing.Size(126, 23)
		self._labelCP.TabIndex = 2
		self._labelCP.Text = "Written by Cyril.P"
		# 
		# label2
		# 
		self._label2.Location = System.Drawing.Point(24, 19)
		self._label2.Name = "label2"
		self._label2.Size = System.Drawing.Size(305, 32)
		self._label2.TabIndex = 2
		self._label2.Text = "Entrer les Noms des Sous Projet (1 par ligne)"
		# 
		# MainForm
		# 
		self.ClientSize = System.Drawing.Size(365, 326)
		self.Controls.Add(self._label2)
		self.Controls.Add(self._labelCP)
		self.Controls.Add(self._OKbutton)
		self.Controls.Add(self._richTextBox1)
		self.Name = "MainForm"
		self.Text = "UI_SetWorket"
		self.ResumeLayout(False)


	def Button1Click(self, sender, e):
		pass

	def RichTextBox1TextChanged(self, sender, e):
		pass
