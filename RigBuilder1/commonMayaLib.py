from __future__ import with_statement # This line is only needed for 2008 and 2009
from pymel.core import *
"""
Copyright (c) 2010 Mauricio Santos-Hoyos
Name: commonMayaLib.py
Version: 1.0
Author: Mauricio Santos-Hoyos
Contact: mauricioptkvp@hotmail.com
Date Created:   9 Oct 2010
Last Modified:  21 Oct 2010

$Revision: 134 $
$LastChangedDate: 2011-08-21 15:43:44 -0700 (Sun, 21 Aug 2011) $
$Author: mauricio $
$HeadURL: file:///Users/mauricio/SVN_Repos/Maya_Tools/trunk/Tools/Rigging/Dev/RigBuilder/commonMayaLib.py $
$Id: commonMayaLib.py 134 2011-08-21 22:43:44Z mauricio $

Description: 
    Collection of small, re-useable Maya methods organized into a class.

Used by: createArmRig.py, createLegRig.py, createIkPoleVector.py
    
Additional Notes: 

Example call:
>>import commonMayaLib as cml
>>cml.snapping( objA, objB )
      
Attributes:

Methods:
    snapping(a,b): Snap Maya transform A to B.
    zero(object)
    squashStretchSDKs(squashNode,distNode)
             
Requires:


Development notes:
   
"""
class commonMayaLib():
    """
    Collection of small, re-useable Maya methods.
    """  
    def snapping(self,a,b,*args):
        """
            Snap a to b.
        """

        pos = xform( b, q=1, ws=True, t=1)
        xform( a, ws=True, t=[pos[0], pos[1], pos[2]])

        rot = xform( b, q=1, ws=True, ro=1)
        xform( a, ws=True, ro=[rot[0], rot[1], rot[2]])

    def zero(self,obj,*args):
        """
            Zero object and create a buffer node for obj.
            Returns bufferNode
        """
        parentObj = listRelatives(obj,parent=True)
        
        name = '%s_buffer'%obj
        zeroNode = group(em=True,n=name)

        pos = xform( obj, q=1, ws=True, t=1)
        xform( zeroNode, ws=True, t=[pos[0], pos[1], pos[2]])

        rot = xform( obj, q=1, ws=True, ro=1)
        xform( zeroNode, ws=True, ro=[rot[0], rot[1], rot[2]])

        scale = xform( obj, q=1, r=True, s=1)
        xform( zeroNode, ws=True, s=[scale[0], scale[1], scale[2]])

        parent(obj, zeroNode, a=True)
        
        try:
            # If it has a parent
            parent(zeroNode, parentObj)
        except:
            pass
        
        return zeroNode
    
    def squashStretchSDKs(self,squashNode,distNode,distValues,squashValues):
        """
        # Use: Select squash node, then distance node, then run code.
        # Command line: squashStretchSDKs(squashNode,distNode,distValues,squashValues)
        
        # Returns: SDK animation curves
        
        # distValues: (7.746, 11.61,6.0) Tuple of three floats
            [0] = Value at default 
            [1] = Value at stretch 
            [2] = Value at squash
        # squashValues: (0.0,1.5,-0.8) Tuple of three floats
            [0] = Value at default 
            [1] = Value at stretch 
            [2] = Value at squash
        
        # What it does: Sets up two SDK's: Squashed and stretched.
        # Driver: Distance 
        # Driven: Squash Factor

        @todo - Allow the user to pass in values
        """
        
        sel = ls(sl=True)
        
        # Transform node names
        squashNode = sel[0]
        distNode = sel[1]
        
        # Get deformer node name
        squash = ''
        list = listConnections(squashNode)
        for each in list:
            if objectType(each) == 'nonLinear':
                squash = each
        
        tempDist = listRelatives(distNode,shapes=True)
        distShape = tempDist[0]
        
        # Setup SDK
        # Default
        setDrivenKeyframe( '%s.factor'%squash, cd='%s.distance'%distShape,dv=distValues[0],v=squashValues[0])
        # Stretched
        setDrivenKeyframe( '%s.factor'%squash, cd='%s.distance'%distShape,dv=distValues[1],v=squashValues[1])
        # Squashed
        setDrivenKeyframe( '%s.factor'%squash, cd='%s.distance'%distShape,dv=distValues[2],v=squashValues[2])
        
    def breakScript(self):
        """ Call this method to terminate a script and return to Maya. """
        import sys
        sys.exit()