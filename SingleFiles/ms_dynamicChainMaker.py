"""
Copyright (c) 2008,2009 Mauricio Santos
Name: ms_dynamicChainMaker.py
Version: 1.0
Author: Mauricio Santos
Contact: mauricioptkvp@hotmail.com
Date Created: 27 Dec 2008
Last Modified: 25 June 2009
License: LGNU
Description:
    Create a dynamic curve and attach to specified start/end controllers.

To do: 

Additional Notes:

"""
#	MakeDynamicChain.py by Mauricio Santos-Hoyos / mauricioptkvp@hotmail.com
#	
#	Process:
#	
#			-Store Joint names
#			
#			-Make Nurbs Plane, set axis, snap to Start Joint 			
#
#			-Create Null group at Base Joint, parent Plane to Null group
#
#			-Draw curve, snapping to joints, Make dynamic
#
#			-IK Spline command (BaseJnt, EndJnt, self.dynCurve)


hairGroups = [] #Stores groups of created dynamic chains


import maya.cmds as mc
import maya.mel as mel

class ms_dynamicChainMaker():
    def __init__(self,*args):
        if(mc.window("dynamicChainMaker",exists=True)):
            mc.deleteUI("dynamicChainMaker",window=True)
    	
        mc.window("dynamicChainMaker",title="Make Dynamic Chain v0.1", rtf=True)
        mc.columnLayout()
    	self.prefixFld = mc.textFieldGrp(label='Prefix',text='L_LampWire_')	
        self.axisSelected = mc.radioButtonGrp(label = 'Chain Axis:', labelArray3=['X','Y','Z'], nrb=3, sl=1)
        
        self.loadStartJntFld = mc.textFieldButtonGrp( label="Start Joint", buttonLabel="Load", bc = self.loadStartJnt  )
        self.loadStartCtrlFld = mc.textFieldButtonGrp( label="Start Control", buttonLabel="Load", bc = self.loadStartCtrl )
        self.loadEndCtrlFld = mc.textFieldButtonGrp( label="End Control (Optional)", buttonLabel="Load", bc = self.loadEndCtrl )
        
        mc.rowLayout(nc=2,cw2=(200,100))
        mc.text(' ')
        mc.button(label = "          Create", c = self.createChain,w=100 )
    	mc.setParent('..')
    		
        mc.showWindow("dynamicChainMaker")
	
    def createChain(self, *args):
        startJnt = mc.textFieldButtonGrp(self.loadStartJntFld, query=True, text=True   )
        self.startCtrl = mc.textFieldButtonGrp(self.loadStartCtrlFld, query=True, text=True   )
        self.endCtrl = mc.textFieldButtonGrp(self.loadEndCtrlFld, query=True, text=True   )        
        self.prefix = mc.textFieldGrp(self.prefixFld, query=True, text=True   )
        
        jointNames = [] 

        mc.select(startJnt, hierarchy=True) 
        jointNames = mc.ls(sl=True,fl=True,typ="joint") 

        axis = mc.radioButtonGrp(self.axisSelected,query=True,sl=True)
        
        mc.select(clear=True)
        #print jointNames
        
        if axis == 1:
            axVal = [1,0,0]
        if axis == 2:
            axVal = [0,1,0]
        if axis == 3:
            axVal = [0,0,1]
        
        planeName = mc.nurbsPlane(p= (0,0,0), ax= axVal, w=.3, lr= 1, d= 3, u= 1, v= 1, ch= 0);
        planeVisAtt = (planeName[0] + ".visibility")
        #Hiding plane
        mc.setAttr(planeVisAtt, 0)

        #snapping plane to start jnt
        pos = mc.xform( startJnt, q=1, ws=True, t=1)
        mc.xform( planeName, ws=True, t=[pos[0], pos[1], pos[2]]) 
        rot = mc.xform( startJnt, q=1, ws=True, ro=1)
        mc.xform( planeName, ws=True, ro=[rot[0], rot[1], rot[2]]) 	
        
        nodeName = (self.prefix + "_DynChain_TopNode") #Create rig top node
        mc.createNode('transform',n=nodeName)
        
        mc.parent(nodeName, self.startCtrl)
        mc.parent(planeName, nodeName)
        
        posTemp = []
        jointPosArray = []
        
        for x in jointNames: #Storing joint positions to create curve with
        	posTemp = mc.xform(x, q=1, ws=True, t=1)
        	#print posTemp
        	jointPosArray.append(posTemp)
        	
        #Create curve
        curveName = (self.prefix + "_BaseCrv")
        curve1 = mc.curve(d=1, point =jointPosArray[0])
        mc.rename(curve1, curveName)
        
        max = len(jointPosArray)
        self.counter = 0
        for x in jointPosArray: 
        	self.counter= self.counter + 1 
        	if self.counter < max: 
        		mc.curve(curveName, append=1, point= jointPosArray[self.counter])
        		
        #Make curve dynamic
        mc.select(curveName,planeName,r=1)
        mel.eval("makeCurvesDynamicHairs 1 0 1")
        
        hairSystemName = mc.pickWalk(curveName,d="up") #Go up to follice
        hairSystemName = mc.pickWalk(hairSystemName,d="up") #Go up to hairSystemFollicles
        	
        temp = hairSystemName[0] #convert list to string
        self.hairSystemName = temp[:-9]	#Remove"Follicles" from name to derive hair system name
        hairSysOPCurves = (self.hairSystemName + "OutputCurves")
        
        self.dynCurve = mc.pickWalk(hairSysOPCurves, d="down")
        		
        for x in jointNames:
        	endEffector = x #Final joint in list
        self.dynCurve = str(self.dynCurve)
        self.dynCurve = self.dynCurve[3:-2] #Cleaning up name via splicing: [u'name1'] = name1
        
        ikHandleName = (self.prefix + "_ikHandle")

        #print self.dynCurve	
        mc.ikHandle(n=ikHandleName ,sol='ikSplineSolver', ccv=0, scv=0, pcv=0,sj=jointNames[0],ee=endEffector, c=str(self.dynCurve));
        
        hairSysFollicles = (self.hairSystemName + "Follicles")
        groupName = (self.prefix + "_DynChain_Grp")   #Setting group name
        
        #clean up nodes
        mc.select(ikHandleName,hairSysOPCurves,hairSysFollicles,self.hairSystemName,r=1)
        mc.group(n=groupName)
        
        mc.select(clear=True)
        grpAttr = (groupName + ".visibility")
        mc.setAttr(grpAttr, 0)
        
        print ("//Created Chain and hid " + groupName + "\n")
        hairGroups.append(groupName)
        
        self.follicle = mc.pickWalk(hairSysFollicles, d='down')  # The follicle
        
        #Create dynamic attributes on controllers
        self.createAtts()
        
        temp = len(self.endCtrl)
        if temp: #Not zero or null
            self.addConstraint()
        #Fin!
    
    def createAtts(self,*args):
        """
            Create follicle attributes on controller and connect them.
        """
        #Create the attributes
        mc.addAttr(self.startCtrl,ln=self.prefix + 'Dynamic',at='float',defaultValue=0,min=0,max=1,k=True)
        mc.setAttr(self.startCtrl + '.' + self.prefix + 'Dynamic', lock=True)
        mc.addAttr(self.startCtrl,ln='StartFrame',at='long',defaultValue=1,k=True)
        mc.addAttr(self.startCtrl,ln='Attract',at='float',defaultValue=0.5,min=0,max=1,k=True)
        mc.addAttr(self.startCtrl,ln='AttractDamp',at='float',defaultValue=0,min=0,max=1,k=True)
        mc.addAttr(self.startCtrl,ln='Stiffness',at='float',defaultValue=0.15,min=0,max=1,k=True)
        
        #Connect the attribute
        mc.connectAttr(self.startCtrl + '.StartFrame', self.hairSystemName + '.startFrame',f=True)
        mc.connectAttr(self.startCtrl + '.Attract', self.hairSystemName + '.startCurveAttract',f=True)
        mc.connectAttr(self.startCtrl + '.AttractDamp', self.hairSystemName + '.attractionDamp',f=True)
        mc.connectAttr(self.startCtrl + '.Stiffness', self.follicle[0] + '.stiffness',f=True)
        
    def addConstraint(self,*args):
        """
            Add transform constraint to dynamic curve and put attributes on start controller
        """
        #select last CV on dynamic curve and end control and create hair transform constraint
        mc.select(self.dynCurve + '.cv[%s]'%self.counter, r=True)
        mc.select(self.endCtrl,add = True)
        mel.eval('createHairConstraint 1;')
        mc.select(clear=True)
        
        #Now, parent the transform constraint to the end control
        num = self.hairSystemName[-1:]          #Just the last number
        hairSystem = self.hairSystemName[:-1]   #All but last number
        temp = mc.listConnections( '%sShape%s' % ( hairSystem, num), c=True)
        for each in temp:
            if 'hairConstraint' in each:
                const = each
                mc.parent(const,self.endCtrl)
        
                #Create the attributes
                mc.addAttr(self.startCtrl,ln=self.prefix + 'EndConstraint',at='float',defaultValue=0,min=0,max=1,k=True)
                mc.setAttr(self.startCtrl + '.' + self.prefix + 'EndConstraint', lock=True)
                mc.addAttr(self.startCtrl,ln='GlueStrength',at='float',defaultValue=1,min=0,max=1,k=True)
                mc.addAttr(self.startCtrl,ln='constStiffness',at='float',defaultValue=0.15,min=0,max=1,k=True)
                
                #Connect the attribute
                mc.connectAttr(self.startCtrl + '.GlueStrength', const + '.glueStrength',f=True)
                mc.connectAttr(self.startCtrl + '.constStiffness', const + '.stiffness',f=True)
        
        
        
        
    def loadStartJnt(self, *args):
        sel = mc.ls(sl=True,fl=True,typ="joint")
        mc.textFieldButtonGrp(self.loadStartJntFld,edit=True,text=sel[0])
        
    def loadStartCtrl(self, *args):
        sel = mc.ls(sl=True,fl=True)
        mc.textFieldButtonGrp(self.loadStartCtrlFld,edit=True,text=sel[0])
        
    def loadEndCtrl(self, *args):
        sel = mc.ls(sl=True,fl=True)
        mc.textFieldButtonGrp(self.loadEndCtrlFld,edit=True,text=sel[0])    
        
        
