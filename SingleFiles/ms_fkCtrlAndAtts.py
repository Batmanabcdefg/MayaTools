"""
Copyright (c) 2010 Mauricio Santos
Name: ms_fkCtrlAndAtts.py
Version: 1.0
Author: Mauricio Santos
Contact: mauricioptkvp@hotmail.com
Date Created: 26 Sep 2010
Last Modified: 27 Sep 2010

Description: Given a joint chain and a controller, create a group above each joint, then create driving attributes for
	the groups and FK controllers on the joints. Also creates a vis swich for the FK controls. 

To do:

Additional Notes:
    1.0		
"""

import maya.cmds as mc

class ms_fkCtrlAndAtts():
    def __init__(self,*args):
        if(mc.window('fkCtrlAndAttrWin1',exists=True)):
            mc.deleteUI('fkCtrlAndAttrWin1',window=True)

        mc.window('fkCtrlAndAttrWin1',title='FK Atts And Controls',rtf=True)
        mc.columnLayout()

        mc.text('                    How many joint chains?.')

        mc.rowLayout(nc=2,cw2=(100,100))
        mc.text(" ")
        self.numChains = mc.intField()
        mc.setParent("..")

        mc.rowLayout(nc=2,cw2=(80,100))
        mc.text(" ")
        mc.button(label='    -=Continue=-',w=80,c=self.secondWindow)
        mc.setParent("..")

        mc.showWindow('fkCtrlAndAttrWin1')

    def secondWindow(self,*args):
        numFlds = mc.intField(self.numChains,query=True,value=True)

        if(mc.window('fkCtrlAndAttrWin1',exists=True)):
            mc.deleteUI('fkCtrlAndAttrWin1',window=True)

        if(mc.window('fkCtrlAndAttrWin2',exists=True)):
            mc.deleteUI('fkCtrlAndAttrWin2',window=True)

        mc.window('fkCtrlAndAttrWin2',title='FK Atts And Controls',rtf=True)
        mc.columnLayout()

        self.labelField = mc.textFieldGrp(label='Main Label:')
        self.cntField = mc.textFieldButtonGrp(label='Control to add attributes on:',bl='Load',bc=self.loadCnt) 
        self.fkCntField = mc.textFieldButtonGrp(label='FK Control:',bl='Load',bc=self.loadFkCnt) 

        self.attNameFlds = []
        self.startFlds = []
        self.endFlds = []

        x = 0
        while x < numFlds:
            x = x + 1

            mc.frameLayout( label='Limb %i'%x,cll=True,cl=False )
            mc.columnLayout()
            self.attNameFlds.append( mc.textFieldGrp(label='Attribute name:') )
            self.startFlds.append( mc.textFieldButtonGrp(label='Start Joint:',bl='load' )  )
            self.endFlds.append( mc.textFieldButtonGrp(label='End Joint:',bl='load')  )
            mc.setParent("..")
            mc.setParent("..")	

            startFldCmd = 'import maya.cmds as mc\nsel = mc.ls(sl=True,fl=True)\nmc.textFieldButtonGrp("%s", edit=True, text=sel[0])' % self.startFlds[x-1]
            mc.textFieldButtonGrp( self.startFlds[x-1], edit=True,bc = startFldCmd)
            endFldCmd = 'import maya.cmds as mc\nsel = mc.ls(sl=True,fl=True)\nmc.textFieldButtonGrp("%s", edit=True, text=sel[0])' % self.endFlds[x-1]
            mc.textFieldButtonGrp( self.endFlds[x-1], edit=True,bc = endFldCmd)

        mc.text('  Axis: ',font='boldLabelFont')
        self.aimField = mc.radioButtonGrp(label='Curl Rotate Axis:',nrb=3,labelArray3=('x','y','z'),sl=3)
        self.twistField = mc.radioButtonGrp(label='Twist Rotate Axis:',nrb=3,labelArray3=('x','y','z'),sl=1)
        self.upField = mc.radioButtonGrp(label='Spread Rotate Axis:',nrb=3,labelArray3=('x','y','z'),sl=2)

        mc.rowLayout(nc=2,cw2=(200,100))
        mc.text(" ")
        mc.button(label='    -=Create=-',w=80,c=self.create)
        mc.setParent("..")

        mc.showWindow('fkCtrlAndAttrWin2')

    def create(self,*args):
        #Define/Store variables
        label = mc.textFieldGrp(self.labelField,query=True,text=True)
        control = mc.textFieldButtonGrp(self.cntField,query=True,text=True)
        fkControl = mc.textFieldButtonGrp(self.fkCntField,query=True,text=True)

        aimVal = mc.radioButtonGrp(self.aimField,query=True,select=True)
        twistVal = mc.radioButtonGrp(self.twistField,query=True,select=True)
        upVal = mc.radioButtonGrp(self.upField,query=True,select=True)

        #Set aim, twist, up
        aim = ' '
        twist = ' '
        up = ' '

        if aimVal == 1:
            aim = 'X'
        if aimVal == 2:
            aim = 'Y'
        if aimVal == 3:
            aim = 'Z'

        if twistVal == 1:
            twist = 'X'
        if twistVal == 2:
            twist = 'Y'
        if twistVal == 3:
            twist = 'Z'

        if upVal == 1:
            up = 'X'
        if upVal == 2:
            up = 'Y'
        if upVal == 3:
            up = 'Z'

            #Create main attributes on control
        mc.select(control,r=True)
        attList = mc.attributeInfo(control,all=True)

        if(label not in attList):
            try:
                mc.addAttr(longName=label,k=True)
                mc.setAttr(control + '.' + label, lock=True)
            except:
                pass #Attribute already exists

        #Per limb specified by user
        for (nameFld,startJntFld,endJntFld) in zip(self.attNameFlds,self.startFlds,self.endFlds):
            #Get data for current limb
            name = mc.textFieldGrp(nameFld,query=True,text=True)
            startJnt = mc.textFieldButtonGrp(startJntFld,query=True,text=True)
            endJnt = mc.textFieldButtonGrp(endJntFld,query=True,text=True)

            #Get full chain
            chain = []

            #Get the hierarchy of startJnt, then store it until endJnt is found
            try:
                mc.select(startJnt,r=True,hi=True)
                sel = mc.ls(sl=True,fl=True,type='joint')
                tempChain = sel

                for each in tempChain:
                    if each == endJnt:
                        chain.append(each)
                        break
                    else:
                        chain.append(each)
            except:
                pass

            #Store parent of chain
            parent = mc.listRelatives(chain[0],parent=True)

            #Unparent joints
            for each in chain:
                try:
                    mc.parent(each,w=True)
                except:
                    pass

            #Create duplicate joints above orig joints, then store duplicate joint names
            dupJoints = []
            for joint in chain:
                offName = joint + '_off'
                jnt = mc.duplicate(joint,rr=True,po=True,n=offName)
                dupJoints.append(jnt)

            #Rebuild heirarchy
            x = 0
            while x < len(chain):
                mc.parent(chain[x],dupJoints[x])
                if x != 0:
                    mc.parent(dupJoints[x],chain[x-1])
                x = x + 1

            #Adding Curl atts on controller
            x= 0 
            while x < len(chain):
                mc.addAttr(control, longName=name + '_curl_' + str(x+1),k=True)
                x = x + 1

            #Adding spread atts on controller
            x= 0 
            while x < len(chain):
                mc.addAttr(control, longName=name + '_spread_' + str(x+1),k=True)
                x = x + 1

            #Twist
            mc.addAttr(control, longName=name + '_Twist',k=True)

            #Connect attributes to dupJoints rotate's ( aim = curl, up = spread )
            x = 0
            #try:
            mc.connectAttr( control + '.' + name + '_Twist' , str(dupJoints[x][0]) + '.rotate' + twist ) 
            while x < len(chain):
                mc.connectAttr( control + '.' + name + '_curl_' + str(x+1) , str(dupJoints[x][0]) + '.rotate' + aim )
                mc.connectAttr( control + '.' + name + '_spread_' + str(x+1), str(dupJoints[x][0]) + '.rotate' + up )
                x = x + 1
            #except:
            #	pass

            #Create fk controllers on joints
            #Duplicate FK control, parent it to chain joints, delete left over transform node
            for each in chain:
                #Duplicate control
                tempCnt = mc.duplicate(fkControl)
                #Select the shape
                tempShp = mc.pickWalk(tempCnt,direction='down')
                mc.parent(tempShp,each,r=True,s=True)
                mc.delete(tempCnt)

            #reparent chain to parent
            mc.parent(dupJoints[0],parent)

    def loadCnt(self,*args):
        sel = mc.ls(sl=True,fl=True)
        mc.textFieldButtonGrp(self.cntField,edit=True,text=sel[0])     

    def loadFkCnt(self,*args):
        sel = mc.ls(sl=True,fl=True)
        mc.textFieldButtonGrp(self.fkCntField,edit=True,text=sel[0])     
