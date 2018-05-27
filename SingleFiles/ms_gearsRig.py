"""
Copyright (c) 2010 Mauricio Santos
Name: ms_gearsRig.py
Version: 1.0
Author: Mauricio Santos
Contact: mauricioptkvp@hotmail.com
Date Created: 28 Jan 2010
Last Modified: 30 Jan 2010

Description:
        Connect various items to multipyDivide nodes, and create
        an interface to the MD nodes on user selected control objects.

To do: 
    


"""

import maya.cmds as mc
import MayaGUIModule as mgm

class ms_gearsRig():
    """
        Connect various items to multipyDivide nodes, and create
        an interface to the MD nodes on user selected objects.
    """
    def __init__(self,*args):
        self.gearsGUI()

  
    def gearsGUI(self,*args):
        """
        Create the GUI        
        """
        if(mc.window('gearsRigWin',exists=True)):
            mc.deleteUI('gearsRigWin',window=True)
           
        mc.window('gearsRigWin',title="Gears Rig Setup v1.0",widthHeight=(500,400))
        
        #mc.columnLayout()
        scrollLayout = mc.scrollLayout(
        horizontalScrollBarThickness=16,
        verticalScrollBarThickness=16)
        mc.columnLayout()
        
        mc.text('                   Control Object:     ',fn='boldLabelFont')
        self.cntField = mc.textFieldButtonGrp(label='Control:',bl='Load',bc=self.loadCnt)
        mc.text('                   Driver Object:     ',fn='boldLabelFont')
        self.r1DriverField = mc.textFieldButtonGrp(label='Driver:',bl='Load',bc=self.loadDriver1)
        self.rotateDriverFld1 = mc.radioButtonGrp(label='Driver Rotation Axis', nrb=3, labelArray3=('X','Y','Z'),sl=1 )
        mc.text('                   Attribute Name:     ',fn='boldLabelFont')
        self.attFld = mc.textFieldGrp(label="Attribute Name:")
        mc.text('        Attribute Title Leading Spaces:     ',fn='boldLabelFont')
        self.intFld = mc.intFieldGrp(label="Leading spaces (Max 5):",numberOfFields=1,v1=1)

        mc.separator(w=500)
        
        mc.frameLayout(label="Load Objects to Connect to Rate 1",cll=True,cl=True,w=450)
        mc.columnLayout()
        # Rate 1 list 
        self.rotateFld1 = mc.radioButtonGrp(label='Driven Rotation Axis', nrb=3, labelArray3=('X','Y','Z'),sl=1 )
        mc.rowLayout(nc=2,cw2=(150,200))
        mc.text(' ')
        mc.columnLayout()
        self.rate1ListFld = mc.textScrollList(numberOfRows=10, w=150, ams = True)
        mc.button(label="   Load Objects", c = self.loadList1,w=100)
        mc.button(label="      Reset", c = self.resetList1,w=100)    
        mc.button(label="     Remove", c = self.removeItem1,w=100) 
        mc.button(label="  Select in scene", c = self.selectItems1,w=100) 
        mc.button(label="    List Size", c = self.listSize1,w=100)    
        mc.setParent('..')
        mc.setParent('..')
        
        mc.setParent('..') # End columnlayout
        mc.setParent('..') # End Framelayout
        
        mc.frameLayout(label="Load Objects to Connect to Rate 2",cll=True,cl=True,w=450)
        mc.columnLayout()
        # Rate 2 list 
        self.rotateFld2 = mc.radioButtonGrp(label='Driven Rotation Axis', nrb=3, labelArray3=('X','Y','Z'),sl=1 ) 
        mc.rowLayout(nc=2,cw2=(150,200))
        mc.text(' ')
        mc.columnLayout()
        mc.text(" Rate 2  ",fn='boldLabelFont')
        self.rate2ListFld = mc.textScrollList(numberOfRows=10, w=150, ams = True)
        mc.button(label="   Load Objects", c = self.loadList2,w=100)
        mc.button(label="      Reset", c = self.resetList2,w=100)    
        mc.button(label="     Remove", c = self.removeItem2,w=100) 
        mc.button(label="  Select in scene", c = self.selectItems2,w=100) 
        mc.button(label="    List Size", c = self.listSize2,w=100)    
        mc.setParent('..')
        mc.setParent('..')

        mc.setParent('..') # End columnlayout
        mc.setParent('..') # End Framelayout        
        
        mc.frameLayout(label="Load Objects to Connect to Rate 3",cll=True,cl=True,w=450)
        mc.columnLayout()
        # Rate 3 list
        self.rotateFld3 = mc.radioButtonGrp(label='Driven Rotation Axis', nrb=3, labelArray3=('X','Y','Z'),sl=1 )
        mc.rowLayout(nc=2,cw2=(150,200))
        mc.text(' ')
        mc.columnLayout()
        mc.text(" Rate 3  ",fn='boldLabelFont')
        self.rate3ListFld = mc.textScrollList(numberOfRows=10, w=150, ams = True)
        mc.button(label="   Load Objects", c = self.loadList3,w=100)
        mc.button(label="      Reset", c = self.resetList3,w=100)    
        mc.button(label="     Remove", c = self.removeItem3,w=100)    
        mc.button(label="  Select in scene", c = self.selectItems3,w=100) 
        mc.button(label="    List Size", c = self.listSize3,w=100)    
        mc.setParent('..')
        mc.setParent('..')

        mc.setParent('..') # End columnlayout
        mc.setParent('..') # End Framelayout
        
        mc.frameLayout(label="Load Objects to Connect to Rate 4",cll=True,cl=True,w=450)
        mc.columnLayout() 
        # Rate 4 list
        self.rotateFld4 = mc.radioButtonGrp(label='Driven Rotation Axis', nrb=3, labelArray3=('X','Y','Z'),sl=1 )
        mc.rowLayout(nc=2,cw2=(150,200))
        mc.text(' ')
        mc.columnLayout()
        mc.text(" Rate 4  ",fn='boldLabelFont')
        self.rate4ListFld = mc.textScrollList(numberOfRows=10, w=150, ams = True)
        mc.button(label="   Load Objects", c = self.loadList4,w=100)
        mc.button(label="      Reset", c = self.resetList4,w=100)    
        mc.button(label="     Remove", c = self.removeItem4,w=100) 
        mc.button(label="  Select in scene", c = self.selectItems4,w=100) 
        mc.button(label="    List Size", c = self.listSize4,w=100)    
        mc.setParent('..')
        mc.setParent('..')
        
        mc.setParent('..') # End columnLayout
        mc.setParent('..') # End FrameLayout
        
        mc.separator(w=500)        
        mc.rowLayout(nc=2,cw2=(200,100))
        mc.text(" ")
        mc.button(label="     Rig Gears",c=self.linkGears,w=80)
        mc.setParent('..')
        
        mc.setParent('..') # End main columnLayout
        mc.setParent('..') # End main scrollLayout
        
        mc.showWindow('gearsRigWin')
      
       
    def linkGears(self,*args):
        # Store values
        control = mc.textFieldButtonGrp(self.cntField,query=True,text=True)
        
        driver = mc.textFieldButtonGrp(self.r1DriverField,query=True,text=True)
        driverAxis1 = mc.radioButtonGrp(self.rotateDriverFld1,q=True,sl=True)
        
        attName = mc.textFieldGrp(self.attFld,query=True,text=True)
        spacesInt = mc.intFieldGrp(self.intFld,query=True,v1=True) 
        
        drivenAxis1 = mc.radioButtonGrp(self.rotateFld1,q=True,sl=True)
        drivenAxis2 = mc.radioButtonGrp(self.rotateFld2,q=True,sl=True)
        drivenAxis3 = mc.radioButtonGrp(self.rotateFld3,q=True,sl=True)
        drivenAxis4 = mc.radioButtonGrp(self.rotateFld4,q=True,sl=True)
        
        list1 = mc.textScrollList(self.rate1ListFld,query=True,allItems=True)
        list2 = mc.textScrollList(self.rate2ListFld,query=True,allItems=True)
        list3 = mc.textScrollList(self.rate3ListFld,query=True,allItems=True)
        list4 = mc.textScrollList(self.rate4ListFld,query=True,allItems=True)
        
        # Setting up leading spaces
        if(spacesInt == 1): spaces = "_"
        if(spacesInt == 2): spaces = "__"
        if(spacesInt == 3): spaces = "___"
        if(spacesInt == 4): spaces = "____"
        if(spacesInt == 5): spaces = "_____"
        
        # Create the approriate string variable for the driver rotations
        if(driverAxis1 == 1): driverR1 = 'rotateX'
        if(driverAxis1 == 2): driverR1 = 'rotateY'
        if(driverAxis1 == 3): driverR1 = 'rotateZ'     
        
        # Create string variables for the driven rotations
        if(drivenAxis1 == 1): drivenR1 = 'rotateX'
        if(drivenAxis1 == 2): drivenR1 = 'rotateY'
        if(drivenAxis1 == 3): drivenR1 = 'rotateZ'

        if(drivenAxis2 == 1): drivenR2 = 'rotateX'
        if(drivenAxis2 == 2): drivenR2 = 'rotateY'
        if(drivenAxis2 == 3): drivenR2 = 'rotateZ' 
            
        if(drivenAxis3 == 1): drivenR3 = 'rotateX'
        if(drivenAxis3 == 2): drivenR3 = 'rotateY'
        if(drivenAxis3 == 3): drivenR3 = 'rotateZ' 
            
        if(drivenAxis4 == 1): drivenR4 = 'rotateX'
        if(drivenAxis4 == 2): drivenR4 = 'rotateY'
        if(drivenAxis4 == 3): drivenR4 = 'rotateZ' 

        # Create attributes on control
        mc.select(control,r=True)
        
        mc.addAttr(longName='%s'%spaces, at='enum',en='%s'%attName,k=False )
        mc.setAttr('%s.%s'%(control,spaces),cb=True)
        
        mc.addAttr(longName="%s1"%attName, sn='%s1'%attName[:1], k=True, at='float', dv=1.0 )
        mc.addAttr(longName="%s2"%attName, sn='%s2'%attName[:1], k=True, at='float', dv=1.0 )
        mc.addAttr(longName="%s3"%attName, sn='%s3'%attName[:1], k=True, at='float', dv=1.0 )
        mc.addAttr(longName="%s4"%attName, sn='%s4'%attName[:1], k=True, at='float', dv=1.0 )

        # Create MD Node
        node1 = mc.createNode('multiplyDivide',n="gearMD")
        node2 = mc.createNode('multiplyDivide',n="gearMD")
        
        # Connect drivers to MD node input1X/Y if one is entered by user
        if(len(driver)):
            mc.connectAttr('%s.%s'%(driver,driverR1),'%s.input1X'%node1 , f=True)
            mc.connectAttr('%s.%s'%(driver,driverR1),'%s.input1Y'%node1 , f=True)
            mc.connectAttr('%s.%s'%(driver,driverR1),'%s.input1X'%node2 , f=True)
            mc.connectAttr('%s.%s'%(driver,driverR1),'%s.input1Y'%node2 , f=True)     
        else: # Set input values to 1 so the multiplier can affect the rotations
            mc.setAttr('%s.input1X'%node1,1);
            mc.setAttr('%s.input1Y'%node1,1);
            mc.setAttr('%s.input1X'%node1,1);
            mc.setAttr('%s.input1Y'%node1,1);
        
        # Connect controller to MD node input2X/Y
        mc.connectAttr('%s.%s1'%(control,attName),'%s.input2X'%node1 , f=True)
        mc.connectAttr('%s.%s2'%(control,attName),'%s.input2Y'%node1 , f=True)
        mc.connectAttr('%s.%s3'%(control,attName),'%s.input2X'%node2 , f=True)
        mc.connectAttr('%s.%s4'%(control,attName),'%s.input2Y'%node2 , f=True)
        
        # Connect node outputs to user selected objects
        if (mc.textScrollList(self.rate1ListFld,q=True,ai=True) ): # checks if there are items in the list
            for each in list1:
                mc.connectAttr( '%s.outputX'%node1, '%s.%s'%(each,drivenR1) )
        if (mc.textScrollList(self.rate2ListFld,q=True,ai=True) ):
            for each in list2:
                mc.connectAttr( '%s.outputY'%node1, '%s.%s'%(each,drivenR2) )
        if (mc.textScrollList(self.rate3ListFld,q=True,ai=True) ):
            for each in list3:
                mc.connectAttr( '%s.outputX'%node2, '%s.%s'%(each,drivenR3) )
        if (mc.textScrollList(self.rate4ListFld,q=True,ai=True) ):
            for each in list4:
                mc.connectAttr( '%s.outputY'%node2, '%s.%s'%(each,drivenR4) )

     
    def loadCnt(self,*args):
        sel = mc.ls(sl=True,fl=True)
        mc.textFieldButtonGrp(self.cntField,edit=True,text=sel[0])     
        
    def loadDriver1(self,*args):
        sel = mc.ls(sl=True,fl=True)
        mc.textFieldButtonGrp(self.r1DriverField,edit=True,text=sel[0])   
    
    # rate 1 list button methods    
    def listSize1(self,*args):
        mgm.listSize(self.rate1ListFld)

    def resetList1(self,*args): 
        mgm.resetList(self.rate1ListFld)

    def loadList1(self,*args):  
        mgm.loadList(self.rate1ListFld)

    def removeItem1(self,*args):    
        mgm.removeListItem(self.rate1ListFld)

    def selectItems1(self,*args):
        mgm.selectListItems(self.rate1ListFld)

    # rate 2 list button methods    
    def listSize2(self,*args):  
        mgm.listSize(self.rate2ListFld)

    def resetList2(self,*args):    
        mgm.resetList(self.rate2ListFld)     

    def loadList2(self,*args):
        mgm.loadList(self.rate2ListFld)

    def removeItem2(self,*args):
        mgm.removeListItem(self.rate2ListFld)

    def selectItems2(self,*args):
        mgm.selectListItems(self.rate2ListFld)
        
    # rate 3 list button methods    
    def listSize3(self,*args):  
        mgm.listSize(self.rate3ListFld)

    def resetList3(self,*args):    
        mgm.resetList(self.rate3ListFld)     

    def loadList3(self,*args):
        mgm.loadList(self.rate3ListFld)

    def removeItem3(self,*args):
        mgm.removeListItem(self.rate3ListFld)
 
    def selectItems3(self,*args):
        mgm.selectListItems(self.rate3ListFld)
        
    # rate 4 list button methods    
    def listSize4(self,*args):  
        mgm.listSize(self.rate4ListFld)
    
    def resetList4(self,*args):    
        mgm.resetList(self.rate4ListFld)     
        
    def loadList4(self,*args):
        mgm.loadList(self.rate4ListFld)

    def removeItem4(self,*args):
        mgm.removeListItem(self.rate4ListFld)

    def selectItems4(self,*args):
        mgm.selectListItems(self.rate4ListFld)