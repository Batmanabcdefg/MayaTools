"""
Copyright (c) 2008,2009 Mauricio Santos
Name: ms_spaceSwitch.py
Version: 1.0
Author: Mauricio Santos
Contact: mauricioptkvp@hotmail.com
Date Created: 27 Dec 2008
Last Modified: 22 Aug 2009
License: LGNU
Description:
    parentConstraint Control to given Objects, create switch attribute(s) on Control.

To do: 
    More than 8 targets?


"""

import maya.cmds as mc

class ms_spaceSwitch():
    """
     parentConstraint Control to given Objects, create switch attribute(s) on Control.
    """
    def __init__(self,*args):
        if(mc.window('spaceSwitchWin',exists=True)):
           mc.deleteUI('spaceSwitchWin',window=True)
           
        mc.window('spaceSwitchWin',title="Space Switch Setup v1.0",rtf=True)
        mc.columnLayout(adj=True)
        
        mc.text('                   Required:     ',fn='boldLabelFont')
        
        self.constField = mc.textFieldButtonGrp(label='Constrain Object:',bl='Load',bc=self.loadConst)
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
        mc.text('  Objects (Targets):',font='boldLabelFont',w=200)
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
        
        mc.showWindow('spaceSwitchWin')
        
    def createSwitch(self,*args):
        #Store values
        constObject = mc.textFieldButtonGrp(self.constField,query=True,text=True)
        control = mc.textFieldButtonGrp(self.cntField,query=True,text=True)
        attName = mc.textFieldGrp(self.attNameField,query=True,text=True)
        op1Name = mc.textFieldGrp(self.op1Field,query=True,text=True)
        op2Name = mc.textFieldGrp(self.op2Field,query=True,text=True)
        op3Name = mc.textFieldGrp(self.op3Field,query=True,text=True)
        op4Name = mc.textFieldGrp(self.op4Field,query=True,text=True)
        op5Name = mc.textFieldGrp(self.op5Field,query=True,text=True)
        op6Name = mc.textFieldGrp(self.op6Field,query=True,text=True)
        op7Name = mc.textFieldGrp(self.op7Field,query=True,text=True)
        op8Name = mc.textFieldGrp(self.op8Field,query=True,text=True)
        object1 = mc.textFieldButtonGrp(self.obj1Field,query=True,text=True)
        object2 = mc.textFieldButtonGrp(self.obj2Field,query=True,text=True)
        object3 = mc.textFieldButtonGrp(self.obj3Field,query=True,text=True)
        object4 = mc.textFieldButtonGrp(self.obj4Field,query=True,text=True)
        object5 = mc.textFieldButtonGrp(self.obj5Field,query=True,text=True)
        object6 = mc.textFieldButtonGrp(self.obj6Field,query=True,text=True)
        object7 = mc.textFieldButtonGrp(self.obj7Field,query=True,text=True)
        object8 = mc.textFieldButtonGrp(self.obj8Field,query=True,text=True)
        
        if ':' in op1Name:
            op1Name = op1Name.split(':')[-1]
        if ':' in op2Name:
            op2Name = op2Name.split(':')[-1]
        if ':' in op3Name:
            op3Name = op3Name.split(':')[-1]     
        if ':' in op4Name:
            op4Name = op4Name.split(':')[-1]
        if ':' in op5Name:
            op5Name = op5Name.split(':')[-1]
        if ':' in op6Name:
            op6Name = op6Name.split(':')[-1] 
        if ':' in op7Name:
            op7Name = op7Name.split(':')[-1]
        if ':' in op8Name:
            op8Name = op8Name.split(':')[-1]
        
        #create attribute on control
        mc.select(control,r=True)
        mc.addAttr(longName=attName,k=True)
        mc.setAttr(control + '.' + attName,lock=True)
        
        if len(object1) == 1:
            mc.addAttr(longName=op1Name,k=True,hasMinValue=True,hasMaxValue=True,minValue=0,maxValue=1.0)
        if len(object2) == 1:
            mc.addAttr(longName=op2Name,k=True,hasMinValue=True,hasMaxValue=True,minValue=0,maxValue=1.0)
        if len(object3) == 1:
            mc.addAttr(longName=op3Name,k=True,hasMinValue=True,hasMaxValue=True,minValue=0,maxValue=1.0)
        if len(object4) == 1:
            mc.addAttr(longName=op4Name,k=True,hasMinValue=True,hasMaxValue=True,minValue=0,maxValue=1.0)
        if len(object5) == 1:
            mc.addAttr(longName=op5Name,k=True,hasMinValue=True,hasMaxValue=True,minValue=0,maxValue=1.0)
        if len(object6) == 1:
            mc.addAttr(longName=op6Name,k=True,hasMinValue=True,hasMaxValue=True,minValue=0,maxValue=1.0)
        if len(object7) == 1:
            mc.addAttr(longName=op7Name,k=True,hasMinValue=True,hasMaxValue=True,minValue=0,maxValue=1.0)
        if len(object8) == 1:
            mc.addAttr(longName=op8Name,k=True,hasMinValue=True,hasMaxValue=True,minValue=0,maxValue=1.0)
        
        #Create parent constraint
        #Nested If's to run command only with objects entered by user
        if len(object2): #Not empty
            if len(object3):
                if len(object4):
                    if len(object5):
                        if len(object6):
                            if len(object7):
                                if len(object8):
                                    pConst = mc.parentConstraint( object1,object2,object3,object4,object5,object6,object7,object8,constObject,mo=True )
                                    #make attributes
                                    mc.addAttr(longName=op1Name,k=True,hasMinValue=True,hasMaxValue=True,minValue=0,maxValue=1.0)
                                    mc.addAttr(longName=op2Name,k=True,hasMinValue=True,hasMaxValue=True,minValue=0,maxValue=1.0)
                                    mc.addAttr(longName=op3Name,k=True,hasMinValue=True,hasMaxValue=True,minValue=0,maxValue=1.0)
                                    mc.addAttr(longName=op4Name,k=True,hasMinValue=True,hasMaxValue=True,minValue=0,maxValue=1.0)
                                    mc.addAttr(longName=op5Name,k=True,hasMinValue=True,hasMaxValue=True,minValue=0,maxValue=1.0)
                                    mc.addAttr(longName=op6Name,k=True,hasMinValue=True,hasMaxValue=True,minValue=0,maxValue=1.0)
                                    mc.addAttr(longName=op7Name,k=True,hasMinValue=True,hasMaxValue=True,minValue=0,maxValue=1.0)
                                    mc.addAttr(longName=op8Name,k=True,hasMinValue=True,hasMaxValue=True,minValue=0,maxValue=1.0)
                                    
                                    #make direct connections
                                    mc.connectAttr( control + '.' + op1Name, pConst[0] + '.' + str( object1.split(':')[-1]) + 'W0' )
                                    mc.connectAttr( control + '.' + op2Name, pConst[0] + '.' + str( object2.split(':')[-1]) + 'W1' )
                                    mc.connectAttr( control + '.' + op3Name, pConst[0] + '.' + str( object3.split(':')[-1]) + 'W2' )
                                    mc.connectAttr( control + '.' + op4Name, pConst[0] + '.' + str( object4.split(':')[-1]) + 'W3' )
                                    mc.connectAttr( control + '.' + op5Name, pConst[0] + '.' + str( object5.split(':')[-1]) + 'W4' )
                                    mc.connectAttr( control + '.' + op6Name, pConst[0] + '.' + str( object6.split(':')[-1]) + 'W5' )
                                    mc.connectAttr( control + '.' + op7Name, pConst[0] + '.' + str( object7.split(':')[-1]) + 'W6' )
                                    mc.connectAttr( control + '.' + op8Name, pConst[0] + '.' + str( object8.split(':')[-1]) + 'W7' )
                                else:#object8 was empty
                                    pConst = mc.parentConstraint( object1,object2,object3,object4,object5,object6,object7,constObject,mo=True )
                                    #make attributes
                                    mc.addAttr(longName=op1Name,k=True,hasMinValue=True,hasMaxValue=True,minValue=0,maxValue=1.0)
                                    mc.addAttr(longName=op2Name,k=True,hasMinValue=True,hasMaxValue=True,minValue=0,maxValue=1.0)
                                    mc.addAttr(longName=op3Name,k=True,hasMinValue=True,hasMaxValue=True,minValue=0,maxValue=1.0)
                                    mc.addAttr(longName=op4Name,k=True,hasMinValue=True,hasMaxValue=True,minValue=0,maxValue=1.0)
                                    mc.addAttr(longName=op5Name,k=True,hasMinValue=True,hasMaxValue=True,minValue=0,maxValue=1.0)
                                    mc.addAttr(longName=op6Name,k=True,hasMinValue=True,hasMaxValue=True,minValue=0,maxValue=1.0)
                                    mc.addAttr(longName=op7Name,k=True,hasMinValue=True,hasMaxValue=True,minValue=0,maxValue=1.0)
                                    
                                    #make direct connections
                                    mc.connectAttr( control + '.' + op1Name, pConst[0] + '.' + str( object1.split(':')[-1]) + 'W0' )
                                    mc.connectAttr( control + '.' + op2Name, pConst[0] + '.' + str( object2.split(':')[-1]) + 'W1' )
                                    mc.connectAttr( control + '.' + op3Name, pConst[0] + '.' + str( object3.split(':')[-1]) + 'W2' )
                                    mc.connectAttr( control + '.' + op4Name, pConst[0] + '.' + str( object4.split(':')[-1]) + 'W3' )
                                    mc.connectAttr( control + '.' + op5Name, pConst[0] + '.' + str( object5.split(':')[-1]) + 'W4' )
                                    mc.connectAttr( control + '.' + op6Name, pConst[0] + '.' + str( object6.split(':')[-1]) + 'W5' )
                                    mc.connectAttr( control + '.' + op7Name, pConst[0] + '.' + str( object7.split(':')[-1]) + 'W6' )
                            
                            else:#object7 was empty
                                pConst = mc.parentConstraint( object1,object2,object3,object4,object5,object6,constObject,mo=True )
                                #make attributes
                                mc.addAttr(longName=op1Name,k=True,hasMinValue=True,hasMaxValue=True,minValue=0,maxValue=1.0)
                                mc.addAttr(longName=op2Name,k=True,hasMinValue=True,hasMaxValue=True,minValue=0,maxValue=1.0)
                                mc.addAttr(longName=op3Name,k=True,hasMinValue=True,hasMaxValue=True,minValue=0,maxValue=1.0)
                                mc.addAttr(longName=op4Name,k=True,hasMinValue=True,hasMaxValue=True,minValue=0,maxValue=1.0)
                                mc.addAttr(longName=op5Name,k=True,hasMinValue=True,hasMaxValue=True,minValue=0,maxValue=1.0)
                                mc.addAttr(longName=op6Name,k=True,hasMinValue=True,hasMaxValue=True,minValue=0,maxValue=1.0)
                                
                                #make direct connections
                                mc.connectAttr( control + '.' + op1Name, pConst[0] + '.' + str( object1.split(':')[-1]) + 'W0' )
                                mc.connectAttr( control + '.' + op2Name, pConst[0] + '.' + str( object2.split(':')[-1]) + 'W1' )
                                mc.connectAttr( control + '.' + op3Name, pConst[0] + '.' + str( object3.split(':')[-1]) + 'W2' )
                                mc.connectAttr( control + '.' + op4Name, pConst[0] + '.' + str( object4.split(':')[-1]) + 'W3' )
                                mc.connectAttr( control + '.' + op5Name, pConst[0] + '.' + str( object5.split(':')[-1]) + 'W4' )
                                mc.connectAttr( control + '.' + op6Name, pConst[0] + '.' + str( object6.split(':')[-1]) + 'W5' )
                        
                        else:#object6 was empty
                            pConst = mc.parentConstraint( object1,object2,object3,object4,object5,constObject,mo=True )
                            #make attributes
                            mc.addAttr(longName=op1Name,k=True,hasMinValue=True,hasMaxValue=True,minValue=0,maxValue=1.0)
                            mc.addAttr(longName=op2Name,k=True,hasMinValue=True,hasMaxValue=True,minValue=0,maxValue=1.0)
                            mc.addAttr(longName=op3Name,k=True,hasMinValue=True,hasMaxValue=True,minValue=0,maxValue=1.0)
                            mc.addAttr(longName=op4Name,k=True,hasMinValue=True,hasMaxValue=True,minValue=0,maxValue=1.0)
                            mc.addAttr(longName=op5Name,k=True,hasMinValue=True,hasMaxValue=True,minValue=0,maxValue=1.0)
                            
                            #make direct connections
                            mc.connectAttr( control + '.' + op1Name, pConst[0] + '.' + str( object1.split(':')[-1]) + 'W0' )
                            mc.connectAttr( control + '.' + op2Name, pConst[0] + '.' + str( object2.split(':')[-1]) + 'W1' )
                            mc.connectAttr( control + '.' + op3Name, pConst[0] + '.' + str( object3.split(':')[-1]) + 'W2' )
                            mc.connectAttr( control + '.' + op4Name, pConst[0] + '.' + str( object4.split(':')[-1]) + 'W3' )
                            mc.connectAttr( control + '.' + op5Name, pConst[0] + '.' + str( object5.split(':')[-1]) + 'W4' )
                
                    else:#object5 was empty
                        pConst = mc.parentConstraint( object1,object2,object3,object4,constObject,mo=True )
                        #make attributes
                        mc.addAttr(longName=op1Name,k=True,hasMinValue=True,hasMaxValue=True,minValue=0,maxValue=1.0)
                        mc.addAttr(longName=op2Name,k=True,hasMinValue=True,hasMaxValue=True,minValue=0,maxValue=1.0)
                        mc.addAttr(longName=op3Name,k=True,hasMinValue=True,hasMaxValue=True,minValue=0,maxValue=1.0)
                        mc.addAttr(longName=op4Name,k=True,hasMinValue=True,hasMaxValue=True,minValue=0,maxValue=1.0)
                        
                        #make direct connections
                        mc.connectAttr( control + '.' + op1Name, pConst[0] + '.' + str( object1.split(':')[-1]) + 'W0' )
                        mc.connectAttr( control + '.' + op2Name, pConst[0] + '.' + str( object2.split(':')[-1]) + 'W1' )
                        mc.connectAttr( control + '.' + op3Name, pConst[0] + '.' + str( object3.split(':')[-1]) + 'W2' )
                        mc.connectAttr( control + '.' + op4Name, pConst[0] + '.' + str( object4.split(':')[-1]) + 'W3' )
                else:#object4 was empty
                    
                    pConst = mc.parentConstraint( str( object1),str( object2),str( object3),constObject,mo=True )
                    #make attributes
                    mc.addAttr(longName=op1Name,k=True,hasMinValue=True,hasMaxValue=True,minValue=0,maxValue=1.0)
                    mc.addAttr(longName=op2Name,k=True,hasMinValue=True,hasMaxValue=True,minValue=0,maxValue=1.0)
                    mc.addAttr(longName=op3Name,k=True,hasMinValue=True,hasMaxValue=True,minValue=0,maxValue=1.0)
                    #make direct connections
                    mc.connectAttr( control + '.' + op1Name, pConst[0] + '.' + str( object1.split(':')[-1]) + 'W0' )
                    mc.connectAttr( control + '.' + op2Name, pConst[0] + '.' + str( object2.split(':')[-1]) + 'W1' )
                    mc.connectAttr( control + '.' + op3Name, pConst[0] + '.' + str( object3.split(':')[-1]) + 'W2' )
            else:# object 3 was empty
                
                pConst = mc.parentConstraint( str( object1),str( object2),constObject,mo=True )
                #make attributes
                mc.addAttr(longName=op1Name,k=True,hasMinValue=True,hasMaxValue=True,minValue=0,maxValue=1.0)
                mc.addAttr(longName=op2Name,k=True,hasMinValue=True,hasMaxValue=True,minValue=0,maxValue=1.0)
                #make direct connections
                mc.connectAttr( control + '.' + op1Name, pConst[0] + '.' + str( object1.split(':')[-1]) + 'W0' )
                mc.connectAttr( control + '.' + op2Name, pConst[0] + '.' + str( object2.split(':')[-1]) + 'W1' )
                
        else: #object2 was empty
            pConst = mc.parentConstraint( str( object1),constObject,mo=True )
            #make attributes
            mc.addAttr(longName=op1Name,k=True,hasMinValue=True,hasMaxValue=True,minValue=0,maxValue=1.0)
            #make direct connections
            mc.connectAttr( control + '.' + op1Name, pConst[0] + '.' + str( object1.split(':')[-1]) + 'W0' )
            
       
        
        
    def loadConst(self,*args):
        sel = mc.ls(sl=True,fl=True)
        mc.textFieldButtonGrp(self.constField,edit=True,text=sel[0])    
        
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
        
