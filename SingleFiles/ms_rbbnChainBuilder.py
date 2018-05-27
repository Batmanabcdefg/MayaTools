"""
Copyright (c) 2009 Mauricio Santos
Name: ms_rbbnChainBuilder.py
Version: 1.0
Author: Mauricio Santos
Contact: mauricioptkvp@hotmail.com
Date Created: 16 June 2009
Last Modified: 27 July 2009
License: LGNU
Description:
    Given a nurbs ribbon(surface) and start/end controllers, build ribbon.

To do: 
        CV indexing input: This will allow the user to explicity enter cv selection values.
        Low priority. Fix before publishing.

Additional Notes: 

Bug: For some unknown reason, the main control joints are flipped when place. This ends up breaking the rig,
        but the fix is simply to detach skin on both plains, unparent main cntrl joints, place as 
        needed, reparent, reskin planes.
        
        Alos, cntrl joints are sometimes snapped to width vs length. Fix is to invert the cv selections from [0][0:3] to [0:3][0]
        when snapping cntrl joints to top, bottom of plane. Interface idea to allow changing values without going into script: 
        See to-do
        
        Otherwise it works beautifully!:)

"""


import maya.cmds as cmds
import maya.mel as mel

class ms_rbbnChainBuilder():
    """
    Create a Ribbon rig using Hair System follicles on a NURBS plane.
    
    - Create the rbbnRig at the origin
    - Snap to user specified position
    
    """
    def __init__(self,*args):
        if(cmds.window("rbbnChainBuilder",exists=True)):
            cmds.deleteUI("rbbnChainBuilder",window=True)
    	
        cmds.window("rbbnChainBuilder",title="Build Ribbon Rig v1.0", rtf=True)
        cmds.columnLayout()
        
    	self.prefixFld = cmds.textFieldGrp(label='Prefix',text='L_upLegRbbn_')	        
        self.ribbonFld = cmds.textFieldButtonGrp( label="Ribbon:", buttonLabel="Load", bc = self.loadRibbon)#,text='main_plane'  )
        self.startFld = cmds.textFieldButtonGrp( label="Start Control:", buttonLabel="Load", bc = self.loadStart,text='cnt_1'  )
        self.endFld = cmds.textFieldButtonGrp( label="End Control:", buttonLabel="Load", bc = self.loadEnd,text='cnt_2' )
        self.numFld = cmds.intFieldGrp(label='Controls:',nf=1,v1=5)
        self.skinFld = cmds.intFieldGrp(label='Skin Joints:',nf=1,v1=5)
        self.buildFld = cmds.radioButtonGrp(nrb=2,labelArray2=('U','V'),label='Build along:',sl=1)
        
        
        cmds.frameLayout(label='Control Options: ',fn='boldLabelFont',cll=False)
        cmds.columnLayout()
        self.crvCreateFld = cmds.radioButtonGrp(nrb=2,labelArray2=('Yes','No'),label='Create bend-bo controls?',sl=1)
        self.radFld = cmds.floatFieldGrp(label='Radius:',nf=1,v1=0.2)
        self.crvNrFld = cmds.radioButtonGrp(nrb=3,labelArray3=('X','Y','Z'),label='Controller normal Axis:',sl=2)
        cmds.setParent("..")
        cmds.setParent("..")
        
        cmds.rowLayout(nc=2,cw2=(200,100))
        cmds.text(' ')
        cmds.button(label = "          Create", c = self.buildRig,w=100 )
    	cmds.setParent('..')
    		
        cmds.showWindow("rbbnChainBuilder")
	
    def buildRig(self, *args):
        # Store the input from the GUI
        self.prefix = cmds.textFieldGrp(self.prefixFld,query=True,text=True)
        self.ctrlRbbn = cmds.textFieldButtonGrp(self.ribbonFld, query=True, text=True   )
        self.startCtrl = cmds.textFieldButtonGrp(self.startFld, query=True, text=True   )
        self.endCtrl = cmds.textFieldButtonGrp(self.endFld, query=True, text=True   )
        numCtrls = cmds.intFieldGrp(self.numFld,query=True,v=True)
        numJnts = cmds.intFieldGrp(self.skinFld,query=True,v=True)
        bldAxis = cmds.radioButtonGrp(self.buildFld,query=True,sl=True)
        
        createCrvs = cmds.radioButtonGrp(self.crvCreateFld,query=True,sl=True)
        rad = cmds.floatFieldGrp(self.radFld,query=True,v=True)
        crvAxis = cmds.radioButtonGrp(self.crvNrFld,query=True,sl=True)
        
        # Create rig top node
        topNode = (self.prefix + "_TopNode") 
        cmds.createNode('transform',n=topNode)
        		
        #
        # Duplicate ribbon
        #
        self.skinRbbn = cmds.duplicate(self.ctrlRbbn)
        
        #
        # Get number spansU or V, depending on surface build, to be able to select the last row of CV's
        #
        lastRow = 0
        self.numU = cmds.getAttr(self.ctrlRbbn+".spansU") + 2
        self.numV = cmds.getAttr(self.ctrlRbbn+".spansU") + 2
        if self.numV > self.numU:
            lastRow = self.numV
        else:
            lastRow = self.numU
        
        #
        # Create and place 2 ctrlRbbn control joints.
        #
        self.mainCtrlJnts= []
        self.mainCtrlJnts.append( cmds.joint(p=(0,0,0), name = self.prefix + 'MainCtr_1' ))  
        cmds.select(clear=True)
        self.mainCtrlJnts.append( cmds.joint(p=(0,0,0), name = self.prefix + 'MainCtr_2' ))    
        cmds.select(clear=True)
        
        #ParentConstraint first joint to statr control, and second to End control
        cmds.parentConstraint(self.startCtrl, self.mainCtrlJnts[0],mo=False)
        cmds.parentConstraint(self.endCtrl, self.mainCtrlJnts[1],mo=False)
        
        #
        #---start: Setup ctrlRbbn
        #
        cmds.select(self.ctrlRbbn,r=True)
        if(bldAxis == 1):#U
            mel.eval("createHair %s 1 2 0 0 0 0 %s 0 2 1 1" % (str(numCtrls[0]), str(numCtrls[0])) )
        if(bldAxis == 2):#V
            mel.eval("createHair 1 %s 2 0 0 0 0 %s 0 2 1 1" % (str(numCtrls[0]), str(numCtrls[0])) )
        
        #      At this point, the created hairSystemShape1 is selected, which is annoying, because
        #    even for hairSystem2, it's shape node is hairSystemShape1!!! So some work needs to be 
        #    done so that we can grab the hairSystem name with an ls
        #    and using some pickWalking and slicing, so we can select the newly created hairSystem
        #    and create names for the other nodes created.
        
        cmds.pickWalk(direction='Up')                 #From shape to transform of hair system...
        hairSystem = []                             #Clear list so it doesn't grow
        
        ctrHairSystem = cmds.ls(sl=True,fl=True)        #Stores: hairSystemX (default name)
        ctrHSystem = ctrHairSystem[0]                   #Convert list item to string
        ctrHOutputCurves = ctrHSystem + "OutputCurves"        
        ctrHFollicles = ctrHSystem + "Follicles"
        
        #Determine hairSystem number to give Follicle group a unique name
        num = len(ctrHSystem)
        num = num - 1
        ctrHSysNum = ctrHSystem[num:]
        
        #rename hairSystemXFollicles
        ctrfollicleGrp = (self.prefix + "ctrlFollicles" + ctrHSysNum)  #New follicle grp name
        cmds.rename(ctrHFollicles, ctrfollicleGrp)            
        
        cmds.delete(ctrHSystem,ctrHOutputCurves)
        
        #
        #Delete follicle curves and Create ctrlJnts per follicle
        #
        ctrHFollicles = cmds.listRelatives(ctrfollicleGrp,c=True)        #Store all children ( follicles )    
        self.ctrlSkinJnts = []
        crvs = []                   #Hold control/bend-bo curve names
        x = 0   
        for each in ctrHFollicles:
            cmds.select(clear=True)
            #if createCrvs is on
            if createCrvs == 1:
                #Create the circle
                crvName = self.prefix + 'BendBo_' + str(x)
                if crvAxis == 1:
                    cmds.circle(name=crvName,radius=rad[0],nr=(1,0,0) )
                if crvAxis == 2:
                    cmds.circle(name=crvName,radius=rad[0],nr=(0,1,0) )
                if crvAxis == 3:
                    cmds.circle(name=crvName,radius=rad[0],nr=(0,0,1) )
                crvs.append(crvName)
                
                #Delete history
                cmds.delete(crvName,ch=True)
                
                #Snap it to follicle
                temp = cmds.pointConstraint(each,crvName,mo=False)  
                temp2 = cmds.orientConstraint(each,crvName,mo=False,offset=(0,90,0))      
                cmds.delete(temp,temp2)
                
                #Zero curve
                zeroNode = cmds.group(em=True,n=crvName + '_buffer')        
                pos = cmds.xform( crvName, q=1, ws=True, t=1)
                cmds.xform( zeroNode, ws=True, t=[pos[0], pos[1], pos[2]]) 
        
                rot = cmds.xform( crvName, q=1, ws=True, ro=1)
                cmds.xform( zeroNode, ws=True, ro=[rot[0], rot[1], rot[2]]) 
                
                scale = cmds.xform( crvName, q=1, r=True, s=1)
                cmds.xform( zeroNode, ws=True, s=[scale[0], scale[1], scale[2]])
        
                cmds.parent(crvName, zeroNode, a=True)
                
                #Parent to follicle
                cmds.parent(zeroNode,each)
                
                #Create joint    
                jnt = cmds.joint( n = self.prefix + 'ctrJnt_' + str(x) )  
                #Snap it to bend-bo control
                temp = cmds.pointConstraint(crvName,jnt,mo=False)            
                cmds.delete(temp)
                #Parent it to crvName
                cmds.parent(jnt,crvName)

            
            else: #Just the jnt to the follicle, no control
                #Create joint    
                jnt = cmds.joint( n = self.prefix + 'ctrJnt_' + str(x) )  
                #Snap it to follicle, parent it to crvName
                temp = cmds.pointConstraint(each,jnt,mo=False)            
                cmds.delete(temp)
                cmds.parent(jnt,each)
            
            #Delete the curves
            crv = cmds.listRelatives(each,c=True)                     #Store each child of each follicle (ie. curve1)
            cmds.delete(crv[1])                                       
            self.ctrlSkinJnts.append(jnt)                           #Store joint names
            x = x + 1
        
        #Set the radius to .5 in the ctrl joints
        for each in self.ctrlSkinJnts:
            cmds.setAttr(each + '.radius',.5)
        
        #
        # Finishing up on ctrlRbbn: skin ctrl joints to ctrlRbbn
        #
        cmds.skinCluster(self.mainCtrlJnts[0], self.mainCtrlJnts[1],self.ctrlRbbn,tsb=True)
        
        #
        # End of ctrlRbbn setup
        #

        
        #
        #---start: Setup skinRbbn
        #
        cmds.select(self.skinRbbn,r=True)
        if(bldAxis == 1):#U
            mel.eval("createHair %s 1 2 0 0 0 0 %s 0 2 1 1" % (str(numJnts[0]), str(numJnts[0])) )
        if(bldAxis == 2):#V
            mel.eval("createHair 1 %s 2 0 0 0 0 %s 0 2 1 1" % (str(numJnts[0]), str(numJnts[0])) )
        
        cmds.pickWalk(direction='Up')                 #From shape to transform of hair system...
        hairSystem = []                             #Clear list so it doesn't grow
        
        skinHairSystem = cmds.ls(sl=True,fl=True)        #Stores: hairSystemX (default name)
        skinHSystem = skinHairSystem[0]                   #Convert list item to string
        skinHOutputCurves = skinHSystem + "OutputCurves"        
        skinHFollicles = skinHSystem + "Follicles"
        
        #Determine hairSystem number to give Follicle group a unique name
        num = len(ctrHSystem)
        num = num - 1
        skinHSysNum = skinHSystem[num:]
        
        #rename hairSystemXFollicles
        skinfollicleGrp = (self.prefix + "skinFollicles" + skinHSysNum)  #New follicle grp name
        cmds.rename(skinHFollicles, skinfollicleGrp)            
        
        cmds.delete(skinHSystem,skinHOutputCurves)
        
        #
        #Delete follicle curves and Create skinJnts per follicle
        #
        skinHFollicles = cmds.listRelatives(skinfollicleGrp,c=True)        #Store all children ( follicles )    
        self.skinSkinJnts = []
        x = 0   
        for each in skinHFollicles:
            cmds.select(clear=True)
            jnt = cmds.joint( n = self.prefix + 'skinJnt_' + str(x), r=.2 )       #Create joint
            temp = cmds.pointConstraint(each,jnt,mo=False)            #Snap/parent it to follicle
            cmds.delete(temp)
            cmds.parent(jnt,each)
            crv = cmds.listRelatives(each,c=True)                     #Store each child of each follicle (ie. curve1)
            cmds.delete(crv[1])                                       #Delete the curves
            self.skinSkinJnts.append(jnt)                           #Store joint names
            x = x + 1
            
        #Set the radius to .2 in the skin joints
        for each in self.skinSkinJnts:
            cmds.setAttr(each + '.radius',.2)
        
        #
        #--- Finishing up on skinRbbn: skin ctrl joints to skinRbbn
        #
        cmds.select(clear=True)
        for each in self.ctrlSkinJnts:
            cmds.select(each,add=True)
        
        cmds.select(self.skinRbbn,add=True)
        sel = cmds.ls(sl=True,fl=True) 
           
        cmds.skinCluster(sel,tsb=True)
        
        #
        # End of ctrlRbbn setup
        #
        
        #Organizing and hiding stuff...
        cmds.parent(ctrfollicleGrp,skinfollicleGrp,self.ctrlRbbn,self.skinRbbn,self.mainCtrlJnts[1],topNode)
        
        #Hide: Planes and mainCtrlJnts
        cmds.setAttr(self.mainCtrlJnts[0] + '.visibility',0)
        cmds.setAttr(self.mainCtrlJnts[1] + '.visibility',0)
        cmds.setAttr(self.ctrlRbbn + '.visibility',0)
        cmds.setAttr(self.skinRbbn[0] + '.visibility',0)
        
        #Fin!

    def loadRibbon(self, *args):
        sel = cmds.ls(sl=True,fl=True)
        cmds.textFieldButtonGrp(self.ribbonFld,edit=True,text=sel[0])
        
    def loadStart(self, *args):
        sel = cmds.ls(sl=True,fl=True)
        cmds.textFieldButtonGrp(self.startFld,edit=True,text=sel[0])
        
    def loadEnd(self, *args):
        sel = cmds.ls(sl=True,fl=True)
        cmds.textFieldButtonGrp(self.endFld,edit=True,text=sel[0])
        
        
        
        
        
