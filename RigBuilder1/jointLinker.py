from __future__ import with_statement # This line is only needed for 2008 and 2009
from pymel.core import *

"""
Copyright (c) 2009,2010 Mauricio Santos
Name: jointLinker.py
Version: 1.0
Author: Mauricio Santos
Contact: mauricioptkvp@hotmail.com
Date Created: 30 Aug 2008
Last Modified: 2 Dec 2010

$Revision: 132 $
$LastChangedDate: 2011-08-06 19:27:15 -0700 (Sat, 06 Aug 2011) $
$Author: mauricio $
$HeadURL: file:///Users/mauricio/SVN_Repos/Maya_Tools/trunk/Tools/Rigging/Dev/RigBuilder/jointLinker.py $
$Id: jointLinker.py 132 2011-08-07 02:27:15Z mauricio $

Description:
 Connect two sets of joints based on location and/or naming with
 direct connections, or constraints. 

To do:
    - Linker: Can select "Type" in GUI for more types, not just 'joint'
    - Figure out how to delete a pane docked to $gMainWindow

Additional Notes:

History:
    2010-Sep-30 : Refactored using PyMEL
    2010-Nov-13 : Added command line interface and removed gui
    2010-Dec-02 : Added check to ensure constraint to only one object

"""
class  jointLinker():
    def __init__(self,**keywords):
        self.commandLineCall(keywords)

    def commandLineCall(self,keywords):
        self.srcJoints = keywords['srcJoints']
        self.tgtJoints = keywords['tgtJoints']
        self.cType = keywords['cType'] #1=None,2=parent,3=point,4=orient,5=scale
        self.slop = keywords['slop']
        self.offsetVal = keywords['offsetVal']
        
        self.connectType = keywords['connectType'] #1=Location, 2=Name
        self.drivenPrefix = keywords['drivenPrefix']
        self.driverPrefix = keywords['driverPrefix']
        self.namespace = keywords['namespace']
        
        self.tVal = keywords['tVal']
        self.rVal = keywords['rVal']
        self.sVal = keywords['sVal']
        
        self.linkJoints()
     
    def linkJoints(self,*args):
        """
        Link joints
        """
        srcPos = []
        tgtPos = []
        
        if(self.offsetVal == 1):
            offset = 1
        else:
            offset = 0
        try:
            for each in self.srcJoints:
                temp = xform(each,query=True,ws=True,t=True)
                srcPos.append(temp)
        except:
            pass        
        
        try:
            for each in self.tgtJoints:
                temp = xform(each,query=True,ws=True,t=True)
                tgtPos.append(temp)
        except:
            pass
        
        #--- Constraint Portion
        if(self.cType == 2): #Parent Constraint
            x = 0
            for src in self.srcJoints:  #Check each joint in self.srcJoints against each joint in self.tgtJoints, see if they are overlapping within the given tolerance
                y = 0
                for tgt in self.tgtJoints:
                    if(tgtPos[y][0] < (srcPos[x][0] + self.slop) and tgtPos[y][0] > (srcPos[x][0] - self.slop)):
                        if(tgtPos[y][1] < (srcPos[x][1] + self.slop) and tgtPos[y][1] > (srcPos[x][1] - self.slop)):
                            if(tgtPos[y][2] < (srcPos[x][2] + self.slop) and tgtPos[y][2] > (srcPos[x][2] - self.slop)):
                                # Check for existing constraints
