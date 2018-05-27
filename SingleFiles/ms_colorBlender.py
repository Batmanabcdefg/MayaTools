"""
Copyright (c) 2009 Mauricio Santos
Name: ms_colorBlender.py
Version: 1.0
Author: Mauricio Santos
Contact: mauricioptkvp@hotmail.com
Date Created: Sometime in 2007?
Last Modified: 26 June 2009
License: LGNU
Description: 

To do:
        
         
        -Add progress bar while creating the second window.
                It takes a while to build in Linux, user might double click, 
                creating a bunch of window requests, which pop up after awhile and 
                slow down the computer and anger user:( not good...

        -Query user:
			-"Would you like to create attribute and SDK?"
			IF: Yes: 
			     Get controller name(For Attribute)
			     -Get Attribute Name from user
				for x in numControls:
					-Store (blenderName)
					-AttName Exist?
						-No: Create att on control Name
						-Yes: Continue
					-Run SDK  
						-Load blenderName as driven
						-Load controller Name as driver
					-Wait Prompt: "Press when done with SDK for blanderName"
						-Pressed = Continue Loop at next iteration (continue)
			IF: No
				Exit
                        
Additional Notes:
		
		-How do I make a button command that can pass an argument?
		-Answer: By-Passed: Created button inside of a class, with instance specific
		            load functions.
		            
		-How do you access a created instance by name?
		-The mistake I was making was in the way I was creating my instances. instance = class.  This only makes a copy of the class!
		    That's why I couldn't access instance specific attributes or store their names upon creation.
		    I wasn't actually creating instances! Well, the right way is like this:
		        instance = class( arg1,arg2,... )

"""
#	Why?: Automated otherwise lengthy procedure outlined below.

#	Procedure:
#		-Query user for number of nodes to create (numControls)
#
#		-for x in numControls:
#			-Obtain two source and one target joint names
#			-node name selection
#		-for x in numControls
#			-Create colorBlend node
#			-Link source joints to inputs
#			-Link target joint to output

import maya.cmds as mc

