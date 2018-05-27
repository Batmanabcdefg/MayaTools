"""
Copyright (c) 2009 Mauricio Santos
Name: ms_autoScapula.py
Version: 1.0
Author: Mauricio Santos
Contact: mauricioptkvp@hotmail.com
Date Created: 14 July 2009
Last Modified: 15 July 2009
License: LGNU
Description:
    Creates an IK SC solver based auto scapula rig.

To do: 

"""

import maya.cmds as mc

class ms_autoScapula():
    """
    builds an auto scapula rig.
    """
    def __init__(self,*args,**kwargs):
        if(mc.window('autoScapulaWin',exists=True)):
           mc.deleteUI('autoScapulaWin',window=True)

        mc.window('autoScapulaWin',title="IK Scapula Rig v1.0",rtf=True)
        mc.columnLayout()
        
        mc.frameLayout(label='Notes',w=450,cl=True,cll=True)
        mc.columnLayout()
        mc.text(' ')
        mc.text('    Scapula should have three joints: base/mid/end')      
        mc.text('    Clavicle should have two joints: base/end')  
        mc.text('    Bases should insert to back and ends near up_arm(shoulder.)') 
        mc.text('    Controller is were the attributes will be placed.')
        mc.text('    These attributes allow you to toggle the automatic behavior.')
        mc.text(' ')
        mc.text('    The shoulder Control needs to have a parent node above it with no constraints.' )
        mc.text('    The leg is only tied to this rig via a parentConstraint from the ')
        mc.text('    up_leg to the shoulder control.')
        mc.text(' ')
        
        mc.setParent('..')
        mc.setParent('..')
        
        self.prefixFld = mc.textFieldGrp(label='Prefix', text='L_scap_')
        
        mc.text('    Joints:     ',fn='boldLabelFont')
        self.scapRootFld = mc.textFieldButtonGrp(label='Scapula Root:',bl='Load',bc=self.loadScapRoot,text='L_scap_root')
        self.clavRootFld = mc.textFieldButtonGrp(label='Clavicle Root:',bl='Load',bc=self.loadClavRoot,text='L_clav_root')
        self.legFld = mc.textFieldButtonGrp(label='Leg Root:',bl='Load',bc=self.loadLeg,text='L_up_leg')
        
        mc.separator(w=500)
       
        mc.text('    Control:     ',fn='boldLabelFont')
        self.cntFld = mc.textFieldButtonGrp(label='Wrist/Ankle Controller:',bl='Load',bc=self.loadCnt,text='foot_cnt')
        self.shldrFld = mc.textFieldButtonGrp(label='Shoulder Controller',bl='Load',bc=self.loadShldr,text='shldr_cnt')

        mc.separator(w=500)
        
        mc.text('    Clavicle Rotations:     ',fn='boldLabelFont')
        self.frontBackFld= mc.radioButtonGrp(label='Front/Back Axis:',labelArray3=('X','Y','Z'),nrb=3,sl=2)
        self.fbPolarityFld = mc.radioButtonGrp(label='Polarity:',labelArray2 = ('+','-'),sl=2,nrb=2)
        mc.text(' ')
        self.upDownFld = mc.radioButtonGrp(label='Up/Down Axis:',labelArray3=('X','Y','Z'),nrb=3,sl=3)
        self.upPolarityFld = mc.radioButtonGrp(label='Polarity:',labelArray2 = ('+','-'),sl=1,nrb=2)
        
        mc.separator(w=500)
        
        #Create button
        mc.rowLayout(nc=2,cw2=(200,100))
        mc.text(" ")
        mc.button(label="     Create Rig  ",c=self.createAutoScap,w=100)
        
        mc.showWindow('autoScapulaWin')
        
    def createAutoScap(self,*args):
        """
         Create ik based auto scapula rig.
        """
        #Store user values in variables
        prefix = mc.textFieldGrp(self.prefixFld,q=True,text=True)
        scapRoot = mc.textFieldButtonGrp(self.scapRootFld,q=True,text=True)
        clavRoot = mc.textFieldButtonGrp(self.clavRootFld,q=True,text=True)
        legJnt = mc.textFieldButtonGrp(self.legFld,q=True,text=True)
        foot_cnt = mc.textFieldButtonGrp(self.cntFld,q=True,text=True)
        shldrCnt = mc.textFieldButtonGrp(self.shldrFld,q=True,text=True)
        fbAxis = mc.radioButtonGrp(self.frontBackFld,q=True,sl=True)
        fbPolarity = mc.radioButtonGrp(self.fbPolarityFld,q=True,sl=True)
        upDownAxis = mc.radioButtonGrp(self.upDownFld,q=True,sl=True)
        upPolarity = mc.radioButtonGrp(self.upPolarityFld,q=True,sl=True)
        
        #Get joint chains
        mc.select(scapRoot,r=True,hi=True)
        scapChain = mc.ls(sl=True,fl=True)
        mc.select(clavRoot,r=True,hi=True)
        clavChain = mc.ls(sl=True,fl=True)
        
        #Rename axis variables from int(1-3) into a character (X,Y,Z)
        if fbAxis == 1:
            fbAxis = 'X'
        if fbAxis == 2:
            fbAxis = 'Y'
        if fbAxis == 3:
            fbAxis = 'Z'
            
        if upDownAxis == 1:
            upDownAxis = 'X'
        if upDownAxis == 2:
            upDownAxis = 'Y'
        if upDownAxis == 3:
            upDownAxis = 'Z'
        
        #Create SC ik for scapula
        scapHandle = mc.ikHandle(solver='ikSCsolver', startJoint=scapChain[0],ee=scapChain[2],name=('%sscapIkHandle'%prefix))
        
        #Parent shldr_cnt buffer to end of clavicle so it follows auto behavior
        shldrBuffer = mc.pickWalk(shldrCnt,direction='Up')
        shldrPconst = mc.parentConstraint(clavChain[1],shldrBuffer,mo=True)
        
        #Parent leg/arm_up and ikSC_handle to shldrCnt
        scapPconst = mc.parentConstraint(shldrCnt,scapHandle[0],mo=True)
        legPconst = mc.parentConstraint(shldrCnt,legJnt,mo=True)
        
        
        #create attributes on wrist/ankle controller
        mc.addAttr(foot_cnt,ln='scapula',k=True)
        mc.setAttr(foot_cnt+'.scapula',lock=True)
        mc.addAttr(foot_cnt, ln='autoScap',k=True,min=0,max=10,dv=0)
        mc.addAttr(foot_cnt,ln='clavicle',k=True)
        mc.setAttr(foot_cnt+'.clavicle',lock=True)
        mc.addAttr(foot_cnt, ln='autoClav',k=True,min=0,max=20,dv=0)
        
        #Create and setup clavicle frontBackMD node
        clavFB_MD = mc.createNode('multiplyDivide', name=('%sclavFB_MD'%prefix) ) 
        mc.connectAttr(foot_cnt+'.translateZ', clavFB_MD+'.input1X',f=True)
        mc.connectAttr(foot_cnt+'.autoClav', clavFB_MD+'.input2X',f=True)
        mc.connectAttr(clavFB_MD+'.outputX', '%s.rotate%s'%(clavRoot,fbAxis),f=True)
        
        if fbPolarity == 2: #Create inversion node and invert the value of outputX
            fb_invert = mc.createNode('reverse',n=prefix+'invertFB')
            mc.connectAttr(clavFB_MD +'.outputX',fb_invert+'.inputX',f=True)
            mc.connectAttr(fb_invert+'.outputX', '%s.rotate%s'%(clavRoot,fbAxis),f=True)
        
        #Create and setup clavicle upDownMD node
        clavUD_MD = mc.createNode('multiplyDivide', name=('%sclavUD_MD'%prefix) ) 
        mc.connectAttr(foot_cnt+'.translateY', clavUD_MD+'.input1X',f=True)
        mc.connectAttr(foot_cnt+'.autoClav', clavUD_MD+'.input2X',f=True)
        mc.connectAttr(clavUD_MD+'.outputX', '%s.rotate%s'%(clavRoot,upDownAxis),f=True)
        
        if upPolarity == 2: #Create inversion node and invert the value of outputX
            up_invert = mc.createNode('reverse',n=prefix+'invertUD')
            mc.connectAttr(clavUD_MD +'.outputX',up_invert+'.inputX',f=True)
            mc.connectAttr(up_invert+'.outputX', '%s.rotate%s'%(clavRoot,fbAxis),f=True)
            

        
    def loadScapRoot(self,*args):
        """
        Load current selection to Scapula Root Field
        """
        sel = mc.ls(sl=True)
        mc.textFieldButtonGrp(self.scapRootFld,e=True,text=sel[0])
        
    def loadClavRoot(self,*args):
        sel = mc.ls(sl=True)
        mc.textFieldButtonGrp(self.clavRootFld,e=True,text=sel[0])
        
    def loadCnt(self,*args):
        sel = mc.ls(sl=True)
        mc.textFieldButtonGrp(self.cntFld,e=True,text=sel[0])
        
    def loadShldr(self,*args):
        sel = mc.ls(sl=True)
        mc.textFieldButtonGrp(self.shldrFld,e=True,text=sel[0])
        
    def loadLeg(self,*args):
        sel = mc.ls(sl=True)
        mc.textFieldButtonGrp(self.legFld,e=True,text=sel[0])

        
