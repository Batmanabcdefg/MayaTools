from __future__ import with_statement # This line is only needed for 2008 and 2009
from pymel.core import *

"""
Copyright (c) 2011 Mauricio Santos-Hoyos
Name: AutoGUI.py
Version: 1.0
Author: Mauricio Santos
Contact: mauricioptkvp@hotmail.com
Date Created: 6 Jan 2011
Last Modified: 6 Jan 2011

$Revision: 132 $
$LastChangedDate: 2011-08-06 19:27:15 -0700 (Sat, 06 Aug 2011) $
$Author: mauricio $
$HeadURL: file:///Users/mauricio/SVN_Repos/Maya_Tools/trunk/Tools/Rigging/Dev/RigBuilder/spaceSwitchTool.py $
$Id: spaceSwitchTool.py 132 2011-08-07 02:27:15Z mauricio $

Description: 
    Creates a GUI that can switch from one space attribute to another without
    the IK control changing location.
      
Example call:


To do:
    

Dev Notes:

    
Additional Notes:

"""
__author__ = "Mauricio Santos"

class spaceSwitchTool():
    """
    Creates a GUI that can switch from one space attribute to another without
    the IK control changing location.
    """
    def __init__(self,*args):
        self.version = 1
        
        if __name__ == 'spaceSwitchTool':
            self.buildGUI()
    
    def buildGUI(self,*args):
        """
        Create GUI with drop down menu of space switch options for loaded controller.
        """
        if(window( 'spaceSwitchToolWin',exists=True )):
            deleteUI('spaceSwitchToolWin',window=True )
            
        # Get current selection
        sel = ls(sl=True)   
        
        with window( 'spaceSwitchToolWin',title=' Space Switch Tool v%s'%self.version,rtf=True ) as mainWin:
            with columnLayout():
                with frameLayout(label='Help',cl=True,cll=True,w=420):
                    with columnLayout():
                        text('\n         Switch space of IK control maintaining current position.')
                        text('          No keys added, unless AutoKey is active and switch attr is keyed.\n')
                        text('            -Select Ik control and click "load".')
                        text('            -Select space switch attribute to set to 0.')
                        text('            -Select space switch attribute to set to 1.')
                        text('            -click "Switch".\n')
                
                if len(sel):
                    self.cntFld = textFieldButtonGrp( l="Ik Control:",bl="Load",bc=self.loadCnt,text=sel[0] ) 
                else:
                    self.cntFld = textFieldButtonGrp( l="Ik Control:",bl="Load",bc=self.loadCnt,text=' ' ) 
                     
                with rowLayout(nc=2,cw2=(100,200)):
                    text('   Switch from:')
                    self.spaceMenu1 = optionMenu( label='(Set to 0)' )
                    
                with rowLayout(nc=2,cw2=(100,200)):
                    text('   Switch to:')
                    self.spaceMenu2 = optionMenu( label='(Set to 1)' )
                    
                with rowLayout(nc=2,cw2=(150,100)):
                    text(' ')
                    button( label='        Switch ',c=self.switch,w=100)
                                 
                mainWin.show()

    def switch(self,*args):
        """
        Given IK control, switch it's space but maintain
        the position of the control.
        """
        # Get control
        cnt = textFieldButtonGrp(self.cntFld,query=True,text=True)
        
        # Create locator, snap it to controls location
        loc = spaceLocator()
        temp = pointConstraint(cnt,loc,mo=False)
        delete(temp)
        temp = orientConstraint(cnt,loc,mo=False)
        delete(temp)
        
        # Change the space switch value
        att1 = optionMenu(self.spaceMenu1,query=True,v=True)
        att2 = optionMenu(self.spaceMenu2,query=True,v=True)
        setAttr('%s.%s'%(cnt,att1),0)
        setAttr('%s.%s'%(cnt,att2),1)
        
        # Snap the IK controller to the locator
        try:
            pos = xform( loc, q=1, ws=True, t=1)
            xform( cnt, ws=True, t=[pos[0], pos[1], pos[2]])
        except:
            pass
        try:
            rot = xform( loc, q=1, ws=True, ro=1)
            xform( cnt, ws=True, ro=[rot[0], rot[1], rot[2]])
        except:
            pass
        
        # Delete the locator
        delete(loc)
        
        # Select the IK control
        select(cnt,r=True)
    
    def loadCnt(self,*args):
        # Redraw GUI to load selected item and clear old menu items
        self.buildGUI()
        
        # Load selected item's attrs into the menu
        self.loadAttrs()
        
    def loadAttrs(self,*args):
        """
        Load attributes of object in cntFld to menu.
        """        
        # Get selection
        cnt = textFieldButtonGrp(self.cntFld,query=True,text=True)
        
        # Exit if no text in field
        if not len(cnt):
            return
        
        # Get keyable attributes
        atts = listAttr(cnt,k=True)
        
        # Load them to menu 
        for each in atts:
            menuItem( label=each, p = self.spaceMenu1 )
            menuItem( label=each, p = self.spaceMenu2 )
