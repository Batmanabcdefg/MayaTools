from __future__ import with_statement # This line is only needed for 2008 and 2009
from pymel.core import *

"""
Copyright (c) 2010 Mauricio Santos
Name: ms_LeafMaker.py
Version: 1.0
Author: Mauricio Santos
Contact: mauricioptkvp@hotmail.com
Date Created: 2 Dec 2010
Last Modified: 2 Dec 2010

Description:
    Creates two rigs:
        1: Places locators to create a branch rig.

        2: Given a single leaf mesh with it's pivot at the base of the stem, a user
             can create locators and place them in places where leafs will be created 
             with a master control object to adjust simulated wind effects.

To do:
    - 

Additional Notes:

History:
    2010-Dec-02 : Initial creation

"""

class ms_LeafMaker():
    """
    Creates two rigs:
        1: Places locators to create a branch rig.

        2: Given a single leaf mesh with it's pivot at the base of the stem, a user
             can create locators and place them in places where leafs will be created 
             with a master control object to adjust simulated wind effects.
    """
    def __init__(self,*args):
        self.buildGUI()
        
    def buildGUI(self,*args):
        """
        Create GUI for LeafMaker
        """
        if(window('leafMakerWin',exists=True)):
            deleteUI('leafMakerWin',window=True)
            
        with window('leafMakerWin',title=' Create Branch/Leaf Rigs',rtf=True) as mainWin:
            with columnLayout():      
                with frameLayout(label='Branch Rig',cll=True,cl=False,w=500):
                    with columnLayout():         
                        
                        with rowLayout(nc=3,cw3=(100,120,80)):
                            text(' ')                        
                            text('  How many joints?: ')    
                            self.branchJointsFld = intField(value=5,min=1)

                        with rowLayout(nc=2,cw2=(200,160)):
                            text(" ")
                            button(label='Create Branch Locators',c=self.br_placeLocators,w=160)
                            
                        with rowLayout(nc=2,cw2=(200,160)):
                            text(" ")
                            button(label='Create Branch Rig',c=self.br_rig,w=160)
                        
                
                with frameLayout(label='Leafs Rig',cll=True,cl=True,w=500):
                    with columnLayout():
                        self.leafGeoFld = textFieldButtonGrp(label='Leaf Geo:',bl='Load',bc=self.loadLeafGeo)
                    
                        with rowLayout(nc=2,cw2=(100,300)):
                            text(" ")
                            text('Locator will be placed at pivot of current selection.')
                    
                        with rowLayout(nc=2,cw2=(200,160)):
                            text(" ")
                            button(label='Create Leaf Locator',c=self.leaf_placeLocator,w=160)
                        
                        with rowLayout(nc=2,cw2=(200,160)):
                            text(" ")
                            button(label='Create Leaves Rig',c=self.leaf_rig,w=160)
                            
            mainWin.show()

    def br_placeLocators(self,*args):
        """
        Places locators for creation of branch rig.
        """
        numJnts = intField(self.branchJointsFld, query=True, value=True)
        x = 0
        offset = 0
        self.locators = []
        while x < numJnts:
            self.locators.append(spaceLocator(p=(offset,0,0),n='branchLocator_%s'%(x+1)))
            x = x + 1
            offset = offset + 5
        

    def leaf_placeLocator(self,*args):
        """
        Places a locator for creation of a leaf.
        """
        pass 
    
    def br_rig(self,*args):
        """
        Create:
            -Atts on controller
            -Connect: Atts --> MD Nodes --> Branch joints
        """
        pass
    
    def leaf_rig(self,*args):
        """
        Create:
            -Wind Attributes on controller
            -Connect: Atts --> MD Nodes --> leaves
        """
        pass

    def loadLeafGeo(self,*args):
        sel = ls(sl=True)
        textFieldButtonGrp(self.leafGeoFld,edit=True,text=sel[0])