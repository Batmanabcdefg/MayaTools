"""
Copyright (c) 2009 Mauricio Santos
Name: ms_correctiveBS.py
Version: 1.0
Author: Mauricio Santos
Contact: mauricioptkvp@hotmail.com
Date Created: 17 Sep 2008
Last Modified: 18 Aug 2009
License: LGNU
Description: Corrective Blend Shape Creator!

To do: 

Additional Notes:
	Special thanks to Carlos Joy who came up with initial concept and additional
        ideas during development.


    Procedure:
        Amended Flow:
            User selects mesh @ broken pose
            -List history (Type = deformers)
            -for each deformer, if env == 0, set envelope att to 0, store att
            -Duplicate mesh with 0 influences: Neutral mesh
            -Turn envelopes back on for stored atts
            -duplicate mesh at current pose
            -hide base mesh
            
            -Prompt user to correct mesh
            
            -Continue with existing script
        
        
        Get Neutral Mesh
        Duplicate Mesh at broken pose (BP Mesh)
        Apply N.Mesh as BS to BP Mesh (Weight: 0)
        Sculpt changes 
        set weight to 1
        Delete history
        
    #Updates

    v1.1: Modified to add nonLinear node types.
	1 May 2009: wrapped geo visibility switching into try/except
"""    
    
    
#    New Process:
#        Duplicate three times:
            
#         ModifyMesh = Mesh to be modified by user.
#         BPNeutral = Broken Pose neutral
#         TPose = Mesh at T-Pose
            
#         Apply ModifyMesh as FOC BS to BPNeutral. Set to 1 (ModifyMeshBS)
#        Apply TPose as Parallel to BPNeutal. (TPoseBS)

#        When user hits continue, set TposeBS to 1, add to user selected BSNode or Default
#        Delete: ModifyMesh, TPose


        


import maya.cmds as mc
import maya.mel as mel