class ms_colorBlender():
    def __init__(self,*args):
        """
         Initial prompt
        """
        if(mc.window("ms_colorBlender",exists=True)):
            mc.deleteUI("ms_colorBlender",window=True)
        mc.window("ms_colorBlender",title="ms_colorBlender v0.1", rtf=True)
        mc.columnLayout()

        mc.text("How many Blend Nodes?")
        self.intFieldName = mc.intField(ann="How many blend nodes?")
        mc.button(label = "Continue", c = self.blender)

        mc.showWindow("ms_colorBlender")
        
    def blender(self,*args):
        """
        Second window: User enters values per node here.
        """
        self.numControls = mc.intField(self.intFieldName,q=True,v=True)
        self.source1 = [] #Used to store names. Assignment happens in step2.
        self.source2 = []
        self.target = []
        self.nodeName = []  
        
        if(mc.window("ms_blending",exists=True)):
            mc.deleteUI("ms_blending",window=True)
            
        mc.window("ms_blending",title="ms_colorBlender v1.0", rtf=True)
        mc.scrollLayout()
        mc.columnLayout()
        
        #Creates numControls frameLayouts by calling fieldsGrp class.
        count = 1 #frameLayout counter
        self.frames = []
        while count < (self.numControls + 1):
            inst = fieldsGrp(count)        #Construct instance of frameLayout group creation class and store it.
            self.frames.append( inst )     #Store created instance
            count = count + 1
        
        #Main creation window buttons/options here
        mc.rowLayout(nc=4)
        mc.text(" Load selected as: ")
        mc.button(label="All Source1", c = self.loadAllSrc1)
        mc.button(label="All Source2", c = self.loadAllSrc2)
        mc.button(label="All Targets", c = self.loadAllTgt)
        mc.setParent("..")
        
        mc.separator(w=400)
        mc.text("\n                Prefix for each blendColor node created.")
        self.prefixField = mc.textFieldGrp(label='Prefix:',text='Default')
        
        mc.text("\n                Attributes to connect into blendColor node inputs/outputs. No point. ('.')")
        self.src1AttField = mc.textFieldGrp(label='Input 1:',text='rotate')
        self.src2AttField = mc.textFieldGrp(label='Input 2:',text='rotate')
        self.tgtAttField = mc.textFieldGrp(label='Output:',text='rotate')
        mc.text("\n")
        mc.text('                              Source1 = 1,  Source2 = 0')
        self.wieghtField = mc.floatFieldGrp(label='Weight On:')
        
        mc.rowLayout(nc=4)
        mc.text(" ")
        mc.text(" ")
        mc.button(label="Connect", c = self.createLinkNodes )
        mc.text(" ")
        mc.setParent("..")
        
        mc.setParent("..")
        mc.setParent("..")
        
        mc.showWindow("ms_blending")
        mc.deleteUI('ms_colorBlender',window=True)
    
    def createLinkNodes(self,*args):	
        #Create (numControls) blendColor nodes, store names, 
        #finally, link src1 + src2 into node inputs and tgt into node output.
        prefix = mc.textFieldGrp(self.prefixField,query=True,text=True)
        createdNames = []  
        
        x = 0
        while x < self.numControls:
            if "Default" in prefix:
                createdNames.append(mc.createNode( 'blendColors')) #Store all names as created by Maya
                x = x + 1
                continue
   
            else:
                temp = mc.createNode( 'blendColors' )
                name = prefix + temp + str(x)
                mc.rename( temp, name )
                createdNames.append( name  )#User selected name, stored in same array
                x = x + 1
    	
    	mc.select(clear=True)
    	
    	#Get user weight choice
    	#weightChoice = mc.radioButtonGrp('weightField', query = True, sl = True)
    	wgt = mc.floatFieldGrp(self.wieghtField,query=True,value1=True)
        
        #	Now we link!
        #Get atts to link (i.e: rotate or translate, etc...)
        src1Att = mc.textFieldGrp(self.src1AttField,query=True,text=True)
        src2Att = mc.textFieldGrp(self.src2AttField,query=True,text=True)
        tgtAtt = mc.textFieldGrp(self.tgtAttField,query=True,text=True)
        
        input1 = src1Att
        input2 = src2Att
        output = tgtAtt
        
        z=0
        for each in createdNames:
            #set weight current blender node
            mc.setAttr((each + ".blender"), wgt)	
    	
            #node attributes
            nodeColor1Att = (each + ".color1")
            nodeColor2Att = (each + ".color2")
            nodeOutputAtt = (each + ".output")
            
            #Get object names from GUI fields per instance in self.frames
            field = self.frames[z].src1Field
            src1Obj = mc.textFieldButtonGrp(field, query=True, text=True)

            src1 = (src1Obj+"."+input1)
            
            field = self.frames[z].src2Field
            src2Obj = mc.textFieldButtonGrp(field, query=True, text=True)
            src2 = (src2Obj+"."+input2)
            
            field = self.frames[z].tgtField
            tgtObj = mc.textFieldButtonGrp(field, query=True, text=True)
            tgt = (tgtObj+"."+output)
        		
    	
            #connections made here
            mc.connectAttr(src1, nodeColor1Att)
            mc.connectAttr(src2, nodeColor2Att)
            mc.connectAttr(nodeOutputAtt, tgt)
    
            z = z + 1

        #Finally, print the names of the created nodes
        print " " * 20
        for each in createdNames:
            print each
    	
    def loadAllSrc1(self,*args):
        """
         Loads each object in the current selection into all the source1 fields.
         Allows for one-click populating of object fields instead of 
         one at a time loading.
        """
        sel = mc.ls(sl=True, fl=True)
        #Iterate thru each object/instance, updating fields with current selection(s)
        for obj,inst in zip(sel,self.frames):
            mc.textFieldButtonGrp(inst.src1Field, edit=True, text=obj)
            
            
    
    def loadAllSrc2(self,*args):
        sel = mc.ls(sl=True, fl=True)
        
        for obj,inst in zip(sel,self.frames):
            mc.textFieldButtonGrp(inst.src2Field, edit=True, text=obj)
            
    def loadAllTgt(self,*args):
        sel = mc.ls(sl=True, fl=True)
        
        for obj,inst in zip(sel,self.frames):
            mc.textFieldButtonGrp(inst.tgtField, edit=True, text=obj)	  		

"""
    This class is so that I can have unique instances of each frameLayout element. This allows me
        to create unique load functions for the text fields.
        Now, each 'load' button calls its unique load function. 
"""
class fieldsGrp():
    """
     Support class to create frameLayout with three textFieldButtonGrp's.
     We can query/edit each instance uniquely.
    """
    def __init__(self,count,*args):
        #Creates numControls frameLayouts.
        #It makes the unique names accessible via the classes attributes: instance.src1Field etc...
        self.num = count #This makes num available through out the class.
        
        mc.frameLayout(l=("BlendColor Node " + str(count)),cll=1)
        mc.columnLayout()

        self.src1Field = mc.textFieldButtonGrp( label="Source 1:(i.e. FK)", buttonLabel="Load", bc = self.loadSrc1  ) 
        self.src2Field = mc.textFieldButtonGrp( label="Source 2:(i.e. IK)", buttonLabel="Load" , bc = self.loadSrc2  )
        self.tgtField = mc.textFieldButtonGrp( label="Target:(i.e. Skin Jnt)", buttonLabel="Load", bc = self.loadTgt  )
       
        mc.setParent("..")
        mc.setParent("..") 
        
    def loadSrc1(self,*args):
        name = mc.ls(sl=True,fl=True)
        mc.textFieldButtonGrp(self.src1Field,edit=True,text=name[0]) 
    
    def loadSrc2(self,*args):
        name = mc.ls(sl=True,fl=True)
        mc.textFieldButtonGrp(self.src2Field,edit=True,text=name[0])
        
    def loadTgt(self,*args):
        name = mc.ls(sl=True,fl=True)
        mc.textFieldButtonGrp(self.tgtField,edit=True,text=name[0])
        
        
          
        
            
    



