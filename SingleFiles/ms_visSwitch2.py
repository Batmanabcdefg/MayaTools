"""
Copyright (c) 2008,2009,2010,2011 Mauricio Santos
Name: ms_visSwitch2.py
Version: 2.0
Author: Mauricio Santos
Contact: mauricioptkvp@hotmail.com
Date Created: 17 Dec 2010
Last Modified: 18 Dec 2011
License: LGNU
Description:
    Connect visibility attributes of selected source objects to a specific attribute on the target object. 
    (The controller curve with the attribute:"world_cnt.l_arm_cnts"

To do: 
    More than 8 targets?

Notes: 
    Seems to create an extra blank attribute at end and crash, but it still makes the attrs and connects them.

"""

import maya.cmds as mc
import pdb

class ms_visSwitch2():
    """
     Create vis switch menu attribute on controller, then one each for switching the objects selected as individual 0-1 int fields
    """
    def __init__(self,*args):
        if(mc.window('visSwitch2Win',exists=True)):
           mc.deleteUI('visSwitch2Win',window=True)
           
        mc.window('visSwitch2Win',title="Visibility Switch Setup v2.1",rtf=True)
        mc.columnLayout()
        
        mc.text('                   Required:     ',fn='boldLabelFont')
        
        #self.constField = mc.textFieldButtonGrp(label='Constrain Objects:',bl='Load',bc=self.loadConst)
        self.cntField = mc.textFieldButtonGrp(label='Put Attributes on:',bl='Load',bc=self.loadCnt)
        self.attNameField = mc.textFieldGrp(label='Main Attribute Label:',text='space')
        mc.separator(w=400)
        mc.text('                   Note: Empty fields ignored      ',fn='boldLabelFont')
        mc.text('Attribute labels:',font='boldLabelFont',w=200)
        self.op1Field = mc.textFieldGrp(label='1:')
        self.op2Field = mc.textFieldGrp(label='2:')
        self.op3Field = mc.textFieldGrp(label='3:')
        self.op4Field = mc.textFieldGrp(label='4:')
        self.op5Field = mc.textFieldGrp(label='5:')
        self.op6Field = mc.textFieldGrp(label='6:')
        self.op7Field = mc.textFieldGrp(label='7:')
        self.op8Field = mc.textFieldGrp(label='8:')
        mc.text('  Objects (Vis on/off):',font='boldLabelFont',w=200)
        self.obj1Field = mc.textFieldButtonGrp(label='Object 1:',bl='Load',bc=self.loadObj1)
        self.obj2Field = mc.textFieldButtonGrp(label='Object 2:',bl='Load',bc=self.loadObj2)
        self.obj3Field = mc.textFieldButtonGrp(label='Object 3:',bl='Load',bc=self.loadObj3)
        self.obj4Field = mc.textFieldButtonGrp(label='Object 4:',bl='Load',bc=self.loadObj4)
        self.obj5Field = mc.textFieldButtonGrp(label='Object 5:',bl='Load',bc=self.loadObj5)
        self.obj6Field = mc.textFieldButtonGrp(label='Object 6:',bl='Load',bc=self.loadObj6)
        self.obj7Field = mc.textFieldButtonGrp(label='Object 7:',bl='Load',bc=self.loadObj7)
        self.obj8Field = mc.textFieldButtonGrp(label='Object 8:',bl='Load',bc=self.loadObj8)
        
        mc.rowLayout(nc=2,cw2=(200,100))
        mc.text(" ")
        mc.button(label="     Create",c=self.createSwitch,w=80)
        
        mc.showWindow('visSwitch2Win')
        
    def createSwitch(self,*args):
        #Store values
        #constObject = mc.textFieldButtonGrp(self.constField,query=True,text=True)
        control = mc.textFieldButtonGrp(self.cntField,query=True,text=True)
        attName = mc.textFieldGrp(self.attNameField,query=True,text=True)
        
        attrNames = []
        attrNames.append( mc.textFieldGrp(self.op1Field,query=True,text=True) )
        attrNames.append( mc.textFieldGrp(self.op2Field,query=True,text=True) )
        attrNames.append( mc.textFieldGrp(self.op3Field,query=True,text=True) )
        attrNames.append( mc.textFieldGrp(self.op4Field,query=True,text=True) )
        attrNames.append( mc.textFieldGrp(self.op5Field,query=True,text=True) )
        attrNames.append( mc.textFieldGrp(self.op6Field,query=True,text=True) )
        attrNames.append( mc.textFieldGrp(self.op7Field,query=True,text=True) )
        attrNames.append( mc.textFieldGrp(self.op8Field,query=True,text=True) )
        
        objectNames = []
        objectNames.append( mc.textFieldButtonGrp(self.obj1Field,query=True,text=True) )
        objectNames.append( mc.textFieldButtonGrp(self.obj2Field,query=True,text=True) )
        objectNames.append( mc.textFieldButtonGrp(self.obj3Field,query=True,text=True) )
        objectNames.append( mc.textFieldButtonGrp(self.obj4Field,query=True,text=True) )
        objectNames.append( mc.textFieldButtonGrp(self.obj5Field,query=True,text=True) )
        objectNames.append( mc.textFieldButtonGrp(self.obj6Field,query=True,text=True) )
        objectNames.append( mc.textFieldButtonGrp(self.obj7Field,query=True,text=True) )
        objectNames.append( mc.textFieldButtonGrp(self.obj8Field,query=True,text=True) )
        
        #Create title attribute on control.
        mc.addAttr(control,longName=attName,k=True)
        mc.setAttr(control + '.' + attName,lock=True)
        
        # Create switch attributes on controller and connect them to objects vis attributes.
        #pdb.set_trace()
        count = 0
        for attr in attrNames:
            mc.addAttr( control, longName=attr,k=True,hasMinValue=True,hasMaxValue=True,minValue=0,maxValue=1.0 )
            mc.connectAttr( control+'.'+attr, objectNames[count]+'.visibility', f=True )     
            count += 1
 
    def loadCnt(self,*args):
        sel = mc.ls(sl=True,fl=True)
        mc.textFieldButtonGrp(self.cntField,edit=True,text=sel[0])
        
    def loadObj1(self,*args):
        sel = mc.ls(sl=True,fl=True)
        mc.textFieldButtonGrp(self.obj1Field,edit=True,text=sel[0])
    
    def loadObj2(self,*args):
        sel = mc.ls(sl=True,fl=True)
        mc.textFieldButtonGrp(self.obj2Field,edit=True,text=sel[0])
        
    def loadObj3(self,*args):
        sel = mc.ls(sl=True,fl=True)
        mc.textFieldButtonGrp(self.obj3Field,edit=True,text=sel[0])
        
    def loadObj4(self,*args):
        sel = mc.ls(sl=True,fl=True)
        mc.textFieldButtonGrp(self.obj4Field,edit=True,text=sel[0])

    def loadObj5(self,*args):
        sel = mc.ls(sl=True,fl=True)
        mc.textFieldButtonGrp(self.obj5Field,edit=True,text=sel[0])

    def loadObj6(self,*args):
        sel = mc.ls(sl=True,fl=True)
        mc.textFieldButtonGrp(self.obj6Field,edit=True,text=sel[0])

    def loadObj7(self,*args):
        sel = mc.ls(sl=True,fl=True)
        mc.textFieldButtonGrp(self.obj7Field,edit=True,text=sel[0])
        
    def loadObj8(self,*args):
        sel = mc.ls(sl=True,fl=True)
        mc.textFieldButtonGrp(self.obj8Field,edit=True,text=sel[0])
        
