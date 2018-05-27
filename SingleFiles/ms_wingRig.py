"""
Copyright (c) 2009 Mauricio Santos
Name: ms_wingRig.py
Version: 1.0
Author: Mauricio Santos
Contact: mauricioptkvp@hotmail.com
Date Created: 10 Aug 2009
Last Modified: 5 Sep 2009
License: LGNU

Description:
    Build a wing rig. This script still requires alot of manual SDKing
    for the wing movements. Troublesome to scale
    
To do:
    Command line interface
    SDK Spread (Script? or manually?) Script may be too complex... Manual will lead to better results faster
    
Additional Notes:
    Spread is too uniform, and is more of a side to side than a spread...
     Maybe I should SDK the spread to fan out and collapse
     
Use: 

        Run script.
        Parent feathers to follow groups
        SDK groups
        SDK 'Display Handle' atts for feather geo
        

"""
import maya.cmds as mc 

class  ms_wingRig():
    """
     Store arguments passed from GUI or Command Line
     and build the Wing Rig.
    """
    def __init__(self,*args,**kwargs):
        #Initialize variables (Storing names)
        self.prefix = kwargs['prefix']
        self.baseCnt = kwargs['baseCnt']
        self.baseJnt = kwargs['baseJnt']
        self.spreadAxis = kwargs['spread']
        self.curlAxis = kwargs['curl']
        self.twistAxis = kwargs['twist']
        self.fSpreadAxis = kwargs['fSpread']
        self.fUpDnAxis = kwargs['fUpDn']
        self.fTwistAxis = kwargs['fTwist']
        self.polarity = kwargs['polarity']
        self.topPrimaryList = kwargs['topPrimaryList']
        self.btmPrimaryList = kwargs['btmPrimaryList']
        self.topSecondaryList = kwargs['topSecondaryList']
        self.btmSecondaryList = kwargs['btmSecondaryList']
        self.interiorList = kwargs['interiorList']
        self.tipList  = kwargs['tipList']
        
        mc.select(self.baseJnt,hi=True)
        self.jointChain = mc.ls(sl=True,fl=True)
        
        if(self.spreadAxis == 1):
            self.spreadAxis = "X"
        if(self.spreadAxis == 2):
            self.spreadAxis = "Y"
        if(self.spreadAxis == 3):
            self.spreadAxis = "Z"
            
        if(self.curlAxis == 1):
            self.curlAxis = "X"
        if(self.curlAxis == 2):
            self.curlAxis = "Y"
        if(self.curlAxis == 3):
            self.curlAxis = "Z"
            
        if(self.twistAxis == 1):
            self.twistAxis = "X"
        if(self.twistAxis == 2):
            self.twistAxis = "Y"
        if(self.twistAxis == 3):
            self.twistAxis = "Z"
            
        if(self.fSpreadAxis == 1):
            self.fSpreadAxis = "X"
        if(self.fSpreadAxis == 2):
            self.fSpreadAxis = "Y"
        if(self.fSpreadAxis == 3):
            self.fSpreadAxis = "Z"
            
        if(self.fUpDnAxis == 1):
            self.fUpDnAxis = "X"
        if(self.fUpDnAxis == 2):
            self.fUpDnAxis = "Y"
        if(self.fUpDnAxis == 3):
            self.fUpDnAxis = "Z"
            
        if(self.fTwistAxis == 1):
            self.fTwistAxis = "X"
        if(self.fTwistAxis == 2):
            self.fTwistAxis = "Y"
        if(self.fTwistAxis == 3):
            self.fTwistAxis = "Z"
            
        if(self.polarity == 1):
            self.polarity = "+"
        if(self.polarity == 2):
            self.polarity = "-"
        
        #Call function to build rig
        self.buildWing()   
        
    def buildWing(self,*args):
        """
         Given user values, build wing rig.
        """
        #--- Create Attributes on controller
        mc.addAttr(self.baseCnt,ln='wing_controls',k=True)
        mc.setAttr('%s.wing_controls' % self.baseCnt, lock=True)

        mc.addAttr(self.baseCnt,ln='wind',k=True)
        mc.setAttr('%s.wind' % self.baseCnt, lock=True)
        mc.addAttr(self.baseCnt,ln='frequency',k=True,dv=0,at='float',min=0)
        mc.addAttr(self.baseCnt,ln='amplitude',k=True,dv=0,at='float',min=0)
        
        mc.addAttr(self.baseCnt,ln='wing_joints',k=True)
        mc.setAttr('%s.wing_joints' % self.baseCnt, lock=True)
        
        mc.addAttr(self.baseCnt,ln='spread',k=True)
        mc.setAttr('%s.spread' % self.baseCnt, lock=True)
        mc.addAttr(self.baseCnt,ln='spSeg_1',k=True,dv=0,at='float')
        mc.addAttr(self.baseCnt,ln='spSeg_2',k=True,dv=0,at='float')
        mc.addAttr(self.baseCnt,ln='spSeg_3',k=True,dv=0,at='float')
        mc.addAttr(self.baseCnt,ln='spSeg_4',k=True,dv=0,at='float')
        
        mc.addAttr(self.baseCnt,ln='curl',k=True)
        mc.setAttr('%s.curl' % self.baseCnt, lock=True)
        mc.addAttr(self.baseCnt,ln='crSeg_1',k=True,dv=0,at='float')
        mc.addAttr(self.baseCnt,ln='crSeg_2',k=True,dv=0,at='float')
        mc.addAttr(self.baseCnt,ln='crSeg_3',k=True,dv=0,at='float')
        mc.addAttr(self.baseCnt,ln='crSeg_4',k=True,dv=0,at='float')
        
        mc.addAttr(self.baseCnt,ln='twist',k=True)
        mc.setAttr('%s.twist' % self.baseCnt, lock=True)
        mc.addAttr(self.baseCnt,ln='tSeg_1',k=True,dv=0,at='float')
        mc.addAttr(self.baseCnt,ln='tSeg_2',k=True,dv=0,at='float')
        mc.addAttr(self.baseCnt,ln='tSeg_3',k=True,dv=0,at='float')
        mc.addAttr(self.baseCnt,ln='tSeg_4',k=True,dv=0,at='float')
        
        mc.addAttr(self.baseCnt,ln='feathers',k=True)
        mc.setAttr('%s.feathers' % self.baseCnt, lock=True)
        
        mc.addAttr(self.baseCnt,ln='display_handles',k=True)
        mc.setAttr('%s.display_handles' % self.baseCnt, lock=True)
        mc.addAttr(self.baseCnt,ln='on_0ff',k=True, min=0, max=1,dv=0)
        
        mc.addAttr(self.baseCnt,ln='primaries',k=True)
        mc.setAttr('%s.primaries' % self.baseCnt, lock=True)
        mc.addAttr(self.baseCnt,ln='pSpread',k=True,dv=0,at='float')
        mc.addAttr(self.baseCnt,ln='pTopS2S',k=True,dv=0,at='float')
        mc.addAttr(self.baseCnt,ln='pBtmS2S',k=True,dv=0,at='float')
        mc.addAttr(self.baseCnt,ln='pTopUpDn',k=True,dv=0,at='float')
        mc.addAttr(self.baseCnt,ln='pBtmUpDn',k=True,dv=0,at='float')
        mc.addAttr(self.baseCnt,ln='pTopTwist',k=True,dv=0,at='float')
        mc.addAttr(self.baseCnt,ln='pBtmTwist',k=True,dv=0,at='float')
        
        mc.addAttr(self.baseCnt,ln='secondaries',k=True)
        mc.setAttr('%s.secondaries' % self.baseCnt, lock=True)
        mc.addAttr(self.baseCnt,ln='sSpread',k=True,dv=0,at='float')
        mc.addAttr(self.baseCnt,ln='sTopS2S',k=True,dv=0,at='float')
        mc.addAttr(self.baseCnt,ln='sBtmS2S',k=True,dv=0,at='float')
        mc.addAttr(self.baseCnt,ln='sTopUpDn',k=True,dv=0,at='float')
        mc.addAttr(self.baseCnt,ln='sTopUnderUpDn',k=True,dv=0,at='float')
        mc.addAttr(self.baseCnt,ln='sBtmUpDn',k=True,dv=0,at='float')
        mc.addAttr(self.baseCnt,ln='sTopTwist',k=True,dv=0,at='float')
        mc.addAttr(self.baseCnt,ln='sBtmTwist',k=True,dv=0,at='float')
        
        mc.addAttr(self.baseCnt,ln='interior',k=True)
        mc.setAttr('%s.interior' % self.baseCnt, lock=True)
        mc.addAttr(self.baseCnt,ln='int_S2S',k=True,dv=0,at='float')
        mc.addAttr(self.baseCnt,ln='int_upDn',k=True,dv=0,at='float')
        mc.addAttr(self.baseCnt,ln='int_twist',k=True,dv=0,at='float')
        
        mc.addAttr(self.baseCnt,ln='tip',k=True)
        mc.setAttr('%s.tip' % self.baseCnt, lock=True)
        mc.addAttr(self.baseCnt,ln='tip_S2S',k=True,dv=0,at='float')
        mc.addAttr(self.baseCnt,ln='tip_upDn',k=True,dv=0,at='float')
        mc.addAttr(self.baseCnt,ln='tip_twist',k=True,dv=0,at='float')
        
        #--- Setup 'Display Handle' SDK's
        driver = '%s.on_0ff' % self.baseCnt
        for each in self.topPrimaryList:
            mc.setDrivenKeyframe(each,cd=driver,dv=0,v=0,at='displayHandle')
            mc.setDrivenKeyframe(each,cd=driver,dv=1,v=1,at='displayHandle')
        for each in self.btmPrimaryList:
            mc.setDrivenKeyframe(each,cd=driver,dv=0,v=0,at='displayHandle')
            mc.setDrivenKeyframe(each,cd=driver,dv=1,v=1,at='displayHandle')
        for each in self.topSecondaryList:
            mc.setDrivenKeyframe(each,cd=driver,dv=0,v=0,at='displayHandle')
            mc.setDrivenKeyframe(each,cd=driver,dv=1,v=1,at='displayHandle')
        for each in self.btmSecondaryList:
            mc.setDrivenKeyframe(each,cd=driver,dv=0,v=0,at='displayHandle')
            mc.setDrivenKeyframe(each,cd=driver,dv=1,v=1,at='displayHandle')
        for each in self.interiorList:
            mc.setDrivenKeyframe(each,cd=driver,dv=0,v=0,at='displayHandle')
            mc.setDrivenKeyframe(each,cd=driver,dv=1,v=1,at='displayHandle')
        for each in self.tipList:
            mc.setDrivenKeyframe(each,cd=driver,dv=0,v=0,at='displayHandle')
            mc.setDrivenKeyframe(each,cd=driver,dv=1,v=1,at='displayHandle')
        
        #--- Setup Joints Spread
        #seg_1:
        mc.connectAttr('%s.spSeg_1'%self.baseCnt,'%s.rotate%s'%(self.jointChain[1],self.spreadAxis),f=True)
        #seg_2: 
        mc.connectAttr('%s.spSeg_2'%self.baseCnt,'%s.rotate%s'%(self.jointChain[2],self.spreadAxis),f=True)
        #seg_3:
        mc.connectAttr('%s.spSeg_3'%self.baseCnt,'%s.rotate%s'%(self.jointChain[3],self.spreadAxis),f=True)
        #seg_4: 
        mc.connectAttr('%s.spSeg_4'%self.baseCnt,'%s.rotate%s'%(self.jointChain[4],self.spreadAxis),f=True)
  
        #--- Setup Joints Curl
        mc.connectAttr('%s.crSeg_1'%self.baseCnt,'%s.rotate%s'%(self.jointChain[1],self.curlAxis),f=True) 
        mc.connectAttr('%s.crSeg_2'%self.baseCnt,'%s.rotate%s'%(self.jointChain[2],self.curlAxis),f=True) 
        mc.connectAttr('%s.crSeg_3'%self.baseCnt,'%s.rotate%s'%(self.jointChain[3],self.curlAxis),f=True) 
        mc.connectAttr('%s.crSeg_4'%self.baseCnt,'%s.rotate%s'%(self.jointChain[4],self.curlAxis),f=True) 
        
        #--- Setup Joints Twist
        mc.connectAttr('%s.tSeg_1'%self.baseCnt,'%s.rotate%s'%(self.jointChain[1],self.twistAxis),f=True)
        mc.connectAttr('%s.tSeg_2'%self.baseCnt,'%s.rotate%s'%(self.jointChain[2],self.twistAxis),f=True)
        mc.connectAttr('%s.tSeg_3'%self.baseCnt,'%s.rotate%s'%(self.jointChain[3],self.twistAxis),f=True) 
        mc.connectAttr('%s.tSeg_4'%self.baseCnt,'%s.rotate%s'%(self.jointChain[4],self.twistAxis),f=True)
        
        #--- Setup Top Primary Feathers Spread/Curl/Twist
        #Store topNodes of feathers geo
        topPrimaryTopNodes = []
        try:
            for each in self.topPrimaryList:
                temp = mc.listRelatives(each,parent=True)
                temp = mc.listRelatives(temp,parent=True)
                topPrimaryTopNodes.append(temp[0])
        except:
            print 'Error: Primary feathers list is empty.'
        
        #Store midNodes of feathers geo
        topPrimaryMidNodes = []
        try:
            for each in self.topPrimaryList:
                temp = mc.listRelatives(each,parent=True)
                topPrimaryMidNodes.append(temp[0])
        except:
            print 'Error: Primary feathers list is empty.'
        
        #Connect mid nodes to attributes on control object
        for each in topPrimaryMidNodes:
            mc.connectAttr('%s.pTopS2S'%self.baseCnt,'%s.rotate%s'%(each,self.fSpreadAxis),f=True)
            mc.connectAttr('%s.pTopUpDn'%self.baseCnt,'%s.rotate%s'%(each,self.fUpDnAxis),f=True)
            mc.connectAttr('%s.pTopTwist'%self.baseCnt,'%s.rotate%s'%(each,self.fTwistAxis),f=True)
        
        #--- Setup Bottom Primary Feathers Spread/Curl/Twist 
        #Store btmNodes of feathers geo
        btmPrimaryTopNodes = []
        try:
            for each in self.btmPrimaryList:
                temp = mc.listRelatives(each,parent=True)
                temp = mc.listRelatives(temp,parent=True)
                btmPrimaryTopNodes.append(temp[0])
        except:
            print 'Error: Primary feathers list is empty.'
        
        #Store midNodes of feathers geo
        btmPrimaryMidNodes = []
        try:
            for each in self.btmPrimaryList:
                temp = mc.listRelatives(each,parent=True)
                btmPrimaryMidNodes.append(temp[0])
        except:
            print 'Error: Primary feathers list is empty.'
            
        #Connect mid nodes to attributes on control object
        for each in btmPrimaryMidNodes:
            mc.connectAttr('%s.pBtmS2S'%self.baseCnt,'%s.rotate%s'%(each,self.fSpreadAxis),f=True)
            mc.connectAttr('%s.pBtmUpDn'%self.baseCnt,'%s.rotate%s'%(each,self.fUpDnAxis),f=True)
            mc.connectAttr('%s.pBtmTwist'%self.baseCnt,'%s.rotate%s'%(each,self.fTwistAxis),f=True)
        
        
        #--- Setup Top Secondary Feathers Spread/Curl/Twist
        #Store btmNodes of feathers geo
        topSecondaryTopNodes = []
        try:
            for each in self.topSecondaryList:
                temp = mc.listRelatives(each,parent=True)
                temp = mc.listRelatives(temp,parent=True)
                topSecondaryTopNodes.append(temp[0])
        except:
            print 'Error: Secondary feathers list is empty.'
        
        #Store midNodes of feathers geo
        topSecondaryMidNodes = []
        try:
            for each in self.topSecondaryList:
                temp = mc.listRelatives(each,parent=True)
                topSecondaryMidNodes.append(temp[0])
        except:
            print 'Error: Secondary feathers list is empty.'
        
        #Connect mid nodes to attributes on control object
        for each in topSecondaryMidNodes:
            if '_btm_' in each:
                mc.connectAttr('%s.sTopS2S'%self.baseCnt,'%s.rotate%s'%(each,self.fSpreadAxis),f=True)
                mc.connectAttr('%s.sTopUnderUpDn'%self.baseCnt,'%s.rotate%s'%(each,self.fUpDnAxis),f=True)
                mc.connectAttr('%s.sTopTwist'%self.baseCnt,'%s.rotate%s'%(each,self.fTwistAxis),f=True)
            else:
                mc.connectAttr('%s.sTopS2S'%self.baseCnt,'%s.rotate%s'%(each,self.fSpreadAxis),f=True)
                mc.connectAttr('%s.sTopUpDn'%self.baseCnt,'%s.rotate%s'%(each,self.fUpDnAxis),f=True)
                mc.connectAttr('%s.sTopTwist'%self.baseCnt,'%s.rotate%s'%(each,self.fTwistAxis),f=True)
            
        #--- Setup Bottom Secondary Feathers Spread/Curl/Twist
        #Store btmNodes of feathers geo
        btmSecondaryTopNodes = []
        try:
            for each in self.btmSecondaryList:
                temp = mc.listRelatives(each,parent=True)
                temp = mc.listRelatives(temp,parent=True)
                btmSecondaryTopNodes.append(temp[0])
        except:
            print 'Error: Secondary feathers list is empty.'
        
        #Store midNodes of feathers geo
        btmSecondaryMidNodes = []
        try:
            for each in self.btmSecondaryList:
                temp = mc.listRelatives(each,parent=True)
                btmSecondaryMidNodes.append(temp[0])
        except:
            print 'Error: Secondary feathers list is empty.'
            
        #Connect mid nodes to attributes on control object
        for each in btmSecondaryMidNodes:
            mc.connectAttr('%s.sBtmS2S'%self.baseCnt,'%s.rotate%s'%(each,self.fSpreadAxis),f=True)
            mc.connectAttr('%s.sBtmUpDn'%self.baseCnt,'%s.rotate%s'%(each,self.fUpDnAxis),f=True)
            mc.connectAttr('%s.sBtmTwist'%self.baseCnt,'%s.rotate%s'%(each,self.fTwistAxis),f=True)         
        
        #--- Setup Interior UpDown/ Side to Side / Twist
        #Store btmNodes of feathers geo
        interiorTopNodes = []
        try:
            for each in self.interiorList:
                temp = mc.listRelatives(each,parent=True)
                temp = mc.listRelatives(temp,parent=True)
                interiorTopNodes.append(temp[0])
        except:
            print 'Error: Interior feathers list is empty.'
        
        #Store midNodes of feathers geo
        interiorMidNodes = []
        try:
            for each in self.interiorList: 
                temp = mc.listRelatives(each,parent=True)
                interiorMidNodes.append(temp[0])
        except:
            print 'Error: Interior feathers list is empty.'
            
        #Connect mid nodes to attributes on control object
        for each in interiorMidNodes:
            mc.connectAttr('%s.int_S2S'%self.baseCnt,'%s.rotate%s'%(each,self.fSpreadAxis),f=True)
            mc.connectAttr('%s.int_upDn'%self.baseCnt,'%s.rotate%s'%(each,self.fUpDnAxis),f=True)
            mc.connectAttr('%s.int_twist'%self.baseCnt,'%s.rotate%s'%(each,self.fTwistAxis),f=True) 
        
        
        #--- Setup Tip UpDown/ Side to Side / Twist
        #Store btmNodes of feathers geo
        tipTopNodes = []
        try:
            for each in self.tipList:
                temp = mc.listRelatives(each,parent=True)
                temp = mc.listRelatives(temp,parent=True)
                tipTopNodes.append(temp[0])
        except:
            print 'Error: Tip feathers list is empty.'
        
        #Store midNodes of feathers geo
        tipMidNodes = []
        try:
            for each in self.tipList: 
                temp = mc.listRelatives(each,parent=True)
                tipMidNodes.append(temp[0])
        except:
            print 'Error: Tip feathers list is empty.'
            
        #Connect mid nodes to attributes on control object
        for each in tipMidNodes:
            mc.connectAttr('%s.tip_S2S'%self.baseCnt,'%s.rotate%s'%(each,self.fSpreadAxis),f=True)
            mc.connectAttr('%s.tip_upDn'%self.baseCnt,'%s.rotate%s'%(each,self.fUpDnAxis),f=True)
            mc.connectAttr('%s.tip_twist'%self.baseCnt,'%s.rotate%s'%(each,self.fTwistAxis),f=True)        
        
        #--- Setup Wind
        # Wind expression setup
        expName = '%s_wingNoiseExp' % self.prefix
        expression = []
        expression = '////Setup %s wing rig Noise expression  \n'
        expression += '$amp = %s.amplitude;\n' %self.baseCnt
        expression += '$freq = %s.frequency;\n'%self.baseCnt
        
        # Get third parent up the hierarchy for each feather and place the expression on it, freeing the
        # geometry so the animator can key it directly.
        topPrimaryList_secondParent = [] 
        for each in self.topPrimaryList:
            temp1 = mc.listRelatives(each,parent=True) 
            temp2 = mc.listRelatives(temp1,parent=True)
            topPrimaryList_secondParent.append( temp2 )
            
        btmPrimaryList_secondParent = [] 
        for each in self.btmPrimaryList:
            temp1 = mc.listRelatives(each,parent=True) 
            temp2 = mc.listRelatives(temp1,parent=True)
            btmPrimaryList_secondParent.append( temp2 )
            
        topSecondaryList_secondParent = [] 
        for each in self.topSecondaryList:
            temp1 = mc.listRelatives(each,parent=True) 
            temp2 = mc.listRelatives(temp1,parent=True)
            topSecondaryList_secondParent.append( temp2 )
            
        btmSecondaryList_secondParent = []
        for each in self.btmSecondaryList:
            temp1 = mc.listRelatives(each,parent=True) 
            temp2 = mc.listRelatives(temp1,parent=True)
            btmSecondaryList_secondParent.append( temp2 )
            
        interiorList_secondParent = []
        for each in self.interiorList:
            temp1 = mc.listRelatives(each,parent=True)
            temp2 = mc.listRelatives(temp1,parent=True)
            interiorList_secondParent.append( temp2 )
            
        tipList_secondParent = [] 
        for each in self.tipList:
            temp1 = mc.listRelatives(each,parent=True) 
            temp2 = mc.listRelatives(temp1,parent=True)
            tipList_secondParent.append( temp2 )
            
        
        for each in topPrimaryList_secondParent:
            expression += '%s.rotate%s = rand(sin($freq * time)) * $amp ;\n' % (each[0], self.fUpDnAxis )
        for each in btmPrimaryList_secondParent:
            expression += '%s.rotate%s = rand(sin($freq * time)) * $amp ;\n' % (each[0], self.fUpDnAxis )
        for each in topSecondaryList_secondParent:
            expression += '%s.rotate%s = rand(sin($freq * time)) * $amp ;\n' % (each[0], self.fUpDnAxis ) 
        for each in btmSecondaryList_secondParent:
            expression += '%s.rotate%s = rand(sin($freq * time)) * $amp ;\n' % (each[0], self.fUpDnAxis ) 
        for each in interiorList_secondParent:
            expression += '%s.rotate%s = rand(sin($freq * time)) * $amp ;\n' % (each[0], self.fUpDnAxis )
        for each in tipList_secondParent:
            expression += '%s.rotate%s = rand(sin($freq * time)) * $amp ;\n' % (each[0], self.fUpDnAxis ) 
                              
        mc.expression( s=expression, n=expName )
                  
        
        
        
        
        
        
        
        
        
        
        
        