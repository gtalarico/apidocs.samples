# coding : utf-8
# Copyright POUPIN.C
import clr
import re
clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *

clr.AddReference('RevitAPI')
import Autodesk
from Autodesk.Revit.DB import *

clr.AddReference('RevitAPIUI')
from Autodesk.Revit.UI import *

clr.AddReference('RevitServices')
import RevitServices
from RevitServices.Persistence import DocumentManager
doc = DocumentManager.Instance.CurrentDBDocument
uiapp =  DocumentManager.Instance.CurrentUIApplication


clr.AddReference('System.Drawing')
clr.AddReference('System.Windows.Forms')
import System.Drawing
import System.Windows.Forms

from System.Drawing import *
from System.Windows.Forms import *
import System
from System.Collections.Generic import List

class ParaProj():
    def __init__(self, definition, binding):
        self.defName = definition.Name
        self.binding = binding	
        self.thesecats = []
        self.group = LabelUtils.GetLabelFor(definition.ParameterGroup)
        for cat in binding.Categories:
            try:
                self.thesecats.append(cat.Name)
            except SystemError:
                pass    		

class MainForm(Form):
    def __init__(self, lstObj_bind):
        self.lstObj_bind = lstObj_bind #lst object
        collSharP = FilteredElementCollector(doc).OfClass(SharedParameterElement)
        self._paraSharPara = [x.GetDefinition().Name for x in collSharP]
        self.InitializeComponent()
    
    def InitializeComponent(self):
        self._treeView1 = System.Windows.Forms.TreeView()
        self._buttonEdit = System.Windows.Forms.Button()
        self._buttonCancel = System.Windows.Forms.Button()
        self.SuspendLayout()   
        # 
        # buttonEdit
        self._buttonEdit.DialogResult = System.Windows.Forms.DialogResult.OK
        self._buttonEdit.Location = System.Drawing.Point(350, 500)
        self._buttonEdit.Name = "buttonEdit"
        self._buttonEdit.Size = System.Drawing.Size(150, 45)
        self._buttonEdit.TabIndex = 0
        self._buttonEdit.Text = "Editer Paramètres de Projet"
        self._buttonEdit.UseVisualStyleBackColor = True
        self._buttonEdit.Click += self.ButtonEditClick
        #
        # buttonCancel
        self._buttonCancel.DialogResult = System.Windows.Forms.DialogResult.Cancel
        self._buttonCancel.Location = System.Drawing.Point(50, 500)
        self._buttonCancel.Name = "buttonCancel"
        self._buttonCancel.Size = System.Drawing.Size(142, 45)
        self._buttonCancel.TabIndex = 0
        self._buttonCancel.Text = "Quitter"
        self._buttonCancel.UseVisualStyleBackColor = True
        self._buttonCancel.Click += self.ButtonCancelClick
        # 
        # textBox1
        self._textBox1 = System.Windows.Forms.TextBox()
        self._textBox1.Location = System.Drawing.Point(50, 46)
        self._textBox1.Name = "SearchBox"
        self._textBox1.Size = System.Drawing.Size(213, 22)
        self._textBox1.TabIndex = 0
        self._textBox1.TextChanged += self.TextBox1TextChanged
        # 
        # Label
        self._label1 = System.Windows.Forms.Label()
        self._label1.Location = System.Drawing.Point(50, 20)
        self._label1.Name = "Search"
        self._label1.Size = System.Drawing.Size(150, 23)
        self._label1.TabIndex = 1
        self._label1.Text = "Recherche (Regex)"        
        # 
        # treeView1
        self._treeView1.Location = System.Drawing.Point(50, 75)
        self._treeView1.Name = "treeView1"     
        dataBind = self.lstObj_bind 
        #create TreeNode        
        self.setDataTreeNode(dataBind)
        self._treeView1.Size = System.Drawing.Size(450, 400)
        self._treeView1.TabIndex = 0
        # 
        # Form1
        self.ClientSize = System.Drawing.Size(540, 580)
        self.Controls.Add(self._treeView1)
        self.Controls.Add(self._label1)
        self.Controls.Add(self._textBox1)
        self.Controls.Add(self._buttonCancel)
        self.Controls.Add(self._buttonEdit)
        self.Name = "Projet Parameters"
        self.Text = "Liste des Parametres de Projet"
        self.ResumeLayout(False)
        
    def setDataTreeNode(self, dataBind):
        self.lsttreenode = List[System.Object]()
        for objbind in dataBind:
            paraproj = objbind.defName
            if paraproj in self._paraSharPara:
                isShared = "Partagé"
            else:
                isShared = "Non Partagé"
            #
            if isinstance(objbind.binding, InstanceBinding):
                bindtype = "Occurrence"
            else:
                bindtype = "Type"
            filtercats = objbind.thesecats
            sublist = List[System.Object]()
            #create data TreeNode
            for cat in filtercats:
                treeNodeChildCat = System.Windows.Forms.TreeNode(cat)
                treeNodeChildCat.Name = cat
                treeNodeChildCat.Text = cat
                sublist.Add(treeNodeChildCat)
            treeNodeParentCat = System.Windows.Forms.TreeNode("Catégories", System.Array[System.Windows.Forms.TreeNode](sublist))
            treeNodeParentCat.Name = "Catégories"
            treeNodeParentCat.Text = "Catégories"
            treeNodeTypePara = System.Windows.Forms.TreeNode("Propriété")
            treeNodeTypePara.Name = "Propriété"
            treeNodeTypePara.Text = "Propriété du Paramètre : " + bindtype 
            treeNodeShared = System.Windows.Forms.TreeNode("Type")
            treeNodeShared.Name = "Type"
            treeNodeShared.Text = "Type de Paramètre : " + isShared    
            treeNodeGroup = System.Windows.Forms.TreeNode("Groupe")
            treeNodeGroup.Name = "Groupe"
            treeNodeGroup.Text = "Groupe : " + objbind.group            
            treeNodeParentPara = System.Windows.Forms.TreeNode(paraproj, System.Array[System.Windows.Forms.TreeNode]([treeNodeTypePara, treeNodeShared, treeNodeGroup, treeNodeParentCat]))
            treeNodeParentPara.Name = paraproj
            treeNodeParentPara.Text = paraproj         
            
            if isinstance(objbind.binding, InstanceBinding): 
                #"Paramètre d'Occurrence"   
                treeNodeParentPara.ForeColor = System.Drawing.Color.Blue
            else:
                #"Paramètre de Type"
                treeNodeParentPara.ForeColor = System.Drawing.Color.Red            
            self.lsttreenode.Add(treeNodeParentPara)
        self._treeView1.Nodes.AddRange(System.Array[System.Windows.Forms.TreeNode](self.lsttreenode))
                    
    def TextBox1TextChanged(self, sender, e):
        try:
            dataBindFilter =  [x for x in self.lstObj_bind if re.search(sender.Text, x.defName) is not None]
            self._treeView1.BeginUpdate()
            self._treeView1.Nodes.Clear()
            self.setDataTreeNode(dataBindFilter)
            self._treeView1.EndUpdate()
        except:pass #if regex failed (typing not finish )
        
    def ButtonCancelClick(self, sender, e):
        self.Close()

    def ButtonEditClick(self, sender, e): 
        id_addin = RevitCommandId.LookupPostableCommandId(PostableCommand.ProjectParameters)
        uiapp.PostCommand(id_addin)  
        self.Close()
   
full_bind = []
iterator =  doc.ParameterBindings.ForwardIterator()
while iterator.MoveNext():
    objBind = ParaProj(iterator.Key, iterator.Current)
    full_bind.append(objBind)
	
full_bind.sort(key = lambda x : x.defName) 
objform = MainForm(full_bind)   
result = objform.ShowDialog()    

OUT = full_bind, result

