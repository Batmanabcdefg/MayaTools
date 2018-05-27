"""
Copyright (c) 2009 Mauricio Santos
Name: ms_wingRigGUI.py
Version: 1.0
Author: Mauricio Santos
Contact: mauricioptkvp@hotmail.com
Date Created: 10 Aug 2009
Last Modified: 3 Sep 2009
License: LGNU

Description:
    Requires ms_wingRig.py
    This is the GUI for ms_wingRig.py
    
To do:
    

Additional Notes:
 

"""
import maya.cmds as mc 
import ms_wingRig as wr

class  ms_wingRigGUI():
    def __init__(self):
        if(mc.window( 'wingRigGUIWin',exists=True )):
           mc.deleteUI( 'wingRigGUIWin',window=True)
        
        mc.window('wingRigGUIWin',rtf=True, title = "Wing Rig v1.0", menuBar=True, widthHeight=(400, 220))

        mc.menu( label='Help', tearOff=True )
        mc.menuItem( label='Pre-Requisites',c=self.preRequisiteWin )
        mc.menuItem( label='Instructions',c=self.instructionsWin )
        mc.menuItem( label='Definitions',c=self.definitionsWin )

        mc.scrollLayout(h=200,w=400,horizontalScrollBarThickness=16,verticalScrollBarThickness=16)
        mc.columnLayout()
        
        self.prefixFld = mc.textFieldGrp(label='Prefix',text='l_wing_')
        self.baseCntFld = mc.textFieldButtonGrp(label='Wing Base Control',bl='Load',bc=self.loadBaseCnt)
        self.clavJntFld = mc.textFieldButtonGrp(label='Wing Clavicle Joint',bl='Load',bc=self.loadClavJnt)
        
        self.spreadAxisFld = mc.radioButtonGrp(label='Spread Axis',nrb=3,labelArray3=('X','Y','Z'),sl=2)
        self.curlAxisFld = mc.radioButtonGrp(label='Curl Axis',nrb=3,labelArray3=('X','Y','Z'),sl=3)
        self.twistAxisFld = mc.radioButtonGrp(label='Twist Axis',nrb=3,labelArray3=('X','Y','Z'),sl=1)
        mc.separator(w=420)
        self.fSpreadAxisFld = mc.radioButtonGrp(label='Feather Spread Axis',nrb=3,labelArray3=('X','Y','Z'),sl=2)
        self.fUpDnAxisFld = mc.radioButtonGrp(label='Feather Up//Down Axis',nrb=3,labelArray3=('X','Y','Z'),sl=1)
        self.fTwistAxisFld = mc.radioButtonGrp(label='Feather Twist Axis',nrb=3,labelArray3=('X','Y','Z'),sl=3)
        mc.separator(w=420)
        self.buildPolarityFld = mc.radioButtonGrp(label='Build Polarity',nrb=2,labelArray2=('+','-'),sl=1)
        
        #--- GUI: Primary Feather Lists
        mc.frameLayout(label='Primary Feathers', cl=True,cll=True,fn='boldLabelFont')
        mc.columnLayout()
        
        mc.rowLayout(nc=3)
        mc.text("Top / Short")
        mc.text( " " )
        mc.text("Bottom / Long")
        mc.setParent("..")        

        mc.rowLayout(nc=3)
        self.topPrimaryList = mc.textScrollList(numberOfRows=25, w=200, ams = True)
        mc.text( " " )
        self.btmPrimaryList = mc.textScrollList(numberOfRows=25, w=200, ams = True)
        mc.setParent("..")
            
        mc.rowLayout(nc=3)
        mc.button(label="          Load ", c = self.loadTopPrimaryList,w=100)
        mc.text( " " )
        mc.button(label="          Load ", c = self.loadBtmPrimaryList,w=100)
        mc.setParent("..")
    
        mc.rowLayout(nc=3)
        mc.button(label="          Reset", c = self.resetTopPrimary,w=100)    
        mc.text(" ")
        mc.button(label="          Reset", c = self.resetBtmPrimary,w=100)
        mc.setParent("..")
               
        mc.rowLayout(nc=3)
        mc.button(label="        Remove", c = self.removeTopPrimary,w=100)    
        mc.text(" ")
        mc.button(label="        Remove", c = self.removeBtmPrimary,w=100)
        mc.setParent("..")     
        
        mc.rowLayout(nc=3)
        mc.button(label="        List Size", c = self.topPrimarySize,w=100)    
        mc.text(" ")
        mc.button(label="        List Size", c = self.btmPrimarySize,w=100)
        mc.setParent("..")           

        mc.setParent("..")
        mc.setParent("..")   
        
        #--- GUI: Secondary Feather Lists
        mc.frameLayout(label='Secondary Feathers', cl=True,cll=True,fn='boldLabelFont')
        mc.columnLayout()
        
        mc.rowLayout(nc=3)
        mc.text("Top / Short")
        mc.text( " " )
        mc.text("Bottom / Long")
        mc.setParent("..")        
        
        mc.rowLayout(nc=3)
        self.topSecondaryList = mc.textScrollList(numberOfRows=25, w=200, ams = True)
        mc.text( " " )
        self.btmSecondaryList = mc.textScrollList(numberOfRows=25, w=200, ams = True)
        mc.setParent("..")
            
        mc.rowLayout(nc=3)
        mc.button(label="          Load ", c = self.loadTopSecondaryList,w=100)
        mc.text( " " )
        mc.button(label="          Load ", c = self.loadBtmSecondaryList,w=100)
        mc.setParent("..")
    
        mc.rowLayout(nc=3)
        mc.button(label="          Reset", c = self.resetTopSecondary,w=100)    
        mc.text(" ")
        mc.button(label="          Reset", c = self.resetBtmSecondary,w=100)
        mc.setParent("..")
               
        mc.rowLayout(nc=3)
        mc.button(label="        Remove", c = self.removeTopSecondary,w=100)    
        mc.text(" ")
        mc.button(label="        Remove", c = self.removeBtmSecondary,w=100)
        mc.setParent("..")     
        
        mc.rowLayout(nc=3)
        mc.button(label="        List Size", c = self.topSecondarySize,w=100)    
        mc.text(" ")
        mc.button(label="        List Size", c = self.btmSecondarySize,w=100)
        mc.setParent("..")           

        mc.setParent("..")
        mc.setParent("..")
        
        #--- GUI: Interior & Tip Lists
        mc.frameLayout(label='Interior & Tip Feathers ', cl=True,cll=True,fn='boldLabelFont')
        mc.columnLayout()
        
        mc.rowLayout(nc=3)
        mc.text("Interior")
        mc.text( " " )
        mc.text("Tip")
        mc.setParent("..")        

        mc.rowLayout(nc=3)
        self.interiorList = mc.textScrollList(numberOfRows=25, w=200, ams = True)
        mc.text( " " )
        self.tipList = mc.textScrollList(numberOfRows=25, w=200, ams = True)
        mc.setParent("..")
            
        mc.rowLayout(nc=3)
        mc.button(label="          Load ", c = self.loadInteriorList,w=100)
        mc.text( " " )
        mc.button(label="          Load ", c = self.loadTipList,w=100)
        mc.setParent("..")
    
        mc.rowLayout(nc=3)
        mc.button(label="          Reset", c = self.resetInterior,w=100)    
        mc.text(" ")
        mc.button(label="          Reset", c = self.resetTip,w=100)
        mc.setParent("..")
               
        mc.rowLayout(nc=3)
        mc.button(label="        Remove", c = self.removeInterior,w=100)    
        mc.text(" ")
        mc.button(label="        Remove", c = self.removeTip,w=100)
        mc.setParent("..")     
        
        mc.rowLayout(nc=3)
        mc.button(label="        List Size", c = self.interiorSize,w=100)    
        mc.text(" ")
        mc.button(label="        List Size", c = self.tipSize,w=100)
        mc.setParent("..")           

        mc.setParent("..")
        mc.setParent("..")

        mc.text(' ')
        mc.separator(w=400)
        mc.rowLayout(nc=2,cw2=(130,100))
        mc.text(" ")
        mc.button(label="     Build Rig  ",c=self.wingRig,w=100,bgc=(0,1,0) )
        mc.setParent("..")
        
        mc.setParent('..') #End main Scroll List

        mc.showWindow('wingRigGUIWin')
        
    #--- Call: ms_wingRig.py
    def wingRig(self,*args):
        """
         Pass arguments to wingRig.py
        """
        #Store values
        prefix = mc.textFieldGrp(self.prefixFld,query=True,text=True)
        baseCnt = mc.textFieldButtonGrp(self.baseCntFld,query=True,text=True)
        clavJnt = mc.textFieldButtonGrp(self.clavJntFld,query=True,text=True)
        
        spread = mc.radioButtonGrp(self.spreadAxisFld,query=True,sl=True)
        curl = mc.radioButtonGrp(self.curlAxisFld,query=True,sl=True)
        twist = mc.radioButtonGrp(self.twistAxisFld,query=True,sl=True)
        fSpread = mc.radioButtonGrp(self.fSpreadAxisFld,query=True,sl=True)
        fUpDn = mc.radioButtonGrp(self.fUpDnAxisFld,query=True,sl=True)
        fTwist = mc.radioButtonGrp(self.fTwistAxisFld,query=True,sl=True)
        polarity = mc.radioButtonGrp(self.buildPolarityFld,query=True,sl=True)
        
        topPrimaryList = mc.textScrollList(self.topPrimaryList,query=True,ai=True)
        btmPrimaryList = mc.textScrollList(self.btmPrimaryList,query=True,ai=True)
        topSecondaryList = mc.textScrollList(self.topSecondaryList,query=True,ai=True)
        btmSecondaryList = mc.textScrollList(self.btmSecondaryList,query=True,ai=True)
        interiorList = mc.textScrollList(self.interiorList,query=True,ai=True)
        tipList = mc.textScrollList(self.tipList,query=True,ai=True)
        
        #Create dictionary to pass with apply()
        arguments = { 'prefix':prefix,
                      'baseCnt':baseCnt,
                      'baseJnt':clavJnt,
                      'spread':spread,
                      'curl':curl,
                      'twist':twist,
                      'fSpread':fSpread,
                      'fUpDn':fUpDn,
                      'fTwist':fTwist,
                      'polarity':polarity,
                      'topPrimaryList':topPrimaryList,
                      'btmPrimaryList':btmPrimaryList,
                      'topSecondaryList':topSecondaryList,
                      'btmSecondaryList':btmSecondaryList,
                      'interiorList':interiorList,
                      'tipList':tipList
                    }
        pargs=(1,2)    #No purpose besides satisfying the required list argument for the apply call.
                  
        #Call script, passing dictionary as an argument using apply()
        apply(wr.ms_wingRig,pargs,arguments)
 
    #--- Help Menu Windows
    def preRequisiteWin(self,*args):
        if(mc.window( 'preRequisiteWin',exists=True )):
           mc.deleteUI( 'preRequisiteWin',window=True)
        mc.window('preRequisiteWin',rtf=True, title = "Prerequisites", menuBar=True, widthHeight=(300, 200))
        
        mc.columnLayout()
        mc.text(' JOINTS: ')
        mc.text(' Hierarchy: ')
        mc.text('    baseJnt --- wing1Jnt --- wing2Jnt --- wing3Jnt --- wingEndJnt')
        mc.text(' Each wing joint can have a child joint to')
        mc.text(' use to parent the feathers to, and SDK as needed.')
        mc.text('------------------------------------------------------------------')
        mc.text(' FEATHERS: ')
        mc.text(' Each feather should have two groups above it where the pivot ')
        mc.text(' and the orientation are the same as the pivot of the geometry.')
        mc.text(' See "Definitions" for more information on required feathers.' )
        
        mc.showWindow('preRequisiteWin')
    
    def instructionsWin(self,*args):
        if(mc.window( 'instructionsWin',exists=True )):
           mc.deleteUI( 'instructionsWin',window=True)
        mc.window('instructionsWin',rtf=True, title = "Instructions", menuBar=True, widthHeight=(300, 200)) 
        
        mc.columnLayout()
        mc.text(' Load the required fields by selecting the geometry for the feathers, ')
        mc.text(' curve for base control, base joint and select the options')
        mc.text(' that relate to the desired rotational behavior (Spread/Curl). ')
        mc.text(' that the wing will follow.')
        mc.text(' ')
        mc.text(' Select the appropriate polarity that the wing is in.')
        
        mc.showWindow('instructionsWin')
        
    def definitionsWin(self,*args):
        if(mc.window( 'definitionsWin',exists=True )):
           mc.deleteUI( 'definitionsWin',window=True)
        mc.window('definitionsWin',rtf=True, title = "Definitions", menuBar=True, widthHeight=(300, 200)) 
        
        mc.columnLayout()
        mc.text(' Base Control: Control to rotate/position wing from insertion point. ')
        mc.text(' Clav Joint: Clavicle, child of shoulders joint / control.')
        mc.text(' ')
        mc.text(' Joints Spread Axis: Axis of joint chain that the wings spread/collapse along.')
        mc.text(' Joints Curl Axis: Axis of joints that the wings curl along. (upward, downward with wing extended)')
        mc.text(' Joints Twist Axis: Axis of joints that they twist along.')
        mc.text(' Feather Spread Axis: Axis of feather geo that it rotates side to side on it\'s pivot.')
        mc.text(' Feather Up/Down Axis: Axis of feather geo that tilts them upward / downward from their pivots.')
        mc.text(' Feather Twist Axis: Axis of feather geo that they twist around the center line.')
        mc.text(' Build Polarity: Polarity of the quadrant that the rig will be built in.')
        mc.text(' ')
        mc.text(' Primary Feathers (Top): Group of feathers towards tip of wing, closest to wing joints. ')
        mc.text(' Primary Feathers (Bottom): Group of feathers towards tip of wing, farthest from wing joints. ')
        mc.text(' Secondary Feathers (Top): Group of feathers closest to body, closest to wing joints. ')
        mc.text(' Secondary Feathers (Bottom): Group of feathers closest to body, farthest from wing joints. ')
        mc.text(' ')
        mc.text(' Interior Feathers: Feathers between wing feathers and body.')
        mc.text(' Tip Feathers: Feathers at tip of wing joints.')
        
        mc.showWindow('definitionsWin')
        
    #--- Base Cnt / Jnt load functions
    def loadBaseCnt(self,*args):
        sel = mc.ls(sl=True,fl=True)
        mc.textFieldButtonGrp(self.baseCntFld,e=True,text=sel[0])
        
    def loadClavJnt(self,*args):
        sel = mc.ls(sl=True,fl=True,exactType='joint')
        mc.textFieldButtonGrp(self.clavJntFld,e=True,text=sel[0])

    #--- Primary List Buttons
    def topPrimarySize(self,*args):  
        num = 0  
        items = mc.textScrollList(self.topPrimaryList,q=True,ai=True)
        try:
            num = len(items)
        except:
            pass
        print "There are %i items in the top Primary Feathers List." % num
        
    def btmPrimarySize(self,*args):   
        num = 0
        items = mc.textScrollList(self.btmPrimaryList,q=True,ai=True)
        try:
            num = len(items)
        except:
            pass
        print "There are %i items in the bottom Primary List." % num        
     
    def resetTopPrimary(self,*args):    
        mc.textScrollList(self.topPrimaryList,e=True,ra=True)
        
    def resetBtmPrimary(self,*args):    
        mc.textScrollList(self.btmPrimaryList,e=True,ra=True)        
        
    def loadTopPrimaryList(self,*args):
        sources = mc.ls(sl=True,fl=True)
        for each in sources:
                mc.textScrollList(self.topPrimaryList,e=True,a=each)
                
    def loadBtmPrimaryList(self,*args):
        targets = mc.ls(sl=True,fl=True)
        for each in targets:
                mc.textScrollList(self.btmPrimaryList,e=True,a=each)  
                
    def removeTopPrimary(self,*args):
        selected = mc.textScrollList(self.topPrimaryList,q=True,si=True)    
        for each in selected:
            mc.textScrollList(self.topPrimaryList,e=True,ri=each)  
            
    def removeBtmPrimary(self,*args):
        selected = mc.textScrollList(self.btmPrimaryList,q=True,si=True)    
        for each in selected:
            mc.textScrollList(self.btmPrimaryList,e=True,ri=each)
            
    #--- Secondary List Buttons
    def topSecondarySize(self,*args):  
        num = 0  
        items = mc.textScrollList(self.topSecondaryList,q=True,ai=True)
        try:
            num = len(items)
        except:
            pass
        print "There are %i items in the top Secondary Feathers List." % num
        
    def btmSecondarySize(self,*args):   
        num = 0
        items = mc.textScrollList(self.btmSecondaryList,q=True,ai=True)
        try:
            num = len(items)
        except:
            pass
        print "There are %i items in the bottom Secondary List." % num        
     
    def resetTopSecondary(self,*args):    
        mc.textScrollList(self.topSecondaryList,e=True,ra=True)
        
    def resetBtmSecondary(self,*args):    
        mc.textScrollList(self.btmSecondaryList,e=True,ra=True)        
        
    def loadTopSecondaryList(self,*args):
        sources = mc.ls(sl=True,fl=True)
        for each in sources:
                mc.textScrollList(self.topSecondaryList,e=True,a=each)
                
    def loadBtmSecondaryList(self,*args):
        targets = mc.ls(sl=True,fl=True)
        for each in targets:
                mc.textScrollList(self.btmSecondaryList,e=True,a=each)  
                
    def removeTopSecondary(self,*args):
        selected = mc.textScrollList(self.topSecondaryList,q=True,si=True)    
        for each in selected:
            mc.textScrollList(self.topSecondaryList,e=True,ri=each)  
            
    def removeBtmSecondary(self,*args):
        selected = mc.textScrollList(self.btmSecondaryList,q=True,si=True)    
        for each in selected:
            mc.textScrollList(self.btmSecondaryList,e=True,ri=each) 
            
    #--- Interior / Tip List Buttons
    def interiorSize(self,*args):  
        num = 0  
        items = mc.textScrollList(self.interiorList,q=True,ai=True)
        try:
            num = len(items)
        except:
            pass
        print "There are %i items in the Interior List." % num
        
    def tipSize(self,*args):   
        num = 0
        items = mc.textScrollList(self.tipList,q=True,ai=True)
        try:
            num = len(items)
        except:
            pass
        print "There are %i items in the Tip List." % num        
     
    def resetInterior(self,*args):    
        mc.textScrollList(self.interiorList,e=True,ra=True)
        
    def resetTip(self,*args):    
        mc.textScrollList(self.tipList,e=True,ra=True)        
        
    def loadInteriorList(self,*args):
        sources = mc.ls(sl=True,fl=True)
        for each in sources:
                mc.textScrollList(self.interiorList,e=True,a=each)
                
    def loadTipList(self,*args):
        targets = mc.ls(sl=True,fl=True)
        for each in targets:
                mc.textScrollList(self.tipList,e=True,a=each)  
                
    def removeInterior(self,*args):
        selected = mc.textScrollList(self.interiorList,q=True,si=True)    
        for each in selected:
            mc.textScrollList(self.interiorList,e=True,ri=each)  
            
    def removeTip(self,*args):
        selected = mc.textScrollList(self.tipList,q=True,si=True)    
        for each in selected:
            mc.textScrollList(self.tipList,e=True,ri=each)                                   
                
    