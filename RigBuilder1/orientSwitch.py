from __future__ import with_statement # This line is only needed for 2008 and 2009
from pymel.core import *
"""
Copyright (c) 2010 Mauricio Santos
Name: orientSwitch.py
Version: 1.0
Author: Mauricio Santos
Contact: mauricioptkvp@hotmail.com
Date Created: 22 Dec 2010
Last Modified: 22 Dec 2010

$Revision: 132 $
$LastChangedDate: 2011-08-06 19:27:15 -0700 (Sat, 06 Aug 2011) $
$Author: mauricio $
$HeadURL: file:///Users/mauricio/SVN_Repos/Maya_Tools/trunk/Tools/Rigging/Dev/RigBuilder/orientSwitch.py $
$Id: orientSwitch.py 132 2011-08-07 02:27:15Z mauricio $

Description:
    orientConstraint Control to given Objects, create switch attribute(s) on Control.

To do: 
    More than 8 targets?


"""

class orientSwitch():
    """
     orientConstraint Control to given Objects, create switch attribute(s) on Control.
    """
    def __init__(self,**keywords):
        # Check if command line call
        self.createdNodes = {}
        
        if len(keywords):
            self.commandlineCall(keywords)
        else:
            self.buildGUI()
            
    def commandlineCall(self,keywords):
        """
        Verify and Store the data passed via command line keywords dictionary.
        """                    
        # Initialize variables based on user input
        self.constObject = keywords['constObj']
        self.control = keywords['control']
        self.attName = keywords['attName']
        self.op1Name = keywords['op1Name']
        self.op2Name = keywords['op2Name']
        self.op3Name = keywords['op3Name']
        self.op4Name = keywords['op4Name']
        self.op5Name = keywords['op5Name']
        self.op6Name = keywords['op6Name']
        self.op7Name = keywords['op7Name']
        self.op8Name = keywords['op8Name']
        self.object1 = keywords['object1']
        self.object2 = keywords['object2']
        self.object3 = keywords['object3']
        self.object4 = keywords['object4']
        self.object5 = keywords['object5']
        self.object6 = keywords['object6']
        self.object7 = keywords['object7']
        self.object8 = keywords['object8']
        
        self.createSwitch()
        
    def buildGUI(self,*args):
        """
        Create GUI in Maya
        """
        if(window('orientSwitchWin',exists=True)):
           deleteUI('orientSwitchWin',window=True)
           
        with window('orientSwitchWin',title="Orient Switch Setup v1.0",rtf=True) as mainWin:
            with columnLayout():
                text('                   Required:     ',fn='boldLabelFont')
                
                self.constField = textFieldButtonGrp(label='Constrain Object:',bl='Load',bc=self.loadConst)
                self.cntField = textFieldButtonGrp(label='Put Attributes on:',bl='Load',bc=self.loadCnt)
                self.attNameField = textFieldGrp(label='Main Attribute Label:',text='space')
                separator(w=400)
                text('                   Note: Empty fields ignored      ',fn='boldLabelFont')
                text('Attribute labels:',font='boldLabelFont',w=200)
                self.op1Field = textFieldGrp(label='1:')
                self.op2Field = textFieldGrp(label='2:')
                self.op3Field = textFieldGrp(label='3:')
                self.op4Field = textFieldGrp(label='4:')
                self.op5Field = textFieldGrp(label='5:')
                self.op6Field = textFieldGrp(label='6:')
                self.op7Field = textFieldGrp(label='7:')
                self.op8Field = textFieldGrp(label='8:')
                text('  Objects (Targets):',font='boldLabelFont',w=200)
                self.obj1Field = textFieldButtonGrp(label='Object 1:',bl='Load',bc=self.loadObj1)
                self.obj2Field = textFieldButtonGrp(label='Object 2:',bl='Load',bc=self.loadObj2)
                self.obj3Field = textFieldButtonGrp(label='Object 3:',bl='Load',bc=self.loadObj3)
                self.obj4Field = textFieldButtonGrp(label='Object 4:',bl='Load',bc=self.loadObj4)
                self.obj5Field = textFieldButtonGrp(label='Object 5:',bl='Load',bc=self.loadObj5)
                self.obj6Field = textFieldButtonGrp(label='Object 6:',bl='Load',bc=self.loadObj6)
                self.obj7Field = textFieldButtonGrp(label='Object 7:',bl='Load',bc=self.loadObj7)
                self.obj8Field = textFieldButtonGrp(label='Object 8:',bl='Load',bc=self.loadObj8)
                
                with rowLayout(nc=2,cw2=(200,100)):
                    text(" ")
                    button(label="     Create",c=self.guiCall,w=80)
                
                mainWin.show()
            
    def guiCall(self,*args):
        """
        Verify and Store the data passed via GUI.
        """
        self.constObject = textFieldButtonGrp(self.constField,query=True,text=True)
        self.control = textFieldButtonGrp(self.cntField,query=True,text=True)
        self.attName = textFieldGrp(self.attNameField,query=True,text=True)
        self.op1Name = textFieldGrp(self.op1Field,query=True,text=True)
        self.op2Name = textFieldGrp(self.op2Field,query=True,text=True)
        self.op3Name = textFieldGrp(self.op3Field,query=True,text=True)
        self.op4Name = textFieldGrp(self.op4Field,query=True,text=True)
        self.op5Name = textFieldGrp(self.op5Field,query=True,text=True)
        self.op6Name = textFieldGrp(self.op6Field,query=True,text=True)
        self.op7Name = textFieldGrp(self.op7Field,query=True,text=True)
        self.op8Name = textFieldGrp(self.op8Field,query=True,text=True)
        self.object1 = textFieldButtonGrp(self.obj1Field,query=True,text=True)
        self.object2 = textFieldButtonGrp(self.obj2Field,query=True,text=True)
        self.object3 = textFieldButtonGrp(self.obj3Field,query=True,text=True)
        self.object4 = textFieldButtonGrp(self.obj4Field,query=True,text=True)
        self.object5 = textFieldButtonGrp(self.obj5Field,query=True,text=True)
        self.object6 = textFieldButtonGrp(self.obj6Field,query=True,text=True)
        self.object7 = textFieldButtonGrp(self.obj7Field,query=True,text=True)
        self.object8 = textFieldButtonGrp(self.obj8Field,query=True,text=True)
        
        self.createSwitch()
        
    def createSwitch(self,*args):
        #Store values
        constObject = self.constObject
        control = self.control
        attName = self.attName
        op1Name = self.op1Name
        op2Name = self.op2Name
        op3Name = self.op3Name
        op4Name = self.op4Name
        op5Name = self.op5Name
        op6Name = self.op6Name
        op7Name = self.op7Name
        op8Name = self.op8Name
        object1 = str(self.object1)
        object2 = self.object2
        object3 = self.object3
        object4 = self.object4
        object5 = self.object5
        object6 = self.object6
        object7 = self.object7
        object8 = self.object8
        
        #create attribute on control
        select(control,r=True)
        addAttr(longName=attName,k=True)
        setAttr(control + '.' + attName,lock=True)
        
        if len(object1) == 1:
            addAttr(longName=op1Name,k=True,hasMinValue=True,hasMaxValue=True,minValue=0,maxValue=1.0)
        if len(object2) == 1:
            addAttr(longName=op2Name,k=True,hasMinValue=True,hasMaxValue=True,minValue=0,maxValue=1.0)
        if len(object3) == 1:
            addAttr(longName=op3Name,k=True,hasMinValue=True,hasMaxValue=True,minValue=0,maxValue=1.0)
        if len(object4) == 1:
            addAttr(longName=op4Name,k=True,hasMinValue=True,hasMaxValue=True,minValue=0,maxValue=1.0)
        if len(object5) == 1:
            addAttr(longName=op5Name,k=True,hasMinValue=True,hasMaxValue=True,minValue=0,maxValue=1.0)
        if len(object6) == 1:
            addAttr(longName=op6Name,k=True,hasMinValue=True,hasMaxValue=True,minValue=0,maxValue=1.0)
        if len(object7) == 1:
            addAttr(longName=op7Name,k=True,hasMinValue=True,hasMaxValue=True,minValue=0,maxValue=1.0)
        if len(object8) == 1:
            addAttr(longName=op8Name,k=True,hasMinValue=True,hasMaxValue=True,minValue=0,maxValue=1.0)
        
        #Create parent constraint
        #Nested If's to run command only with objects entered by user
        if len(object2): #Not empty
            if len(object3):
                if len(object4):
                    if len(object5):
                        if len(object6):
                            if len(object7):
                                if len(object8):
                                    self.pConst = orientConstraint( object1,object2,object3,object4,object5,object6,object7,object8,constObject,mo=True )
                                    #make attributes
                                    addAttr(longName=op1Name,k=True,hasMinValue=True,hasMaxValue=True,minValue=0,maxValue=1.0)
                                    addAttr(longName=op2Name,k=True,hasMinValue=True,hasMaxValue=True,minValue=0,maxValue=1.0)
                                    addAttr(longName=op3Name,k=True,hasMinValue=True,hasMaxValue=True,minValue=0,maxValue=1.0)
                                    addAttr(longName=op4Name,k=True,hasMinValue=True,hasMaxValue=True,minValue=0,maxValue=1.0)
                                    addAttr(longName=op5Name,k=True,hasMinValue=True,hasMaxValue=True,minValue=0,maxValue=1.0)
                                    addAttr(longName=op6Name,k=True,hasMinValue=True,hasMaxValue=True,minValue=0,maxValue=1.0)
                                    addAttr(longName=op7Name,k=True,hasMinValue=True,hasMaxValue=True,minValue=0,maxValue=1.0)
                                    addAttr(longName=op8Name,k=True,hasMinValue=True,hasMaxValue=True,minValue=0,maxValue=1.0)
                                    
                                    #make direct connections
                                    connectAttr( control + '.' + op1Name, self.pConst + '.' + str( object1) + 'W0' )
                                    connectAttr( control + '.' + op2Name, self.pConst + '.' + str( object2) + 'W1' )
                                    connectAttr( control + '.' + op3Name, self.pConst + '.' + str( object3) + 'W2' )
                                    connectAttr( control + '.' + op4Name, self.pConst + '.' + str( object4) + 'W3' )
                                    connectAttr( control + '.' + op5Name, self.pConst + '.' + str( object5) + 'W4' )
                                    connectAttr( control + '.' + op6Name, self.pConst + '.' + str( object6) + 'W5' )
                                    connectAttr( control + '.' + op7Name, self.pConst + '.' + str( object7) + 'W6' )
                                    connectAttr( control + '.' + op8Name, self.pConst + '.' + str( object8) + 'W7' )
                                else:#object8 was empty
                                    self.pConst = orientConstraint( object1,object2,object3,object4,object5,object6,object7,constObject,mo=True )
                                    #make attributes
                                    addAttr(longName=op1Name,k=True,hasMinValue=True,hasMaxValue=True,minValue=0,maxValue=1.0)
                                    addAttr(longName=op2Name,k=True,hasMinValue=True,hasMaxValue=True,minValue=0,maxValue=1.0)
                                    addAttr(longName=op3Name,k=True,hasMinValue=True,hasMaxValue=True,minValue=0,maxValue=1.0)
                                    addAttr(longName=op4Name,k=True,hasMinValue=True,hasMaxValue=True,minValue=0,maxValue=1.0)
                                    addAttr(longName=op5Name,k=True,hasMinValue=True,hasMaxValue=True,minValue=0,maxValue=1.0)
                                    addAttr(longName=op6Name,k=True,hasMinValue=True,hasMaxValue=True,minValue=0,maxValue=1.0)
                                    addAttr(longName=op7Name,k=True,hasMinValue=True,hasMaxValue=True,minValue=0,maxValue=1.0)
                                    
                                    #make direct connections
                                    connectAttr( control + '.' + op1Name, self.pConst + '.' + str( object1) + 'W0' )
                                    connectAttr( control + '.' + op2Name, self.pConst + '.' + str( object2) + 'W1' )
                                    connectAttr( control + '.' + op3Name, self.pConst + '.' + str( object3) + 'W2' )
                                    connectAttr( control + '.' + op4Name, self.pConst + '.' + str( object4) + 'W3' )
                                    connectAttr( control + '.' + op5Name, self.pConst + '.' + str( object5) + 'W4' )
                                    connectAttr( control + '.' + op6Name, self.pConst + '.' + str( object6) + 'W5' )
                                    connectAttr( control + '.' + op7Name, self.pConst + '.' + str( object7) + 'W6' )
                            
                            else:#object7 was empty
                                self.pConst = orientConstraint( object1,object2,object3,object4,object5,object6,constObject,mo=True )
                                #make attributes
                                addAttr(longName=op1Name,k=True,hasMinValue=True,hasMaxValue=True,minValue=0,maxValue=1.0)
                                addAttr(longName=op2Name,k=True,hasMinValue=True,hasMaxValue=True,minValue=0,maxValue=1.0)
                                addAttr(longName=op3Name,k=True,hasMinValue=True,hasMaxValue=True,minValue=0,maxValue=1.0)
                                addAttr(longName=op4Name,k=True,hasMinValue=True,hasMaxValue=True,minValue=0,maxValue=1.0)
                                addAttr(longName=op5Name,k=True,hasMinValue=True,hasMaxValue=True,minValue=0,maxValue=1.0)
                                addAttr(longName=op6Name,k=True,hasMinValue=True,hasMaxValue=True,minValue=0,maxValue=1.0)
                                
                                #make direct connections
                                connectAttr( control + '.' + op1Name, self.pConst + '.' + str( object1) + 'W0' )
                                connectAttr( control + '.' + op2Name, self.pConst + '.' + str( object2) + 'W1' )
                                connectAttr( control + '.' + op3Name, self.pConst + '.' + str( object3) + 'W2' )
                                connectAttr( control + '.' + op4Name, self.pConst + '.' + str( object4) + 'W3' )
                                connectAttr( control + '.' + op5Name, self.pConst + '.' + str( object5) + 'W4' )
                                connectAttr( control + '.' + op6Name, self.pConst + '.' + str( object6) + 'W5' )
                        
                        else:#object6 was empty
                            self.pConst = orientConstraint( object1,object2,object3,object4,object5,constObject,mo=True )
                            #make attributes
                            addAttr(longName=op1Name,k=True,hasMinValue=True,hasMaxValue=True,minValue=0,maxValue=1.0)
                            addAttr(longName=op2Name,k=True,hasMinValue=True,hasMaxValue=True,minValue=0,maxValue=1.0)
                            addAttr(longName=op3Name,k=True,hasMinValue=True,hasMaxValue=True,minValue=0,maxValue=1.0)
                            addAttr(longName=op4Name,k=True,hasMinValue=True,hasMaxValue=True,minValue=0,maxValue=1.0)
                            addAttr(longName=op5Name,k=True,hasMinValue=True,hasMaxValue=True,minValue=0,maxValue=1.0)
                            
                            #make direct connections
                            connectAttr( control + '.' + op1Name, self.pConst + '.' + str( object1) + 'W0' )
                            connectAttr( control + '.' + op2Name, self.pConst + '.' + str( object2) + 'W1' )
                            connectAttr( control + '.' + op3Name, self.pConst + '.' + str( object3) + 'W2' )
                            connectAttr( control + '.' + op4Name, self.pConst + '.' + str( object4) + 'W3' )
                            connectAttr( control + '.' + op5Name, self.pConst + '.' + str( object5) + 'W4' )
                
                    else:#object5 was empty
                        self.pConst = orientConstraint( object1,object2,object3,object4,constObject,mo=True )
                        #make attributes
                        addAttr(longName=op1Name,k=True,hasMinValue=True,hasMaxValue=True,minValue=0,maxValue=1.0)
                        addAttr(longName=op2Name,k=True,hasMinValue=True,hasMaxValue=True,minValue=0,maxValue=1.0)
                        addAttr(longName=op3Name,k=True,hasMinValue=True,hasMaxValue=True,minValue=0,maxValue=1.0)
                        addAttr(longName=op4Name,k=True,hasMinValue=True,hasMaxValue=True,minValue=0,maxValue=1.0)
                        
                        #make direct connections
                        connectAttr( control + '.' + op1Name, self.pConst + '.' + str( object1) + 'W0' )
                        connectAttr( control + '.' + op2Name, self.pConst + '.' + str( object2) + 'W1' )
                        connectAttr( control + '.' + op3Name, self.pConst + '.' + str( object3) + 'W2' )
                        connectAttr( control + '.' + op4Name, self.pConst + '.' + str( object4) + 'W3' )
                else:#object4 was empty
                    
                    self.pConst = orientConstraint( str( object1),str( object2),str( object3),constObject,mo=True )
                    #make attributes
                    addAttr(longName=op1Name,k=True,hasMinValue=True,hasMaxValue=True,minValue=0,maxValue=1.0)
                    addAttr(longName=op2Name,k=True,hasMinValue=True,hasMaxValue=True,minValue=0,maxValue=1.0)
                    addAttr(longName=op3Name,k=True,hasMinValue=True,hasMaxValue=True,minValue=0,maxValue=1.0)
                    #make direct connections
                    connectAttr( control + '.' + op1Name, self.pConst + '.' + str( object1) + 'W0' )
                    connectAttr( control + '.' + op2Name, self.pConst + '.' + str( object2) + 'W1' )
                    connectAttr( control + '.' + op3Name, self.pConst + '.' + str( object3) + 'W2' )
            else:# object 3 was empty
                
                self.pConst = orientConstraint( str( object1),str( object2),constObject,mo=True )
                #make attributes
                addAttr(longName=op1Name,k=True,hasMinValue=True,hasMaxValue=True,minValue=0,maxValue=1.0)
                addAttr(longName=op2Name,k=True,hasMinValue=True,hasMaxValue=True,minValue=0,maxValue=1.0)
                #make direct connections
                connectAttr( control + '.' + op1Name, self.pConst + '.' + str( object1) + 'W0' )
                connectAttr( control + '.' + op2Name, self.pConst + '.' + str( object2) + 'W1' )
                
        else: #object2 was empty
            self.pConst = orientConstraint( str( object1),constObject,mo=True )
            #make attributes
            addAttr(longName=op1Name,k=True,hasMinValue=True,hasMaxValue=True,minValue=0,maxValue=1.0)
            #make direct connections
            connectAttr( control + '.' + op1Name, self.pConst + '.' + str( object1) + 'W0' )
            
        self.createdNodes['constraint'] = self.pConst
        
        
    def loadConst(self,*args):
        sel = ls(sl=True,fl=True)
        textFieldButtonGrp(self.constField,edit=True,text=sel[0])    
        
    def loadCnt(self,*args):
        sel = ls(sl=True,fl=True)
        textFieldButtonGrp(self.cntField,edit=True,text=sel[0])
        
    def loadObj1(self,*args):
        sel = ls(sl=True,fl=True)
        textFieldButtonGrp(self.obj1Field,edit=True,text=sel[0])
    
    def loadObj2(self,*args):
        sel = ls(sl=True,fl=True)
        textFieldButtonGrp(self.obj2Field,edit=True,text=sel[0])
        
    def loadObj3(self,*args):
        sel = ls(sl=True,fl=True)
        textFieldButtonGrp(self.obj3Field,edit=True,text=sel[0])
        
    def loadObj4(self,*args):
        sel = ls(sl=True,fl=True)
        textFieldButtonGrp(self.obj4Field,edit=True,text=sel[0])

    def loadObj5(self,*args):
        sel = ls(sl=True,fl=True)
        textFieldButtonGrp(self.obj5Field,edit=True,text=sel[0])

    def loadObj6(self,*args):
        sel = ls(sl=True,fl=True)
        textFieldButtonGrp(self.obj6Field,edit=True,text=sel[0])

    def loadObj7(self,*args):
        sel = ls(sl=True,fl=True)
        textFieldButtonGrp(self.obj7Field,edit=True,text=sel[0])
        
    def loadObj8(self,*args):
        sel = ls(sl=True,fl=True)
        textFieldButtonGrp(self.obj8Field,edit=True,text=sel[0])
        
