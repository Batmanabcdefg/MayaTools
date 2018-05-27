"""
Copyright (c) 2009 Mauricio Santos
Name: ms_autoRbbn_v2.py
Version: 2.0
Author: Mauricio Santos
Contact: mauricioptkvp@hotmail.com
Date Created: 10 June 2009
Last Modified: 10 June 2009
License: LGNU
Description: Builds rbbn weighted to two end joints (ex:shldr/wrist) with following elbow controls (Parented to follicles)

To do: -finalize code: 
        Needs naming of nodes and grouping into : No_Touchy, Translate

Additional Notes:

"""

import os as os
import sys
import maya.cmds as mc
import maya.mel as mel


class ms_autoRbbn_v2():
    #### Internal classes:
    
    """
        Create a ribbon 
        Command Line call:
        
        rg_ribbonMaker(prefix,numJnts,width,aimAxis,upAxis)
        
        Returns: Three controller names in a list
        
    """
    def __init__(self,*args):
        
        temp = len(args)
        
        #Test to see if called with arguments, if so, run script by passing arguments to it
        if(temp > 0):
            self.createRibbon(args) #Passing arguments to function, by passing GUI 

        else:
            ### Initialize, definitions        
            if(mc.window("ms_autoRbbnWin",exists=True)):
                mc.deleteUI("ms_autoRbbnWin",window=True)
            mc.window("ms_autoRbbnWin",title="autoRibbon Limb Rig Maker v1.0",rtf=True)
            mc.columnLayout()

            mc.text(" ")
            self.prefixField = mc.textFieldGrp( label="Prefix: ")
            #self.numJntsField = mc.intFieldGrp( numberOfFields=1, label='Skin Joints:', value1=5 )
            self.widthField = mc.intFieldGrp( numberOfFields=1, label='Length', value1=20 ) 
            mc.text(" ")
            self.aimAxisField = mc.radioButtonGrp(label="Build/Aim Axis:",nrb=3,labelArray3=('x','y','z'),sl=1)
            self.upAxisField = mc.radioButtonGrp(label="Up Axis:",nrb=3,labelArray3=('x','y','z'),sl=2)

            mc.frameLayout(label="Parent to:", w=500,cll=False)
            mc.columnLayout()
            self.typeField = mc.radioButtonGrp(label='Type:',nrb=3,labelArray3=('Constraint','Make Child','None'), sl=3)
            self.moField = mc.radioButtonGrp(label='Maintain Offset:',nrb=2,labelArray2=('On','Off'),sl=2)
            self.topField = mc.textFieldButtonGrp(label='Top (i.e. ShouldrJnt):',bl='Load',bc=self.topLoad)
            self.btmField = mc.textFieldButtonGrp(label='Bottom (i.e. WristJnt):',bl='Load',bc=self.btmLoad)
            mc.setParent("..")
            mc.setParent("..")
            
            mc.rowLayout(nc=3)
            mc.text(" ")
            mc.text(" ")
            mc.button(label="Make Ribbon",c=self.createRibbon)            
            mc.setParent("..")
            mc.text(" ")

            mc.showWindow("ms_autoRbbnWin")
    
    ### The main procedure
    def createRibbon(self,*args):
        temp =len(args[0])
        if temp > 3:
            #Storing names from GUI
            prefix = args[0][0]
            numJnts = 5 #args[0][1]
            width = args[0][2]
            aimAxis = args[0][3]
            upAxis = args[0][4]
            topPrnt = args[0][5]
            btmPrn = args[0][6]
            type = args[0][7]
            mo = args[0][8]
            
        else:
            #Storing names from GUI
            prefix = mc.textFieldGrp(self.prefixField,query=True,text=True)
            numJnts = 5 #mc.intFieldGrp(self.numJntsField,query=True,value1=True)
            width = mc.intFieldGrp(self.widthField,query=True,value1=True)
            aimAxis =mc.radioButtonGrp(self.aimAxisField,query=True,sl=True)
            upAxis =mc.radioButtonGrp(self.upAxisField,query=True,sl=True)        
            topPrnt = mc.textFieldButtonGrp(self.topField,query=True,text=True)
            btmPrnt = mc.textFieldButtonGrp(self.btmField,query=True,text=True)
            type = mc.radioButtonGrp(self.typeField,query=True,sl=True)
            mo = mc.radioButtonGrp(self.moField,query=True,sl=True)
        
        #Now, some error checking. Make sure name is entered and that it's unique
        # If another chain exists any where in the scene, can't use that same name because it causes  
        # errors with the follicle creation        
        
        if(len(prefix)<1):
            mel.eval("warning \"Name field empty. Please enter a name.\"")
            return(0)
            
        if(mc.objExists(prefix + "_topNode")):
            mc.select(prefix + "_topNode")
            
        tempObjects = mc.ls(sl=True)
        
        if(len(tempObjects)>1):
            mel.eval("warning \"Name is not unique. Please select a unique name.\"")
            mc.select(clear=True)
            return(0)  
          
        #Setting up variables
        if(aimAxis == 1):
            aimAxis = "X"
            aim = "X"
        if(aimAxis == 2):
            aimAxis ="Y" 
            aim = "Y"
        if(aimAxis == 3):
            aimAxis = "Z"
            aim = "Z"
            
        if(upAxis == 1):
            upAxis = "X"
            up = "X"
        if(upAxis == 2):
            upAxis = "Y"
            up = "Y"
        if(upAxis == 3):
            upAxis = "Z"    
            up = "Z"
        
        #
        #Making the Nurbs plane
        #
        if(aimAxis == "X"):     #X selected
            tempName = mc.nurbsPlane(pivot=[0,0,0],axis=[0,1,0],width=width,lengthRatio=.2,degree=3,u=numJnts,v=1,ch=1)
            planeName = (prefix + "_rbbn_" + str(tempName[0]))
            mc.rename(tempName[0],planeName)
            mc.select(planeName,r=True)

        elif(aimAxis == "Y"):     #Y selected
            tempName = mc.nurbsPlane(pivot=[0,0,0],axis=[0,1,0],width=width,lengthRatio=.2,degree=3,u=numJnts,v=1,ch=1)
            planeName = (prefix + "_rbbn_" + str(tempName[0]))
            mc.rename(tempName[0],planeName)
        
            #orient surface along axis
            mc.setAttr((planeName + ".rotateAxis"),(90),(0),(90))
            mc.select(planeName,r=True)
        
        elif(aimAxis == "Z"):     #Z selected
            tempName = mc.nurbsPlane(pivot=[0,0,0],axis=[0,0,1],width=width,lengthRatio=.2,degree=3,u=numJnts,v=1,ch=1)
            planeName = (prefix + "_rbbn_" + str(tempName[0]))
            mc.rename(tempName[0],planeName)

            #orient surface along axis
            mc.setAttr((planeName + ".rotateAxis"),0,90,90)
            mc.select(planeName,r=True)
        
        #Resetting up variables
        if(aimAxis == "X"):
            aimAxis = 1.0,0,0
            
        if(aimAxis == "Y"):
            aimAxis = 0,1.0,0
            
        if(aimAxis == "Z"):
            aimAxis = 0,0,1.0
            
            
        if(upAxis == "X"):
            upAxis = 1.0,0,0
            
        if(upAxis == "Y"):
            upAxis = 0,1.0,0
        
        if(upAxis == "Z"):
            upAxis = 0,0,1.0    
            
        #
        #Create follicles
        #
        mc.select(planeName,r=True)
        mel.eval("createHair " + str(numJnts) + " 1 2 0 0 0 0 " + str(numJnts) + " 0 2 1 1") 
        
        #      At this point, the created hairSystemShape1 is selected, which is annoying, because
        #    even for hairSystem2, it's shape node is hairSystemShape1!!! So some work needs to be 
        #    done so that we can grab the hairSystem name with an ls
        #    and using some pickWalking and slicing, so we can select the newly created hairSystem
        #    and create names for the other nodes created.
        
        mc.pickWalk(direction='Up') #From shape to transform of hair system...
        hairSystem = []                        #Clear list so it doesn't grow
        
        hairSystem = mc.ls(sl=True,fl=True)             #Stores: hairSystemX (default name)
        hSystem = hairSystem[0]                 #Convert list item to string
        hOutputCurves = hSystem + "OutputCurves"        
        hFollicles = hSystem + "Follicles"
        
        #Determine hairSystem number to give Follicle group a unique name
        num = len(hSystem)
        num = num - 1
        hSysNum = hSystem[num:]
        
        #rename hairSystemXFollicles
        follicleGrp = (prefix + "Follicles" + hSysNum)     #New follicle grp name
        mc.rename(hFollicles, follicleGrp)            
        
        mc.delete(hSystem,hOutputCurves)
        
        #Delete follicle curves
        hFollicles = mc.listRelatives(follicleGrp,c=True)     #Store all children ( follicles )       
        for each in hFollicles:
            crv = mc.listRelatives(each,c=True) #Store each child of each follicle (curve1, etc...)
            mc.delete(crv[1])                   #Delete the curves
        #    
        #Create control curves and joints: 5: Top,mid1,mid2,mid3,Btm AND Twist control
        #
        conCurves = []
        conJoints = []
        x=0
         
        while(x<5):
            if(aim == "X"):
                conCurves.append( mc.circle(nr=(1,0,0),r=2) )
                conJoints.append( mc.joint(p=(0,0,0),rad=.2 ))
            if(aim == "Y"):
                conCurves.append( mc.circle(nr=(0,1,0),r=2) )
                conJoints.append( mc.joint(p=(0,0,0),rad=.2 ))
            if(aim == "Z"):
                conCurves.append( mc.circle(nr=(0,0,1),r=2) )
                conJoints.append( mc.joint(p=(0,0,0),rad=.2 ))
            x = x + 1

            
        #
        #Snap controllers: 5: Top,mid1,mid2,mid3,Btm
        #
        ##First row of CV's
        mc.select(planeName + ".cv[0][0:3]",r=True)
        temp = mc.cluster()
        temp2 = mc.pointConstraint(temp,conCurves[0],mo=False)
        mc.delete(temp,temp2) 
        
        ##mid1 row of CV's
        mc.select(planeName + ".cv[" + str((numJnts/2) + 0) + "][0:3]",r=True)
        mc.select(planeName + ".cv[" + str((numJnts/2) + 1) + "][0:3]",add=True)
        temp = mc.cluster()
        temp2 = mc.pointConstraint(temp,conCurves[1],mo=False)
        mc.delete(temp,temp2)   
            
        ##mid2 row of CV's
        mc.select(planeName + ".cv[" + str((numJnts/2) + 1) + "][0:3]",r=True)
        mc.select(planeName + ".cv[" + str((numJnts/2) + 2) + "][0:3]",add=True)
        temp = mc.cluster()
        temp2 = mc.pointConstraint(temp,conCurves[2],mo=False)
        mc.delete(temp,temp2)
        
        ##mid3 row of CV's
        mc.select(planeName + ".cv[" + str((numJnts/2) + 2) + "][0:3]",r=True)
        mc.select(planeName + ".cv[" + str((numJnts/2) + 3) + "][0:3]",add=True)
        temp = mc.cluster()
        temp2 = mc.pointConstraint(temp,conCurves[3],mo=False)
        mc.delete(temp,temp2)

        ##Last row of CV's
        mc.select(planeName + ".cv[" + str(numJnts + 2) + "][0:3]",r=True)
        temp = mc.cluster()
        temp2 = mc.pointConstraint(temp,conCurves[4],mo=False)
        mc.delete(temp,temp2)
        
        mc.select(clear=True)
        
        #Binding control top/btm joints to surface here
        bindList = []
        bindList.append(conJoints[0])
        bindList.append(conJoints[4])
        mc.skinCluster(bindList,planeName,dr=4)    
        
        mc.select(clear=True)
        
        #
        # Rename controllers and joints
        #
        x = 0
        for jnt,crv in zip(conJoints,conCurves):
            tempJnt = prefix + '_skin_jnt_' + str(x)
            tempCrv = prefix + '_ctrl_' + str(x)
            mc.rename(jnt,tempJnt)
            conJoints[x]=tempJnt
            #print crv[0]
            mc.rename(crv[0], tempCrv)
            conCurves[x]=tempCrv
            x = x + 1
            
        #
        #Zero controls 
        #
        zeroNodes = []
        x = 0
        for each in conCurves:
            zeroNode = mc.group(em=True)
            
            pos = mc.xform( each, q=1, ws=True, t=1)
            mc.xform( zeroNode, ws=True, t=[pos[0], pos[1], pos[2]]) 

            rot = mc.xform( each, q=1, ws=True, ro=1)
            mc.xform( zeroNode, ws=True, ro=[rot[0], rot[1], rot[2]]) 

            mc.parent(each, zeroNode, a=True)
            
            #Rename
            temp = prefix + '_zero_' + str(x)
            mc.rename(zeroNode,temp)
            zeroNodes.append(temp)
            x = x + 1
        
        #
        # Parent mid controllers to follicles
        #
        mc.parent(zeroNodes[1],hFollicles[1])
        mc.parent(zeroNodes[2],hFollicles[2])
        mc.parent(zeroNodes[3],hFollicles[3])
            
        #
        # Grp controllers
        #
        ctrlGrp = mc.group(zeroNodes[0],zeroNodes[4],name=prefix + '_ControlsGrp')
        #Get follicles Grp
        mc.select(hFollicles[0],r=True)
        mc.pickWalk(direction='Up')
        sel = mc.ls(sl=True,fl=True)
        noTouchy = mc.group(sel[0],planeName,name=prefix + '_NoTouchy')
        mc.group(noTouchy,ctrlGrp,name=prefix + '_topNode')
        
        #Parent top/btm controls to user specified objects.
        if type == 1: #Constraint
            if mo == 1: #Maintain offset
                mc.parentConstraint(topPrnt,zeroNodes[0],mo=True)
                mc.parentConstraint(btmPrnt,zeroNodes[4],mo=True)
            else:
                mc.parentConstraint(topPrnt,zeroNodes[0],mo=False)
                mc.parentConstraint(btmPrnt,zeroNodes[4],mo=False)
        
        if type == 2: #Put in hierarchy
            if mo == 1: #Maintain offset
                mc.parent(zeroNodes[0],topPrnt)
                mc.parent(zeroNodes[4],btmPrnt)
            else:
                #First, snap them to location, and then parent them
                pos = mc.xform( topPrnt, q=1, ws=True, t=1)
                mc.xform( zeroNodes[0], ws=True, t=[pos[0], pos[1], pos[2]]) 
                rot = mc.xform( topPrnt, q=1, ws=True, ro=1)
                mc.xform( zeroNodes[0], ws=True, ro=[rot[0], rot[1], rot[2]])
                mc.parent(zeroNodes[0],topPrnt)
                          
                pos = mc.xform( btmPrnt, q=1, ws=True, t=1)
                mc.xform( zeroNodes[4], ws=True, t=[pos[0], pos[1], pos[2]]) 
                rot = mc.xform( btmPrnt, q=1, ws=True, ro=1)
                mc.xform( zeroNodes[4], ws=True, ro=[rot[0], rot[1], rot[2]])
                mc.parent(zeroNodes[4],btmPrnt)
                
        if type == 3:
            pass
            
        mc.select(clear=True)
        
        

            
        

            
    def topLoad(self,*args):
        sel = mc.ls(sl=True,fl=True)
        mc.textFieldGrp(self.topField,e=True,text=sel[0])
        
    def btmLoad(self,*args):
        sel = mc.ls(sl=True,fl=True)
        mc.textFieldGrp(self.btmField,e=True,text=sel[0])
            
            
            
            
            
            
            
            
            