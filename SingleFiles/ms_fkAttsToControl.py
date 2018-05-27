"""
Copyright (c) 2008,2009 Mauricio Santos
Name: ms_fkAttsToControl.py
Version: 1.0
Author: Mauricio Santos
Contact: mauricioptkvp@hotmail.com
Date Created: 26 Dec 2008
Last Modified: 22 Dec 2009
License: LGNU
Description: Quickly setup finger attributes on given hand controller

To do:
    -Add joints per limb option.

Additional Notes:
    1.0		11 June 2009: Major revision. Make it more flexible. Added start/end joints + unique attribute name.
    1.1		22 Dec 2009: Made it so user can enter the amount of chains to connect, vs the fixed 5 I had before.	
"""

import maya.cmds as mc

class ms_fkAttsToControl():
    def __init__(self,*args):
        if(mc.window('fkInitialWin',exists=True)):
            mc.deleteUI('fkInitialWin',window=True)

        mc.window('fkInitialWin',title='FK Atts To Control v1.1',rtf=True)
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

        mc.showWindow('fkInitialWin')

    def secondWindow(self,*args):
        if(mc.window('fkAttsToControlWin',exists=True)):
            mc.deleteUI('fkAttsToControlWin',window=True)

        numFlds = mc.intField(self.numChains,query=True,value=True)

        if(mc.window('fkInitialWin',exists=True)):
            mc.deleteUI('fkInitialWin',window=True)

        mc.window('fkAttsToControlWin',title='FK Atts To Control v1.1',rtf=True)
        mc.columnLayout()

        self.labelField = mc.textFieldGrp(label='Main Label:',text='L_Hand')
        self.cntField = mc.textFieldButtonGrp(label='Control:',bl='Load',bc=self.loadCnt) 


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


            startFldCmd = 'sel = mc.ls(sl=True,fl=True)\nmc.textFieldButtonGrp("%s", edit=True, text=sel[0])' % self.startFlds[x-1]
            mc.textFieldButtonGrp( self.startFlds[x-1], edit=True,bc = startFldCmd)
            endFldCmd = 'sel = mc.ls(sl=True,fl=True)\nmc.textFieldButtonGrp("%s", edit=True, text=sel[0])' % self.endFlds[x-1]
            mc.textFieldButtonGrp( self.endFlds[x-1], edit=True,bc = endFldCmd)

        mc.text('  Axis: ',font='boldLabelFont')
        self.aimField = mc.radioButtonGrp(label='Curl Rotate Axis:',nrb=3,labelArray3=('x','y','z'),sl=3)
        self.twistField = mc.radioButtonGrp(label='Twist Rotate Axis:',nrb=3,labelArray3=('x','y','z'),sl=1)
        self.upField = mc.radioButtonGrp(label='Spread Rotate Axis:',nrb=3,labelArray3=('x','y','z'),sl=2)

        mc.rowLayout(nc=2,cw2=(200,100))
        mc.text(" ")
        mc.button(label='    -=Create=-',w=80,c=self.createHand)
        mc.setParent("..")

        mc.showWindow('fkAttsToControlWin')


    def createHand(self,*args):
        #Define/Store variables
        label = mc.textFieldGrp(self.labelField,query=True,text=True)
        control = mc.textFieldButtonGrp(self.cntField,query=True,text=True)

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

        #Create attributes on control
        mc.select(control,r=True)
        attList = mc.attributeInfo(control,all=True)

        if(label not in attList):
            try:
                mc.addAttr(longName=label,k=True)
                mc.setAttr(control + '.' + label, lock=True)
            except:
                pass #Attribute already exists

        for (nameFld,startJntFld,endJntFld) in zip(self.attNameFlds,self.startFlds,self.endFlds):
            attList = mc.attributeInfo(control,all=True)

            name = mc.textFieldGrp(nameFld,query=True,text=True)
            startJnt = mc.textFieldButtonGrp(startJntFld,query=True,text=True)
            endJnt = mc.textFieldButtonGrp(endJntFld,query=True,text=True)


            #Get full chain for each
            chain = []

            #Get the hierarchy of start1, then store it until end1 is found, etc...
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

            #Adding Curl atts on controller
            x= 0 
            while x < len(chain):
                mc.addAttr(control, longName=name + '_curl_' + str(x+1), k=True)
                x = x + 1

            #Adding spread atts on controller
            x= 0 
            while x < len(chain):
                mc.addAttr(control, longName=name + '_spread_' + str(x+1), k=True)
                x = x + 1

            #Twist
            x= 0 
            while x < len(chain):            
                mc.addAttr(control, longName=name + '_twist_' + str(x+1), k=True)
                x = x + 1

            #Connect attributes to joint rotate's ( aim = curl, up = spread )
            x = 0
            try:
                
                while x < len(chain):
                    mc.connectAttr( control+'.'+name + '_curl_' + str(x+1) , chain[x] + '.rotate' + aim )
                    mc.connectAttr( control+'.'+name + '_spread_' + str(x+1), chain[x] + '.rotate' + up )
                    mc.connectAttr( control+'.'+name + '_twist_' + str(x+1), chain[x] + '.rotate' + twist ) 
                    x = x + 1
            except:
                pass



    def loadCnt(self,*args):
        sel = mc.ls(sl=True,fl=True)
        mc.textFieldButtonGrp(self.cntField,edit=True,text=sel[0])     