class ms_correctiveBS():
    def __init__(self):
        
        #Make sure geometry is selected, to be able to populate blend shape selection list.
        self.geo = mc.ls(sl=True,fl=True)
        temp = len(self.geo)
        if(temp==0):
            if(mc.window( 'cbsWin',exists=True )):
                mc.deleteUI( 'cbsWin',window=True)
            mc.window('cbsWin',rtf=True, title = "Corrective Blend Shape v1.0",w=320)
            
            mc.columnLayout()
            mc.text("Please select a skinned mesh and then re-run the script.")
            mc.rowLayout(nc=2)
            mc.text(" ")
            mc.button(l="           Ok",c=self.quickClose,w=100)
            mc.setParent("..")
            
            mc.showWindow('cbsWin')
            #Exit if no mesh selected after prompting user.
            return None
        
        #Get Blendshape List content for given mesh
        #First, initialize values
        paraBlender = ""
        bsList = ""
        bsListSize = 0
        
        blendShapesList = [] #List of all blend shapes
        temp = mc.listHistory(self.geo)
        for each in temp:
            type = mc.nodeType(each)    #Checks each item returned by listHistory to seeif it's a blendShape
            if(type == 'blendShape'):
                blendShapesList.append(each)
        
        try:        
            blendShapesListSize = len(blendShapesList)
            #bsList = mc.listConnections(paraBlender,type='blendShape')
            #bsListSize = len(bsList)
        except:
            pass
        
        
        #Main Window
        if(mc.window( 'cbsWin',exists=True )):
            mc.deleteUI( 'cbsWin',window=True)
            
        mc.window('cbsWin',rtf=True, title = "Corrective Blend Shape v1.0",w=320)   
        
        mc.columnLayout()
        
        mc.text("\n                                      Select posed mesh, hit continue.\n")
        
        self.bsNameField = mc.textFieldGrp(label="CBS Name:")
        mc.rowLayout(nc=2,cw2=(180,100))
        mc.text("            BS node to add CBS to:")
        self.bsNodeMenu = mc.optionMenu()
        #Populate menu
        mc.menuItem(label='Default')
        if(blendShapesListSize):
            for each in blendShapesList:
                mc.menuItem(label=each)
        mc.setParent( ".." )
        
        mc.rowLayout( nc=3,cw3=(80,80,100) )
        mc.text(" ")
        mc.text(" ")
        mc.button(label="      -=Continue=-", c=self.cbs, w=100 )
 
        mc.showWindow( 'cbsWin' )
        
    def cbs(self,*args):

        #Get base mesh and duplicate and name
        self.name = mc.textFieldGrp(self.bsNameField,q=True,text=True)
        self.baseMesh = mc.ls(sl=True)
        self.bpModifyMesh = mc.duplicate(self.baseMesh)
        self.bpNeutralMesh = mc.duplicate(self.baseMesh)
        
        #Lets check and see if ":" are in the base mesh name. If so,
        #split it, and only use the name portion to name the scriptBSnode
        if(":" in self.baseMesh[0]):
            tempName = self.baseMesh[0].split(":")
            self.scriptBSnode = "CBS_" +  tempName[1]               #add mesh name here to make unique
        else:
            self.scriptBSnode = "CBS_" +  self.baseMesh[0]
        
        #Rename duplicate to user name, if it exists
        temp = len(self.name)
        if(temp):
            self.bpModifyMesh = mc.rename(self.bpModifyMesh, ("Modifiy_" + self.name) )
            self.bpNeutralMesh = mc.rename(self.bpNeutralMesh, ("Neutral_" + self.name ) )

        self.bsNode = mc.optionMenu(self.bsNodeMenu,q=True,v=True)
        if(self.bsNode=='Default'):
            self.bsNodeSize = 0
        else:
            self.bsNodeSize = len(self.bsNode)        
        
        #Close window
        mc.deleteUI('cbsWin',window=True)        
        
        #Get deformers influencing base mesh
        temp = mc.listHistory(self.baseMesh)
        
        #Lets store all blendshapes, skin clusters and tweak nodes
        deformers = []
        for each in temp:
            temp2 = mc.nodeType(each)
            if(temp2 == 'skinCluster'):
                deformers.append(each)
            if(temp2 == 'blendShape'):
                deformers.append(each)
            if(temp2 == 'tweak'):
                deformers.append(each) 
            if(temp2 == 'nonLinear'):
                deformers.append(each)
                   
        #Lets turn off their envelopes        
        for each in deformers:
            mc.setAttr(each + ".envelope",0)
            
        #Get neutral mesh
        self.Tpose = mc.duplicate(self.baseMesh)
        
        #Hide TPoseMesh, NeutralMesh and Base mesh
        try:
            mc.setAttr(self.Tpose[0] + ".visibility", 0)
            mc.setAttr(self.bpNeutralMesh + ".visibility", 0)
            mc.setAttr(self.baseMesh[0] + ".visibility", 0) 
        except:
            pass
        
        #And now lets switch envelopes all back on
        for each in deformers:
            mc.setAttr(each + ".envelope",1)

        #Apply bpModifyMesh as FOC BS to self.bpNeutralMesh
        self.modifyBS = mc.blendShape( self.bpModifyMesh, self.bpNeutralMesh, w=(1,1), foc=True )
        #Apply Tpose as Parallel BS to self.bpNeutralMesh
        self.tposeBS = mc.blendShape( self.Tpose, self.bpNeutralMesh, w=(1,0), par=True )
        
        if(mc.window( 'cbs2Win',exists=True )):
            mc.deleteUI( 'cbs2Win',window=True)
        mc.window('cbs2Win',rtf=True, title = "Adjust Mesh",w=320)
        
        mc.columnLayout()
        mc.text("Adjust the geometry then")
        mc.text(" click continue.")
        mc.button(label='   Continue',c=self.cbs2,w=100)

        mc.showWindow('cbs2Win')
        
    def cbs2(self,*args):
        '''
            Add bpMesh to BS node selected by user.
        '''  
        #Store wether or not user is using existing bs node
        mc.deleteUI('cbs2Win',window=True)

        #Lets get the index to add to BS 
        #Also, determine if the standard BS node exists
        SN_exists = ""
        SBSN = 0
        
        try:
            SN_exists = mc.listAttr(self.scriptBSnode,v=True)
        except:
            pass
        
        try:
            SBSN = len(SN_exists) #Standard BlendShape Node
        except:
            pass

        #Determine index by counting existing items in BSnode and adding 1
        if(self.bsNodeSize):
            temp = mc.blendShape(self.bsNode,q=True,t=True)
            index = len(temp) + 1
        elif(SBSN):
            temp = mc.blendShape(self.scriptBSnode,q=True,t=True)
            index = len(temp) + 1     
        else:
            index = 0
        #Turn on the Tpose BS and the ModifyBS on the neutral
        mc.setAttr(self.tposeBS[0] + "." + self.Tpose[0], 1)
        mc.setAttr(self.modifyBS[0] + "." + self.bpModifyMesh, 1)
 
        if(self.bsNodeSize): #Yes
            #Apply to user selected bs node
            try:
                mc.blendShape(self.bsNode,e=True,t=(self.baseMesh[0],index,self.bpNeutralMesh,1)) 
            except:
                print "Error connecting to " + self.bsNode
        else:
            #Apply to standard script node, if it exists, otherwise, create it.
            try:
                mc.blendShape(self.scriptBSnode,e=True,t=(self.baseMesh[0],index,self.bpNeutralMesh,1))
                mc.blendShape(self.scriptBSnode,e=True,w=(index,1))
            except: 
                print self.scriptBSnode    
                self.newBS = mc.blendShape(self.bpNeutralMesh,self.baseMesh,par=True,name=self.scriptBSnode)
                mc.blendShape(self.newBS,e=True,w=(1,1))
                
        #Show baseMesh
        try:
            mc.setAttr(self.baseMesh[0] + ".visibility", 1)   
        except:
            pass
        
        #Delete Tpose and Modify meshes
        mc.delete(self.bpModifyMesh, self.Tpose)               
        
        if(self.bsNodeSize):
            mc.select(self.bsNode,r=True)
        else:
            mc.select(self.scriptBSnode,r=True) 

    def quickClose(self,*args):
        mc.deleteUI('cbsWin', window=True)   
        
     

