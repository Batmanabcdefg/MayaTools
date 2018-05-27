"""
Copyright (c) 2009 Mauricio Santos
Name: ms_visSwitch.py
Version: 1.0
Author: Mauricio Santos
Contact: mauricioptkvp@hotmail.com
Date Created:  27 July 2009
Last Modified: 16 Dec 2009
License: LGNU
Description:
 Load a list with objects, select a controller to place the switching attribute, 
     name the attribute and hit 'Create' button.

To do:


Additional Notes:

"""
import maya.cmds as mc 
import maya.mel as mel


class  ms_visSwitch():
    def __init__(self):
        """
         Connects visibility of items in list to the selected attribute.
        """
        if(mc.window( 'visSwitchWin',exists=True )):
           mc.deleteUI( 'visSwitchWin',window=True)
        
        mc.window('visSwitchWin',rtf=True, title = "Visibility Switch v1.0",w=200)
 
        mc.columnLayout()                                           #Main layout
        
        
        mc.text(' ')
        mc.text('       Creates user named attribute on control if it doesn\'t exist.')
        mc.text('       Connects that attribute to the \'.visibility\' attribute of ')
        mc.text('       objects loaded in the list.')
        mc.text('       List size is printed in the command response / script editor.')
        
        mc.text(' ')
        self.cntFld = mc.textFieldButtonGrp(label='Switch Control',bl='Load',bc=self.loadCnt)
        self.attNameFld = mc.textFieldGrp( label="Attribute Name:", text='l_arm_cnt_vis' )
        mc.rowLayout(nc=2)
        mc.text(" ")
       
        
        """self.attrMenu = mc.optionMenu(label='Attribute')
        try: #The control 'Load' function re-runs __init__ to rebuild this menu with current objects atts
            for each in self.atts:
                mc.menuItem(label=each)
        except:
            pass
        mc.setParent("..")
        """
        
        mc.rowLayout(nc=2,cw2=(100,200))
        mc.text(' ')
        mc.columnLayout()
        mc.text(" Objects  ",fn='boldLabelFont')
        self.objectsListFld = mc.textScrollList(numberOfRows=10, w=150, ams = True)
        mc.button(label="   Load Objects", c = self.loadList,w=100)
        mc.button(label="      Reset", c = self.resetList,w=100)    
        mc.button(label="     Remove", c = self.removeItem,w=100)    
        mc.button(label="    List Size", c = self.listSize,w=100)    
        mc.setParent('..')
        mc.setParent('..')
        
        
        
        mc.setParent( ".." )
           
        mc.text(" ")
        mc.rowLayout(nc=2)
        mc.text(" ")
        mc.button(label="     Create  ",c=self.createSwitch,w=100)
        mc.setParent("..")
        
        mc.frameLayout(label=" Common Tools", cl=True, cll=True)
        mc.button(label="Add Attribute",w=100,c= 'mel.eval("AddAttribute;")' )
        
        
        
        mc.setParent("..")
        
        
        mc.showWindow('visSwitchWin')
    
    def createSwitch(self,*args):
        """
         Links visibility of selected to attribute specified
        """
        objectsList = mc.textScrollList(self.objectsListFld,query=True,allItems=True)
        cnt = mc.textFieldButtonGrp(self.cntFld,query=True,text=True)
        attr = mc.textFieldGrp(self.attNameFld,query=True,text=True)
        
        for obj in objectsList:
            try:                #If it fails, means we need to create the attribute. 
                mc.connectAttr( cnt+'.'+attr, obj+'.visibility', f=True )   
            except:             #Once it's created, it shouldn't fail again
                mc.addAttr( cnt, longName=attr, attributeType='long',min=0,max=1, k=True )
                mc.connectAttr( cnt+'.'+attr, obj+'.visibility', f=True ) 
                
    def loadCnt(self,*args):
        sel = mc.ls(sl=True,fl=True)
        
        #Store all keyable attributes
        self.atts = []
        self.atts = mc.listAttr(sel[0],k=True)
             
        #And finally, load the controller name
        mc.textFieldButtonGrp(self.cntFld,e=True,text=sel[0])
        
    def loadAttr(self,*args):
        sel = mc.ls(sl=True,fl=True)
        mc.textFieldButtonGrp(self.attrFld,e=True,text=sel[0])

    def listSize(self,*args):  
        num = 0  
        items = mc.textScrollList(self.objectsListFld,q=True,ai=True)
        try:
            num = len(items)
        except:
            pass
        print "\n\n\n\n\nThere are %i items in the source list." % num  
     
    def resetList(self,*args):    
        mc.textScrollList(self.objectsListFld,e=True,ra=True)      
        
    def loadList(self,*args):
        sources = mc.ls(sl=True,fl=True)
        for each in sources:
                mc.textScrollList(self.objectsListFld,e=True,a=each)
                
    def removeItem(self,*args):
        selected = mc.textScrollList(self.objectsListFld,q=True,si=True)    
        for each in selected:
            mc.textScrollList(self.objectsListFld,e=True,ri=each)  
                                           
                
    
        
        