from __future__ import with_statement # This line is only needed for 2008 and 2009
from pymel.core import *
"""
Copyright (c) 2010 Mauricio Santos
Name: createNeckRig.py
Version: 0.9
Author: Mauricio Santos
Contact: mauricioptkvp@hotmail.com
Date Created:   28 Dec 2010
Last Modified:  28 Dec 2010

Description: 
    Build a neck rig.

Used by: createFullRig.py

Uses:

Process:


Example call:

Additional Notes: 

@todo    

"""
import commonMayaLib as cml
import standardNames

class createNeckRig():
    """
    Creates a neck rig.
    """
    def __init__(self,**keywords):
        # Set version number
        self.version = 0.9
        
        # Create library instance
        self.lib = cml.commonMayaLib()
        
        # Standard names object
        self.sNames = standardNames.standardNames()
        
        # Store the final node names to be returned to client
        self.createdNodes = {}
        
        # Command line call
        self.commandlineCall(keywords)
        
    def commandlineCall(self,keywords):
        """
        Store values passed via commandline arguments
        and call the main process.
        """
        pass
    
    def createJoints(self,*args):
        """
        Create the Ik and the control joints.
        """
        pass
    
    def bindSplineCurve(self,*args):
        """
        Skin the spline IK curve to the control joints.
        """
        pass
    
    def createNeckControl(self,*args):
        """
        Create the mid neck control and all the needed
        groups to make the final rig.
        """
        pass
    
    def setupConnections(self,*args):
        """
        Make constraints and connect them to attributes.
        """
        pass
    
    def finalizeRig(self,*args):
        """
        Parent control joints to controllers and organize
        heirarchy.
        """
        pass