#                                children = listRelatives(tgt)
#                                for child in children:
#                                    if 'Constraint' in child:
#                                        continue
#                                    else:
#                                        parentConstraint(src,tgt,mo=offset)
                                parentConstraint(src,tgt,mo=offset)
                    y = y + 1
                x = x + 1

        if(self.cType == 3): #Point Constraint
            x = 0
            for src in self.srcJoints:  #Check each joint in self.srcJoints against each joint in self.tgtJoints, see if they are overlapping within the given tolerance
                y = 0
                for tgt in self.tgtJoints:
                    if(tgtPos[y][0] < (srcPos[x][0] + self.slop) and tgtPos[y][0] > (srcPos[x][0] - self.slop)):
                        if(tgtPos[y][1] < (srcPos[x][1] + self.slop) and tgtPos[y][1] > (srcPos[x][1] - self.slop)):
                            if(tgtPos[y][2] < (srcPos[x][2] + self.slop) and tgtPos[y][2] > (srcPos[x][2] - self.slop)):
                                pointConstraint(src,tgt,mo=offset)
                    y = y + 1
                x = x + 1
                
        if(self.cType == 4): #Orient Constraint
            x = 0
            for src in self.srcJoints:  #Check each joint in self.srcJoints against each joint in self.tgtJoints, see if they are overlapping within the given tolerance
                y = 0
                for tgt in self.tgtJoints:
                    if(tgtPos[y][0] < (srcPos[x][0] + self.slop) and tgtPos[y][0] > (srcPos[x][0] - self.slop)):
                        if(tgtPos[y][1] < (srcPos[x][1] + self.slop) and tgtPos[y][1] > (srcPos[x][1] - self.slop)):
                            if(tgtPos[y][2] < (srcPos[x][2] + self.slop) and tgtPos[y][2] > (srcPos[x][2] - self.slop)):
                                orientConstraint(src,tgt,mo=offset)
                    y = y + 1
                x = x + 1
                
        if(self.cType == 5): #Scale Constraint
            x = 0
            for src in self.srcJoints:  #Check each joint in self.srcJoints against each joint in self.tgtJoints, see if they are overlapping within the given tolerance
                y = 0
                for tgt in self.tgtJoints:
                    if(tgtPos[y][0] < (srcPos[x][0] + self.slop) and tgtPos[y][0] > (srcPos[x][0] - self.slop)):
                        if(tgtPos[y][1] < (srcPos[x][1] + self.slop) and tgtPos[y][1] > (srcPos[x][1] - self.slop)):
                            if(tgtPos[y][2] < (srcPos[x][2] + self.slop) and tgtPos[y][2] > (srcPos[x][2] - self.slop)):
                                scaleConstraint(src,tgt,mo=offset)
                    y = y + 1
                x = x + 1                
        
        
        if(self.connectType == 1): #Location based Connection
            if(self.tVal == 1):
                x = 0
                for src in self.srcJoints:  #Check each joint in self.srcJoints against each joint in self.tgtJoints, see if they are overlapping within the given tolerance
                    y = 0
                    for tgt in self.tgtJoints:
                        if(tgtPos[y][0] < (srcPos[x][0] + self.slop) and tgtPos[y][0] > (srcPos[x][0] - self.slop)):
                            if(tgtPos[y][1] < (srcPos[x][1] + self.slop) and tgtPos[y][1] > (srcPos[x][1] - self.slop)):
                                if(tgtPos[y][2] < (srcPos[x][2] + self.slop) and tgtPos[y][2] > (srcPos[x][2] - self.slop)):
                                    connectAttr(src + ".translate",tgt + ".translate",f=True)
                        y = y + 1
                    x = x + 1 
                
            if(self.rVal == 1):
                x = 0
                for src in self.srcJoints:  #Check each joint in self.srcJoints against each joint in self.tgtJoints, see if they are overlapping within the given tolerance
                    y = 0
                    for tgt in self.tgtJoints:
                        if(tgtPos[y][0] < (srcPos[x][0] + self.slop) and tgtPos[y][0] > (srcPos[x][0] - self.slop)):
                            if(tgtPos[y][1] < (srcPos[x][1] + self.slop) and tgtPos[y][1] > (srcPos[x][1] - self.slop)):
                                if(tgtPos[y][2] < (srcPos[x][2] + self.slop) and tgtPos[y][2] > (srcPos[x][2] - self.slop)):
                                    connectAttr(src + ".rotate",tgt + ".rotate",f=True)
                        y = y + 1
                    x = x + 1
                
            if(self.sVal == 1):
                x = 0
                for src in self.srcJoints:  #Check each joint in self.srcJoints against each joint in self.tgtJoints, see if they are overlapping within the given tolerance
                    y = 0
                    for tgt in self.tgtJoints:
                        if(tgtPos[y][0] < (srcPos[x][0] + self.slop) and tgtPos[y][0] > (srcPos[x][0] - self.slop)):
                            if(tgtPos[y][1] < (srcPos[x][1] + self.slop) and tgtPos[y][1] > (srcPos[x][1] - self.slop)):
                                if(tgtPos[y][2] < (srcPos[x][2] + self.slop) and tgtPos[y][2] > (srcPos[x][2] - self.slop)):
                                    connectAttr(src + ".scale",tgt + ".scale",f=True)
                        y = y + 1
                    x = x + 1
    
        #--- Name based connections
        if(self.connectType == 2): 
            for each in self.tgtJoints:
                #Replace existing prefix with user specified prefix
                temp = each.lstrip(self.drivenPrefix)
                temp = self.driverPrefix + temp
                temp = self.namespace + temp
                
                print temp

                if(self.tVal == 1):
                    try:
                        connectAttr(temp + ".translate",each + ".translate",f=True)
                    except:
                        print "Error connecting to " + temp + ".translate" 
                if(self.rVal == 1):
                    try:
                        connectAttr(temp + ".rotate",each + ".rotate",f=True)
                    except:
                        print "Error connecting to " + temp + ".rotate"     
                if(self.sVal == 1):
                    try:
                        connectAttr(temp + ".scale",each + ".scale",f=True)
                    except:
                        print "Error connecting to " + temp + ".scale"  
                                     
