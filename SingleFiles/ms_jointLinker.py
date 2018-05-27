from __future__ import with_statement # This line is only needed for 2008 and 2009
from pymel.core import *

"""
Copyright (c) 2009,2010 Mauricio Santos
Name: ms_jointLinker.py
Version: 1.0
Author: Mauricio Santos
Contact: mauricioptkvp@hotmail.com
Date Created: 30 Aug 2008
Last Modified: 13 Nov 2010

Description:
 Connect two sets of joints based on location and/or naming with
 direct connections, or constraints. 

To do:
    - Linker: Can select "Type" in GUI for more types, not just 'joint'
    - Figure out how to delete a pane docked to $gMainWindow

Additional Notes:

History:
    2010-Sep-30 : Refactored using PyMEL
    2010-Nov-13 : Added command line interface

"""
class  ms_jointLinker():
    def __init__(self,**keywords):

        if len(keywords):
            self.commandLineCall(keywords)
        else:
            self.buildGUI()
            
    def commandLineCall(self,keywords):
        self.srcJoints = keywords['srcJoints']
        self.tgtJoints = keywords['tgtJoints']
        self.cType = keywords['cType'] #1=None,2=parent,3=point,4=orient,5=scale
        self.slop = keywords['slop']
        self.offsetVal = keywords['offsetVal']
        
        self.connectType = keywords['connectType'] #1=Location, 2=Name
        self.drivenPrefix = keywords['drivenPrefix']
        self.driverPrefix = keywords['driverPrefix']
        self.namespace = keywords['namespace']
        
        self.tVal = keywords['tVal']
        self.rVal = keywords['rVal']
        self.sVal = keywords['sVal']
        
    def buildGUI(self,*args):
        """
        Build the GUI window in Maya
        Returns: "ms_jointLinker"
        2011: Returns: Name of docked pane
        """
        if(window("ms_jointLinkerWin",exists=True)):
            deleteUI("ms_jointLinkerWin",window=True)
        
        with window('ms_jointLinkerWin',rtf=True, title = "Joint Linker v1.0",w=400):
            
            with columnLayout(adj=True): 
                cmds.text(' ')
                with rowLayout(nc=3,cw3=(200,10,200),adj=1):
                    text("\tSource / Driver List")
                    text( " " )
                    text("Target / Driven List")
       
                with columnLayout(adj=True,rs=2):
                        with rowLayout(nc=3,adj=3,cw3=(200,1,200)):
                            self.sourceListLayout = textScrollList(numberOfRows=50, w=200, h=300, ams = True)
                            text( " " )
                            self.targetListLayout = textScrollList(numberOfRows=50, w=200, h=300, ams = True)
                            
                        with rowLayout(nc=3, cl3=('center','center','center'),adj=3,cw3=(200,1,200)):
                            button(label="    Load Source", c = self.loadSourceList,w=200, align='center')
                            text( " " )
                            button(label="    Load Targets", c = self.loadTargetList,w=200, align='center')
            
                        with rowLayout(nc=3,  cl3=('center','center','center'),adj=3,cw3=(200,1,200)):
                            button(label="          Reset", c = self.resetSources,w=200, align='center')
                            text(" ")
                            button(label="          Reset", c = self.resetTargets,w=200, align='center')
                         
                        with rowLayout(nc=3, cl3=('center','center','center'),adj=3,cw3=(200,1,200)):
                            button(label="        Remove", c = self.removeSource,w=200, align='center')
                            text(" ")
                            button(label="        Remove", c = self.removeTarget,w=200, align='center')
                            setParent("..")     
                    
                        with rowLayout(nc=3, cl3=('center','center','center'),adj=3,cw3=(200,1,200)):
                            button(label="        List Size", c = self.sourceSize,w=200, align='center')
                            text(" ")
                            button(label="        List Size", c = self.targetSize,w=200, align='center')
                      
                with frameLayout(label="Constrain", cl=False,cll=True,w=420):
                    with columnLayout(adj=True,rs=5,cal='center'):
                        with rowLayout(nc=2,cw2=(5,200)):
                            text(' ')
                            self.constraintField = optionMenu(label="  Constraint Type: ")
                            menuItem(label="None")
                            menuItem(label="Parent")
                            menuItem(label="Point")
                            menuItem(label="Orient")
                            menuItem(label="Scale")
                            
                        with rowLayout(nc=2,cw2=(5,200)):
                            text(' ')
                            self.offsetField = radioButtonGrp(nrb=2,labelArray2=('Yes','No'),label='Maintain offset? ',sl=1)
                            
                        with rowLayout(nc=2,cw2=(5,200)):
                            text(' ')
                            self.precisionField = floatFieldGrp(label='Precision',value1=0.1,cal=(1,'center'),cw=(1,70))
        
                with frameLayout(label="Direct Connection", cl=True,cll=True,w=420):
                    with columnLayout(adj=True):
                        self.connectField = checkBoxGrp( numberOfCheckBoxes=3, label='Connect', labelArray3=['Translations', 'Rotations', 'Scale'],vr=True )
                        self.cTypeField = radioButtonGrp(label="Match by:",nrb=2,labelArray2=("Location","Name"),sl=1)
                        self.drivenField = textFieldGrp(label="Driven/Target Prefix:",cal=(1,'left'),cw2=(200,50))
                        self.driverField = textFieldGrp(label="Driver/Source Prefix:",cal=(1,'left'),cw2=(200,50))
                        self.namespaceField = textFieldGrp(label="Namespace:",cal=(1,'left'),cw2=(200,50),text=':')

                with frameLayout(label="Helper tools:", cl=True,cll=True,w=420):
                    with columnLayout(adj=True):
                        button(label="Select Hierarchy",c= self.sH)
                        button(label="Remove Constraints",c= self.removeConstraints)
                    
                text(" ")
                with rowLayout(nc=2,cw2=(150,100)):
                    text(" ")
                    button(label="     Link Joints!  ",c=self.guiCall,w=100)

            # Store window name for this instance
            self.guiLayout = 'ms_jointLinkerWin'
        
    #--- Methods
    def sH(self,*args):
        mel.eval('SelectHierarchy;')
        
    def removeConstraints(self,*args):
        """ Remove all constraints from selected object(s) and their heirarchy. """
        sel= ls(sl=True)
        select(sel[0],hi=True)
        constraints = listRelatives(type='constraint',children=True)
        for each in constraints:
            delete(each)
 
    def sourceSize(self,*args):  
        num = 0  
        items = textScrollList(self.sourceListLayout,q=True,ai=True)
        try:
            num = len(items)
        except:
            pass
        print "There are %i items in the source list." % num
        
    def targetSize(self,*args):   
        num = 0
        items = textScrollList(self.targetListLayout,q=True,ai=True)
        try:
            num = len(items)
        except:
            pass
        print "There are %i items in the target list." % num        
     
    def resetSources(self,*args):    
        textScrollList(self.sourceListLayout,e=True,ra=True)
        
    def resetTargets(self,*args):    
        textScrollList(self.targetListLayout,e=True,ra=True)        
        
    def loadSourceList(self,*args):
        sources = ls(sl=True,fl=True,exactType='joint')
        for each in sources:
            textScrollList(self.sourceListLayout,e=True,a=each)
                
    def loadTargetList(self,*args):
        targets = ls(sl=True,fl=True,exactType='joint')
        for each in targets:
            textScrollList(self.targetListLayout,e=True,a=each)  
                
    def removeSource(self,*args):
        selected = textScrollList(self.sourceListLayout,q=True,si=True)    
        for each in selected:
            textScrollList(self.sourceListLayout,e=True,ri=each)  
            
    def removeTarget(self,*args):
        selected = textScrollList(self.targetListLayout,q=True,si=True)    
        for each in selected:
            textScrollList(self.targetListLayout,e=True,ri=each)                                    
               
    def guiCall(self,*args):
        """
        Load all the values passed by gui.
        """
        # Store values
        self.srcJoints = textScrollList(self.sourceListLayout,query=True,allItems=True) 
        self.tgtJoints = textScrollList(self.targetListLayout,query=True,allItems=True)
        self.cType = optionMenu(self.constraintField,query=True,sl=True) #1=None,2=parent,3=point,4=orient,5=scale
        self.slop = floatFieldGrp(self.precisionField,query=True,value1=True)
        self.offsetVal = radioButtonGrp(self.offsetField,query=True,sl=True)
        
        self.connectType = radioButtonGrp(self.cTypeField,q=True,sl=True) #1=Location, 2=Name
        self.drivenPrefix = textFieldGrp(self.drivenField,q=True,text=True)
        self.driverPrefix = textFieldGrp(self.driverField,q=True,text=True)
        self.namespace = textFieldGrp(self.namespaceField,q=True,text=True)
        
        self.tVal = checkBoxGrp(self.connectField,q=True,v1=True)
        self.rVal = checkBoxGrp(self.connectField,q=True,v2=True)
        self.sVal = checkBoxGrp(self.connectField,q=True,v3=True)
        
        self.linkJoints()
     
    def linkJoints(self,*args):
        """
        Link joints
        """
        
        print 'Linking joints...'
        
        srcPos = []
        tgtPos = []
        
        if(self.offsetVal == 1):
            offset = 1
        else:
            offset = 0
        try:
            for each in self.srcJoints:
                temp = xform(each,query=True,ws=True,t=True)
                srcPos.append(temp)
        except:
            pass        
        
        try:
            for each in self.tgtJoints:
                temp = xform(each,query=True,ws=True,t=True)
                tgtPos.append(temp)
        except:
            pass
        
        #--- Constraint Portion
        if(self.cType == 2): #Parent Constraint
            x = 0
            for src in self.srcJoints:  #Check each joint in self.srcJoints against each joint in self.tgtJoints, see if they are overlapping within the given tolerance
                y = 0
                for tgt in self.tgtJoints:
                    if(tgtPos[y][0] < (srcPos[x][0] + self.slop) and tgtPos[y][0] > (srcPos[x][0] - self.slop)):
                        if(tgtPos[y][1] < (srcPos[x][1] + self.slop) and tgtPos[y][1] > (srcPos[x][1] - self.slop)):
                            if(tgtPos[y][2] < (srcPos[x][2] + self.slop) and tgtPos[y][2] > (srcPos[x][2] - self.slop)):
                                parentConstraint(src,tgt,mo=offset)
                    y = y + 1
                x = x + 1

        if(self.cType == 3): #Point Constraint
            x = 0
            for src in self.srcJoints:  #Check each joint in self.srcJoints against each joint in self.tgtJoints, see if they are overlapping within the given tolerance
                y = 0
                for tgt in self.tgtJoints:
                    if(tgtPos[y][0] < (srcPos[x][0] + self.slop) and tgtPos[y][0] > (srcPos[x][0] - self.slop)):
                        if(tgtPos[y][1] < (srcPos[x][1] + self.slop) and tgtPos[y][1] > (srcPos[x][1] - self.slop)):
                            if(tgtPos[y][2] < (srcPos[x][2] + self.slop) and tgtPos[y][2] > (srcPos[x][2] - self.slop)):
                                pointConstraint(src,tgt,mo=offset)
                    y = y + 1
                x = x + 1
                
        if(self.cType == 4): #Orient Constraint
            x = 0
            for src in self.srcJoints:  #Check each joint in self.srcJoints against each joint in self.tgtJoints, see if they are overlapping within the given tolerance
                y = 0
                for tgt in self.tgtJoints:
                    if(tgtPos[y][0] < (srcPos[x][0] + self.slop) and tgtPos[y][0] > (srcPos[x][0] - self.slop)):
                        if(tgtPos[y][1] < (srcPos[x][1] + self.slop) and tgtPos[y][1] > (srcPos[x][1] - self.slop)):
                            if(tgtPos[y][2] < (srcPos[x][2] + self.slop) and tgtPos[y][2] > (srcPos[x][2] - self.slop)):
                                orientConstraint(src,tgt,mo=offset)
                    y = y + 1
                x = x + 1
                
        if(self.cType == 5): #Scale Constraint
            x = 0
            for src in self.srcJoints:  #Check each joint in self.srcJoints against each joint in self.tgtJoints, see if they are overlapping within the given tolerance
                y = 0
                for tgt in self.tgtJoints:
                    if(tgtPos[y][0] < (srcPos[x][0] + self.slop) and tgtPos[y][0] > (srcPos[x][0] - self.slop)):
                        if(tgtPos[y][1] < (srcPos[x][1] + self.slop) and tgtPos[y][1] > (srcPos[x][1] - self.slop)):
                            if(tgtPos[y][2] < (srcPos[x][2] + self.slop) and tgtPos[y][2] > (srcPos[x][2] - self.slop)):
                                scaleConstraint(src,tgt,mo=offset)
                    y = y + 1
                x = x + 1                
        
        
        if(self.connectType == 1): #Location based Connection
            if(self.tVal == 1):
                x = 0
                for src in self.srcJoints:  #Check each joint in self.srcJoints against each joint in self.tgtJoints, see if they are overlapping within the given tolerance
                    y = 0
                    for tgt in self.tgtJoints:
                        if(tgtPos[y][0] < (srcPos[x][0] + self.slop) and tgtPos[y][0] > (srcPos[x][0] - self.slop)):
                            if(tgtPos[y][1] < (srcPos[x][1] + self.slop) and tgtPos[y][1] > (srcPos[x][1] - self.slop)):
                                if(tgtPos[y][2] < (srcPos[x][2] + self.slop) and tgtPos[y][2] > (srcPos[x][2] - self.slop)):
                                    connectAttr(src + ".translate",tgt + ".translate",f=True)
                        y = y + 1
                    x = x + 1 
                
            if(self.rVal == 1):
                x = 0
                for src in self.srcJoints:  #Check each joint in self.srcJoints against each joint in self.tgtJoints, see if they are overlapping within the given tolerance
                    y = 0
                    for tgt in self.tgtJoints:
                        if(tgtPos[y][0] < (srcPos[x][0] + self.slop) and tgtPos[y][0] > (srcPos[x][0] - self.slop)):
                            if(tgtPos[y][1] < (srcPos[x][1] + self.slop) and tgtPos[y][1] > (srcPos[x][1] - self.slop)):
                                if(tgtPos[y][2] < (srcPos[x][2] + self.slop) and tgtPos[y][2] > (srcPos[x][2] - self.slop)):
                                    connectAttr(src + ".rotate",tgt + ".rotate",f=True)
                        y = y + 1
                    x = x + 1
                
            if(self.sVal == 1):
                x = 0
                for src in self.srcJoints:  #Check each joint in self.srcJoints against each joint in self.tgtJoints, see if they are overlapping within the given tolerance
                    y = 0
                    for tgt in self.tgtJoints:
                        if(tgtPos[y][0] < (srcPos[x][0] + self.slop) and tgtPos[y][0] > (srcPos[x][0] - self.slop)):
                            if(tgtPos[y][1] < (srcPos[x][1] + self.slop) and tgtPos[y][1] > (srcPos[x][1] - self.slop)):
                                if(tgtPos[y][2] < (srcPos[x][2] + self.slop) and tgtPos[y][2] > (srcPos[x][2] - self.slop)):
                                    connectAttr(src + ".scale",tgt + ".scale",f=True)
                        y = y + 1
                    x = x + 1
    
        #--- Name based connections
        if(self.connectType == 2): 
            for each in self.tgtJoints:
                #Replace existing prefix with user specified prefix
                temp = each.lstrip(self.drivenPrefix)
                temp = self.driverPrefix + temp
                temp = self.namespace + temp
                
                print temp

                if(self.tVal == 1):
                    try:
                        connectAttr(temp + ".translate",each + ".translate",f=True)
                    except:
                        print "Error connecting to " + temp + ".translate" 
                if(self.rVal == 1):
                    try:
                        connectAttr(temp + ".rotate",each + ".rotate",f=True)
                    except:
                        print "Error connecting to " + temp + ".rotate"     
                if(self.sVal == 1):
                    try:
                        connectAttr(temp + ".scale",each + ".scale",f=True)
                    except:
                        print "Error connecting to " + temp + ".scale"  
        
        print 'Linking done.'                   