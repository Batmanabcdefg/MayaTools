from __future__ import with_statement # This line is only needed for 2008 and 2009
from pymel.core import *

"""
Copyright (c) 2010,2011 Mauricio Santos-Hoyos
Name: AutoGUI.py
Version: $Revision: 132 $
Authors: Mauricio Santos, $Author: mauricio $
Contact: mauricioptkvp@hotmail.com
Date Created: 4 Dec 2010
$Date: 2011-08-06 19:27:15 -0700 (Sat, 06 Aug 2011) $
Last Modified: 10 Jan 2011

$Revision: 132 $
$LastChangedDate: 2011-08-06 19:27:15 -0700 (Sat, 06 Aug 2011) $
$Author: mauricio $
$HeadURL: file:///Users/mauricio/SVN_Repos/Maya_Tools/trunk/Tools/Rigging/Dev/RigBuilder/AutoGUI.py $
$Id: AutoGUI.py 132 2011-08-07 02:27:15Z mauricio $

Description: 
    Creates a customizable GUI for any items the user selects. 
    Best results with character in T pose
      
Example call:
    import AutoGUI
    AutoGUI.AutoGUI()

To do:
    -Fix: Ik/fk matching ---> Progress display look on fk to ik switch
    -Add: Space switch tool button in AutoGUI ---> Drop down menu space option selection, click 'Switch'.
                Switches from current space, to next space without changing position.
    -Add: Tab layouts
            -Poses tab with "Get pose" button
    -Add: Select all geometry list   ----> Select all geometry button for points caching.
    -Add: GUI shelf button icon selection field.   
    -Add: Selection Type drop down menu, vs having to choose only one. Simlar to namespace.

Dev Notes:
- Added : Custom error class
    
Additional Notes:
    Known issues: 
        A controller that is not uniquely named will not work with this script.
        All attributes with incoming connections should be locked and hidden. 
"""
__author__ = "Mauricio Santos"

import time
import standardNames

reload(standardNames)

class AutoGUIError(Exception):
    """ Custom error class to send messages to stderr """
    def __init__(self, value):
        Exception.__init__(self)
        self.value = value
    def __str__(self):
        return repr(self.value)
    

class FrameGrp():
    """
    Stores the data from a custom GUI creation group, i.e. L_Arm group.
    Used to generate gui.py file.
    
    Properties:
        self.objNames = []          #List of objects in gui group scroll list
        self.objAttrNames = []      #2D List of attr names per object [object[attrs]]
        self.objDefaults = []       #2D List of attr names per object [attr[values]]
        self.objAndAttrNames = []   #List of "objName.attr" per attr, per object.
        self.grpName = ''           #Name of the the specific GUI group.
        self.self.guiName = ''           #Name entered by user for the GUI.
        self.self.selType = ''           #Selection type chosen by user.
    """
    def __init__(self,*args):
        self.objNames = []          #List of objects in list
        self.objAttrNames = []      #List of attr names per object
        self.objDefaults = []       #List of current values per attribute, per object.
        self.objAndAttrNames = []   #List of "objName.attr" per attr, per object.
        self.grpName = ''           #Name of the the specific GUI group.
        self.guiName = ''           #Name entered by user for the GUI.
        self.selType = ''           #Selection type chosen by user.
        self.saveDir = ''           #Path to user selected save to directory for GUI file.


class AutoGUI():
    """
    The main method to create GUI / write gui.py file
    """
    def __init__(self,**keywords):
        """
        Setup initial variables
        """
        self.version = 1.1
        self.commandLineCall(keywords)
    
    def commandLineCall(self,keywords):
        """
        Initialize variables to values passed in via command line parameters.
        """
        self.guiName = keywords['guiName']     # Name of the GUI
        self.selType = keywords['selType']          # add, replace, or tgl. Defines behaviour of selection buttons.
        self.saveToDir = keywords['saveToDir']      # Directory to write the GUI file to
        self.ikFkMatch = keywords['ikFkMatch']      # 0, 1 = no/yes. Include ikFkMatching in GUI?
        self.groups = keywords['groups']            # Dict: { "group name":objects[] }  
        self.joint_up = keywords['joint_up']        # 
        
        if self.ikFkMatch == 1:                     # Needed to setup ik/fk matching on rig GUI script
            self.l_handCnt = keywords['l_handCnt']
            self.l_ikChain = keywords['l_ikChain']
            self.l_fkChain = keywords['l_fkChain']
            
            self.r_handCnt = keywords['r_handCnt']
            self.r_ikChain = keywords['r_ikChain']
            self.r_fkChain = keywords['r_fkChain']
        
        self.sNames = standardNames.standardNames()
        
        self.createObjects()     
        
    def createObjects(self,*args):
        """
        Creates FrameGrp objects with data for each group.
        
        Each FrameGrp object has:
        
        Properties:
            self.objNames = []          #List of objects in list
            self.objAttrNames = []      #List of attr names per object
            self.objDefaults = []       #List of current values per attribute, per object.
            self.objAndAttrNames = []   #List of "objName.attr" per attr, per object.
            self.grpName = ''           #Name of the the specific GUI group.
            self.self.guiName = ''      #Name entered by user for the GUI.
            self.self.selType = ''      #Selection type chosen by user.
            self.saveDir = ''           #Path to user selected save to directory for GUI file.
        
        Note: Namespaces: This can be a built in aspect of the script when 
            generating final object names for file output.
        """
        #Initializing variables
        self.frameGrps = []  #List of FrameGrp data objects
        
        #Setup group name list and list of associated objects
        self.grpNames = []
        self.guiGrpList = []
        
        self.grpNames.append('Head')
        self.guiGrpList.append(self.groups['Head'])

        self.grpNames.append('Torso')
        self.guiGrpList.append(self.groups['Torso'])
        
        self.grpNames.append('L_Arm')
        self.guiGrpList.append(self.groups['L_Arm'])
        
        self.grpNames.append('R_Arm')
        self.guiGrpList.append(self.groups['R_Arm'])
        
        self.grpNames.append('L_Leg')
        self.guiGrpList.append(self.groups['L_Leg'])
        
        self.grpNames.append('R_Leg')
        self.guiGrpList.append(self.groups['R_Leg'])
        
#        self.grpNames.append('Misc')
#        self.guiGrpList.append(self.groups['Misc'])
        
        #For each group, create a FrameGrp object and store the data.
        count = 0            
        for list,name in zip(self.guiGrpList,self.grpNames):
            
            #Create FrameGrp Object
            frameGrpObj = FrameGrp() 
            
            #Save to dir
            frameGrpObj.saveDir = self.saveToDir
            
            #Store gui name
            frameGrpObj.guiName = self.guiName
            
            #Store "obj_name" 's for all controller in group
            fullPathNames = []
            frameGrpObj.objNames = list

            #Store each objects unlocked/keyable attributes
            for obj in frameGrpObj.objNames:
                frameGrpObj.objAttrNames.append(listAttr(obj,keyable=True,u=True))
                
            #Store the "obj_name.attr" as a list for each attr the object has.
            #Store the default values as a list for each attr the object has.
            count = 0
            for obj in frameGrpObj.objNames:
                attrNamesArray = []
                valueArray = []
                for attr in frameGrpObj.objAttrNames[count]:
                    #"obj_name.attr"
                    tempStr = obj + '.' + attr
                    attrNamesArray.append(tempStr)
                    #Store default value for obj.attr
                    value = getAttr('%s.%s'%(obj,attr))
                    valueArray.append(value)
                    
                frameGrpObj.objAndAttrNames.append(attrNamesArray)
                frameGrpObj.objDefaults.append(valueArray)
                count = count + 1
            
            #Store the group name
            frameGrpObj.grpName = name
            
            #Store selection type
            frameGrpObj.selType = self.selType
            
            #Add to list of groups (FrameGrp objects)
            self.frameGrps.append(frameGrpObj)
            
            #Setup the Ik/Fk matching
            if self.ikFkMatch == 1:
                self.setupIkFkMatching()
            else:
                #Write the file
                self.writeFile()

            
    def setupIkFkMatching(self,*args):
        """
        Setup ik/fk matching distance dimension nodes on rig.
        """
        # Left arm:
        #-- Setup distance node between ik/fk elbow
        self.l_distNode = distanceDimension(sp=(10,10,10), ep=(11,11,11))
        temp = listConnections(self.l_distNode)
        startLoc = temp[0]
        endLoc = temp[1]

        #Parent locators to ik/fk elbow joints and hide them
        parent(startLoc,self.l_ikChain[1])
        makeIdentity(startLoc,t=True,r=True)
        
        parent(endLoc,self.l_fkChain[1])
        makeIdentity(endLoc,t=True,r=True)
        
        #Hide node and locators
        setAttr('%s.visibility'%self.l_distNode,0)
        setAttr('%s.visibility'%startLoc,0)
        setAttr('%s.visibility'%endLoc,0)
            
        # Right arm:
        #-- Setup distance node between ik/fk elbow
        self.r_distNode = distanceDimension(sp=(10,10,10), ep=(11,11,11))
        temp = listConnections(self.r_distNode)
        startLoc = temp[0]
        endLoc = temp[1]
        
        #Parent locators to ik/fk elbow joints and hide them
        parent(startLoc,self.r_ikChain[1])
        makeIdentity(startLoc,t=True,r=True)
        
        parent(endLoc,self.r_fkChain[1])
        makeIdentity(endLoc,t=True,r=True)
        
        #Hide node and locators
        setAttr('%s.visibility'%self.r_distNode,0)
        setAttr('%s.visibility'%startLoc,0)
        setAttr('%s.visibility'%endLoc,0)  
        
        # Place dist nodes in doNotTranslate grp
        parent(self.r_distNode,self.l_distNode,'%s_doNotTranslate'%self.guiName)
        
        #Write the file
        self.writeFile()          

    def writeFile(self,*args):
        """
        Now, armed with self.frameGrps, we write the file.
        
        GUI notes:
        -Buttons per Control:       'Select'     , 'Key'     , 'Reset'
        -Buttons per Frame:       'Select Grp' , 'Key Grp' , 'Reset Grp'    
        -Main GUI buttons:        'Select All' , 'Key All' , 'Reset All' 
        """
        self.resetAll = ''
        
        #List of GUI creation strings. Written to file
        string = []
        
        string.append('from __future__ import with_statement\n')
        string.append('from pymel.core import *\n\n') 
        
        string.append('# A utility to help switch space on an IK controller without poping.\n')
        string.append('import spaceSwitchTool\n\n')        
        
        #Get and format time string
        fullDate = time.localtime()
        date = str(fullDate[1]) + '/' + str(fullDate[2]) + '/' + str(fullDate[0])
        
        if fullDate[3] > 11:
            if fullDate[4] < 10:
                cTime = str(fullDate[3]-12) + ':0' + str(fullDate[4]) + 'pm'
            else:
                cTime = str(fullDate[3]-12) + ':' + str(fullDate[4]) + 'pm'
        else:
            if fullDate[4] < 10:
                cTime = str(fullDate[3]) + ':0' + str(fullDate[4]) + 'am'
            else:
                cTime = str(fullDate[3]) + ':' + str(fullDate[4]) + 'am'
        
        #Create the GUI file header
        string.append('"""\n')    
        string.append('# Created by: AutoGUI v%s\n'%self.version)
        string.append('# Date Created: %s\n'%date)
        string.append('# Time Created: %s\n'%cTime)
        string.append('# File Name: %s_gui.py\n' %self.frameGrps[0].guiName)
        string.append('#\n')
        string.append('# This file generates a GUI inside of Maya.\n') 
        string.append('# Load it into the script editor and run it.\n')
        string.append('"""\n\n') 
        
        #Create top GUI part

        #Create class definition:
        string.append('class %s_gui():\n'%self.frameGrps[0].guiName) 
        string.append('\t"""\n')
        string.append('\tCreate a GUI in Maya for %s\n'%self.frameGrps[0].guiName)
        string.append('\t"""\n')
                
        #__init__()
        string.append('\n\tdef __init__(self,*args):\n')
        string.append('\t\t"""\n')
        string.append('\t\tInitialize namespace variables and call buildGUI().\n')
        string.append('\t\t"""\n')
        string.append('\t\tself.currentNS = ":"\n')
        string.append('\t\tself.namespaceField = ""\n')    
        string.append('\t\tself.buildGUI()\n')           
        
        #Build_GUI()
        string.append('\n\tdef buildGUI(self,*args):\n')
        string.append('\t\t"""\n')
        string.append('\t\tBuild the Maya GUI.\n')
        string.append('\t\t"""\n')
        string.append('\t\tif(window("' + self.frameGrps[0].guiName + 'GUIWin", exists=True)):\n')
        string.append('\t\t\tdeleteUI("' + self.frameGrps[0].guiName + 'GUIWin",window=True)\n')
        string.append('\t\twith window("' + self.frameGrps[0].guiName +
                         'GUIWin",rtf=True,title="' + self.frameGrps[0].guiName + ' GUI")as win:\n')
        string.append('\n')
        
        # Tab layout
        string.append('\t\t\twith tabLayout(innerMarginWidth=5, innerMarginHeight=5) as tabs:\n')
        
        # GUI Tab
        string.append('\t\t\t\twith scrollLayout() as guiMainLayout:\n')

        string.append('\t\t\t\t\twith columnLayout():\n')
        string.append('\t\t\t\t\t\twith columnLayout():\n')
        
        #Namespace drop down menu
        string.append('\n')
        string.append('\t\t\t\t\t\t\twith rowLayout(nc=2,cw2=(50,100)):\n')
        string.append('\t\t\t\t\t\t\t\ttext("  ")\n')
        string.append('\t\t\t\t\t\t\t\tself.namespaceField = optionMenu( label="Namespace:")\n')
        string.append('\t\t\t\t\t\t\toptionMenu(self.namespaceField,edit=True,cc=self.nsChange)\n')
        string.append('\t\t\t\t\t\t\tself.addNamespaces()\n\n')
        
        #IK/FK Matching buttons
        if self.ikFkMatch == 1:
            string.append('\n')
            string.append('\t\t\t\t\t\t\twith rowLayout(nc=3,cw3=(20,100,100)):\n')
            string.append('\t\t\t\t\t\t\t\ttext("  ")\n')
            string.append('\t\t\t\t\t\t\t\tbutton(label="L_IK/FK Match",c=self.l_ikFkMatch,bgc=(0.8,0.7,0.7))\n')
            string.append('\t\t\t\t\t\t\t\tbutton(label="R_IK/FK Match",c=self.r_ikFkMatch,bgc=(0.8,0.7,0.7))\n')
        
        # Space switch utility    
        string.append('\n')
        string.append('# A utility to help switch space on an IK controller without poping.\n')
        string.append('\t\t\t\t\t\t\twith rowLayout(nc=2,cw2=(80,100)):\n')
        string.append('\t\t\t\t\t\t\t\ttext("  ")\n')
        string.append('\t\t\t\t\t\t\t\tbutton(label="Space Switch",c=spaceSwitchTool.spaceSwitchTool,bgc=(0.8,0.7,0.7))\n')

        #list of strings that define reset group functions
        self.resetGrpCmds = ''
        
        #string that defines reset all functions
        self.resetAllCmd = '\n\tdef resetAll(self,*args):\n'  
        self.resetAllCmd = self.resetAllCmd + '\t\t"""\n'  
        self.resetAllCmd = self.resetAllCmd + '\t\tReset all controller objects\n' 
        self.resetAllCmd = self.resetAllCmd + '\t\t"""\n' 
        
        #---Create custom frames
        for group in self.frameGrps:
            string.append('\t\t\t\t\t\t\t#--- %s : Custom Frame Group\n'%group.grpName)
            string.append('\t\t\t\t\t\t\twith frameLayout(label="%s",cl=True,cll=True,w=220):\n'%group.grpName)
            string.append('\t\t\t\t\t\t\t\twith columnLayout():\n')
            string.append('\n')
            

            #Define button commands
            selectCmd = [] #List of string commands to select each object.
            keyCmd = []    #List of string commands to key all keyable attributes.
            
            #Individual object buttons inside frame / group  
            counter = 0
            for obj in group.objNames:
                reset = '"'
                for name,value in zip(group.objAndAttrNames[counter],group.objDefaults[counter]):
                    reset = reset + 'setAttr(\'" + self.currentNS + "%s\',%s),'%(name,value)
                reset = reset[:-1] + '"'
                #Create command strings for the object buttons
                #selectCmd[]
                selectCmd.append( '"select(\'" + self.currentNS + "' + obj + '\', ' + 
                                    group.selType + '=True)"' )
                #keyCmd[]
                keyCmd.append( '"setKeyframe(\'" + self.currentNS + "' + obj + '\')"')
                
                #Create object buttons
                string.append('\t\t\t\t\t\t\t\t\twith rowLayout(nc=4,w=220,cw4=(100,10,50,50)):\n')
                string.append('\t\t\t\t\t\t\t\t\t\tbutton(label="'+ obj + '",c=' + selectCmd[counter] + ',w=100,bgc=(0.7,0.9,0.7))\n')
                string.append('\t\t\t\t\t\t\t\t\t\ttext(" ")\n')
                string.append('\t\t\t\t\t\t\t\t\t\tbutton(label="    Key",c=' + keyCmd[counter] + ',w=50,bgc=(0.8,0.8,0.8))\n')
                string.append('\t\t\t\t\t\t\t\t\t\tbutton(label="  Reset",c='+reset+',w=50,bgc=(0.6,0.6,0.6))\n')
                
                counter = counter + 1

            #--- Group buttons per frame
            #Create buttons out of frame so they are visible when it is collapsed.
            #SelectGrp, keyGrp and resetGrp command strings
          
            selectGrp = '"select(\'"'
            keyGrp = '"setKeyframe(\'"'
            for each in group.objNames:
                selectGrp = selectGrp + ' + self.currentNS + "' + each + '\',\'"'
            selectGrp = selectGrp[:-2] + group.selType + '=True)"' 
            
            for each in group.objNames:
                keyGrp = keyGrp + ' + self.currentNS + "' + each + '\',\'"'
            keyGrp = keyGrp[:len(keyGrp)-4] #Remove trailing comma.
            keyGrp = keyGrp + '\')"'
            
            #Generate resetGrp function string (Stored in self.resetGrpCmds)    
            self.resetGrpCmds = self.resetGrpCmds + self.resetGrp(group)
            
            string.append('\n')
            string.append('\t\t\t\t\t\t\t\t\twith rowLayout(nc=4,w=220,cw4=(10,70,70,70)):\n')
            string.append('\t\t\t\t\t\t\t\t\t\ttext(" ")\n')
            string.append('\t\t\t\t\t\t\t\t\t\tbutton(label="Select Grp",c=' + str(selectGrp) + ',w=65,bgc=(0.5,0.9,0.5))\n')
            string.append('\t\t\t\t\t\t\t\t\t\tbutton(label=" Key Grp",c=' + str(keyGrp) + ',w=65,bgc=(0.8,0.8,0.8))\n')
            string.append('\t\t\t\t\t\t\t\t\t\tbutton(label=" Reset Grp",c=self.%s_resetGrp,w=65,bgc=(0.6,0.6,0.6))\n'%group.grpName)
   
        #GUI bottom 
        selectAll = '"select(\''
        keyAll = '"setKeyframe(\''
        
        for group in self.frameGrps:
            for obj in group.objNames:
                selectAll = selectAll + '" + self.currentNS + "' + obj + '\',\''
                keyAll = keyAll + '" + self.currentNS + "' + obj + '\',\''
        selectAll = selectAll[:-1] + self.frameGrps[0].selType + '=True)"' 
        keyAll = keyAll[:-2] + ')"'

        string.append('\n\t\t\t\t\t\t\t#---Bottom of GUI: Select/Key/Reset All Buttons\n') 
        string.append('\t\t\t\t\t\t\ttext(" ")\n') 
        string.append('\t\t\t\t\t\t\tseparator(w=230)\n')
        string.append('\t\t\t\t\t\t\twith rowLayout(nc=2,w=220,cw2=(80,100)):\n')
        string.append('\t\t\t\t\t\t\t\ttext(" ")\n')
        string.append('\t\t\t\t\t\t\t\ttext("--All-- Buttons        ",font="boldLabelFont")\n')
        
        string.append('\t\t\t\t\t\t\twith rowLayout(nc=4,w=220,cw4=(10,70,70,70)):\n')
        string.append('\t\t\t\t\t\t\t\ttext(" ")\n')
        string.append('\t\t\t\t\t\t\t\tbutton(label="Select All",c=' + str(selectAll) + ',w=65,bgc=(0.3,0.9,0.3))\n')
        string.append('\t\t\t\t\t\t\t\tbutton(label=" Key All",c=' + str(keyAll) + ',w=65,bgc=(0.7,0.7,0.7))\n')
        string.append('\t\t\t\t\t\t\t\tbutton(label=" Reset All",c=self.resetAll,w=65,bgc=(0.4,0.4,0.4))\n\n')       
        
# @todo- Poses support # Poses Tab
#        string.append('\t\t\t\twith shelfTabLayout("Poses") as posesMainLayout:\n\n')
        
        string.append('\t\t\t\ttabLayout( tabs, edit=True, tabLabel=((guiMainLayout, "Selection")) )\n')
        string.append('\t\t\t\twin.show()\n\n')

#        # Exit GUI event handler scriptJob to save poses
#        string.append('\t\t\t\t# Exit GUI event handler scriptJob to save poses.\n')
#        string.append('\t\t\t\tscriptJob(uid=(win,self.savePoses))\n\n')

        #Add in the addNamespaces methods to the gui file.
        #string.append('\n    #--- Namespace methods\n')
        string.append(self.addNamespaces()) 
        string.append(self.nsChangeCmd()) 
        
        # Add ik/fk matching
        if self.ikFkMatch == 1:
            string.append(self.addIkFkMatching())

        #Add in the reset group function string   
        string.append('\n    #--- Reset methods\n')
        string.append(self.resetGrpCmds)
        
        #Add the reset all function string
        string.append(self.resetAllCmd)
        
        #Add initializing call to class
        string.append('\nwin = %s_gui()\n\n'%self.frameGrps[0].guiName)
        
#        #@todo - Add Maya 2011 GUI docking Mel code.
#        string.append('version = about(v=True)\n\n')
#        string.append('#--- Dock GUI in Maya layout if running 2011')
#        string.append('if "2011" in version:\n')
#        string.append('\twindow = win.window\n')
#
#        string.append('\tmel.eval(\'$layOut1 = `paneLayout -configuration \"single\" -parent $gMainWindow`;\')\n')
#        string.append('\tmel.eval(\'dockControl -allowedArea \"all\" -area \"right\" -floating off -content $layOut1 -label \"'+self.frameGrps[0].self.guiName+'_GUI\";\')\n')
#        string.append('\tmel.eval(\'control -e -parent $layOut1 %s;\'%window)\n')

        #Create/Open the file in location selected by user
        try:
            file = open('%s/%s_gui.py'%(self.frameGrps[0].saveDir,self.frameGrps[0].guiName),
                        'w')
        except Exception, e:
            print "Could not create: %s/%s_gui.py"%(self.frameGrps[0].saveDir,self.frameGrps[0].guiName)
            raise AutoGUIError(e)
        
        #Write string to file
        for lines in string:
            file.writelines(lines)
        
        #Close the file
        try:
            file.close()
        except:
            print "Could not close: %s/%s_gui.py"%(self.frameGrps[0].saveDir,self.frameGrps[0].guiName)

    #--- Namepace methods
    def addNamespaces(self,*args):
        """
        Return: addNamespaces() as a string
        """
        string  = []
        
        string.append('\n\tdef addNamespaces(self,*args):\n')
        string.append('\t\t"""\n')
        string.append('\t\tAdd scene namespaces to the gui namespace drop down menu.\n')
        string.append('\t\tself.namespaceField = path/name to GUI drop down menu.\n')
        string.append('\t\t"""\n')
        string.append('\t\tsceneNS = namespaceInfo(listOnlyNamespaces=True)\n')
        string.append('\n')
        string.append('\t\t#Add the current namespace to top of option menu.\n')
        string.append('\t\tmenuItem(label=self.currentNS,p=self.namespaceField)\n')
        string.append('\n')
        string.append('\t\t#Add the root namespace to option menu if its not the self.currentNS.\n')
        string.append('\t\tif self.currentNS != ":":\n')
        string.append('\t\t\tmenuItem(label=":",p=self.namespaceField)\n')
        string.append('\n')
        string.append('\t\t#Add namespaces to option menu.\n')
        string.append('\t\tfor each in sceneNS:\n' )
        string.append('\t\t\t#UI and shared are namespaces common to all scenes\n')
        string.append('\t\t\tif ("UI" in each) or ("shared" in each) or (self.currentNS[len(self.currentNS)-1] in each):\n')
        string.append('\t\t\t\tcontinue\n')
        string.append('\t\t\t#Add all other namespaces to option menu.\n')
        string.append('\t\t\telse:\n')
        string.append('\t\t\t\tmenuItem(label=each+":",p=self.namespaceField)\n\n')

        return string
    
    def nsChangeCmd(self,*args):
        """
        Return: nsChange() as a string
        """
        string  = []
        string.append('\n\tdef nsChange(self,*args):\n')
        string.append('\t\t"""\n')
        string.append('\t\tWhen user changes namespace drop down menu,\n')
        string.append('\t\trecreate the GUI and update self.currentNS\n')
        string.append('\t\twith the drop down menu item selected by user.\n')
        string.append('\t\t"""\n')
        string.append('\t\tself.currentNS = optionMenu(self.namespaceField,query=True,value=True)\n')
        string.append('\t\tself.buildGUI()\n')
        
        return string
    
    #--- Ik/Fk Matching
    def addIkFkMatching(self,*args):
        """
        Insert ik/fk matching code into string that is to be written to gui.py file.
        """
        """
        PROCESS:
        -Write switch file to Current Directory
        
        -Set FK to the IK:
                Get IK chain rotations, set FK to those values
                
        -Set IK to the FK:
                   -PointConstraint ikControl to fkWrist
                   -Delete the constraint
                   -Get distance between ik/fk elbows
                   -Get ikControl.elbow value
                   -Store original distance
                   -Add 1 to elbow.
                       if distance increases:
                           decrement elbow until distance == 0
                       if distance decreases:
                           increment elbow until distance == 0
                       
        """
        string = []
        string.append('\n\t#--- IK/FK Matching methods\n')
        string.append('\t"""\n')
        string.append('\tCreate two functions:\n')
        string.append('\t l_ikFkMatch and r_ikFkMatch.\n')
        string.append('\tThese functions switch the IK to FK, or vice versa,\n')
        string.append('\tkeeping the arm rig in place."""\n\n')
        
        #--- l_ikFkMatch()
        string.append('\tdef l_ikFkMatch(self,*args):\n') 
                            
        #Get Ik data
        string.append('\t\tikShldrRotates = xform(self.currentNS + "%s",q=True, os=True, ro=True)\n'%self.l_ikChain[0])
        string.append('\t\tikElbow1Rotates = xform(self.currentNS + "%s",q=True, os=True, ro=True)\n'%self.l_ikChain[1])
        string.append('\t\tikWristRotates = xform(self.currentNS + "%s",q=True, os=True, ro=True)\n\n'%self.l_ikChain[2])
            
        #Switching
        string.append('\t\tstate = getAttr(self.currentNS + "%s.FK_IK")\n'%self.sNames.controlNames['left_hand'])
        
        #IK to FK
        string.append('\t\t# Match Ik to Fk\n')
        string.append('\t\tif state == 0:\n')
        
        string.append('\t\t\tamount = 0\n')
        string.append('\t\t\tprogWin = progressWindow( title="Left Arm Ik/Fk Matching",\n')
        string.append('\t\t\tprogress = amount,\n')
        string.append('\t\t\tisInterruptable=True,\n')
        string.append('\t\t\tstatus="Switching Left Arm IK/FK ...")\n\n')
        
        string.append('\t\t\ttemp = pointConstraint(self.currentNS + "%s",self.currentNS + "%s",mo=False)\n' % (self.l_fkChain[2], self.sNames.controlNames['left_armIk']))
        string.append('\t\t\tdelete(temp);\n\n')
            
        string.append('\t\t\tdist = getAttr(self.currentNS + "%s.distance")\n' % self.l_distNode)
        string.append('\t\t\telbow = getAttr(self.currentNS + "%s.elbow")\n' % self.sNames.controlNames['left_armIk'])
        string.append('\t\t\tif elbow <= 0:\n')
        string.append('\t\t\t\twhile dist > 0.1:\n')
        string.append('\t\t\t\t\tif progressWindow(progWin, query=True, isCancelled=True ) :\n')
        string.append('\t\t\t\t\t\tbreak\n')
        string.append('\t\t\t\t\tprogressWindow(progWin, edit=True, step=1)\n')        
        
        string.append('\t\t\t\t\tdist = getAttr(self.currentNS + "%s.distance")\n' % self.l_distNode)
        string.append('\t\t\t\t\telbow = getAttr(self.currentNS + "%s.elbow")\n' % self.sNames.controlNames['left_armIk'])
        string.append('\t\t\t\t\tsetAttr(self.currentNS + "%s.elbow",(elbow + 0.1))\n\n' % self.sNames.controlNames['left_armIk'])
        
        string.append('\t\t\tif elbow >= 360:\n')
        string.append('\t\t\t\twhile dist > 0.1:\n')
        string.append('\t\t\t\t\tif progressWindow(progWin, query=True, isCancelled=True ) :\n')
        string.append('\t\t\t\t\t\tbreak\n')
        string.append('\t\t\t\t\tprogressWindow(progWin, edit=True, step=1)\n')    
        
        string.append('\t\t\t\t\tdist = getAttr(self.currentNS + "%s.distance")\n' % self.l_distNode)
        string.append('\t\t\t\t\telbow = getAttr(self.currentNS + "%s.elbow")\n' % self.sNames.controlNames['left_armIk'])
        string.append('\t\t\t\t\tsetAttr(self.currentNS + "%s.elbow",(elbow - 0.1))\n' % self.sNames.controlNames['left_armIk'])
        string.append('\t\t\telse:\n')
        string.append('\t\t\t\twhile dist > 0.1:\n')
        string.append('\t\t\t\t\tif progressWindow(progWin, query=True, isCancelled=True ) :\n')
        string.append('\t\t\t\t\t\tbreak\n')
        string.append('\t\t\t\t\tprogressWindow(progWin, edit=True, step=1)\n')
        
        string.append('\t\t\t\t\tdist = getAttr(self.currentNS + "%s.distance")\n' % self.l_distNode)
        string.append('\t\t\t\t\telbow = getAttr(self.currentNS + "%s.elbow")\n' % self.sNames.controlNames['left_armIk'])
        string.append('\t\t\t\t\tsetAttr(self.currentNS + "%s.elbow",(elbow - 0.1))\n\n' % self.sNames.controlNames['left_armIk'])

        string.append('\t\t\tprogressWindow(progWin, edit=True, endProgress=True)\n')
        string.append('\t\t\tsetAttr(self.currentNS + "%s.FK_IK",1 )\n\n' % self.sNames.controlNames['left_hand'])

        #FK to IK
        string.append('\t\t# Match Fk to Ik\n')
        string.append('\t\tif state == 1:\n')
        string.append('\t\t\tsetAttr(self.currentNS + "%s.rotate",ikShldrRotates[0],ikShldrRotates[1],ikShldrRotates[2])\n\n'%self.l_fkChain[0])
        
        #Only set the rotates for the non-locked elbow rotate value
        string.append('\t\t\t#Only set the rotates for the non-locked elbow rotate value.\n') 
        if self.joint_up == 1:
            string.append('\t\t\tsetAttr(self.currentNS + "%s.rotateX",ikElbow1Rotates[0])\n'%self.l_fkChain[1])
        elif self.joint_up == 2:
            string.append('\t\t\tsetAttr(self.currentNS + "%s.rotateY",ikElbow1Rotates[1])\n'%self.l_fkChain[1])
        elif self.joint_up == 3:
            string.append('\t\t\tsetAttr(self.currentNS + "%s.rotateZ",ikElbow1Rotates[2])\n'%self.l_fkChain[1])    
                                
        string.append('\t\t\tsetAttr(self.currentNS + "%s.rotate",ikWristRotates[0],ikWristRotates[1],ikWristRotates[2])\n'%self.l_fkChain[2])
        string.append('\t\t\tsetAttr(self.currentNS + "%s.FK_IK",0 )\n\n'%self.sNames.controlNames['left_hand'])
        
        #--- r_ikFkMatch()
        string.append('\tdef r_ikFkMatch(self,*args):\n') 
                            
        #Get Ik data
        string.append('\t\tikShldrRotates = xform(self.currentNS + "%s",q=True, os=True, ro=True)\n'%self.r_ikChain[0])
        string.append('\t\tikElbow1Rotates = xform(self.currentNS + "%s",q=True, os=True, ro=True)\n'%self.r_ikChain[1])
        string.append('\t\tikWristRotates = xform(self.currentNS + "%s",q=True, os=True, ro=True)\n\n'%self.r_ikChain[2])
            
        #Switching
        string.append('\t\tstate = getAttr(self.currentNS + "%s.FK_IK")\n'%self.sNames.controlNames['right_hand'])
        
        #IK to FK
        string.append('\t\tif state == 0:\n')
        
        string.append('\t\t\tamount = 0\n')
        string.append('\t\t\tprogWin = progressWindow( title="Right Arm Ik/Fk Matching",\n')
        string.append('\t\t\tprogress = amount,\n')
        string.append('\t\t\tisInterruptable=True,\n')
        string.append('\t\t\tstatus="Switching Right Arm IK/FK ...")\n')
        
        string.append('\t\t\ttemp = pointConstraint(self.currentNS + "%s",self.currentNS + "%s",mo=False)\n' % (self.r_fkChain[2], self.sNames.controlNames['right_armIk']))
        string.append('\t\t\tdelete(temp);\n\n')
            
        string.append('\t\t\tdist = getAttr(self.currentNS + "%s.distance")\n' % self.r_distNode)
        string.append('\t\t\telbow = getAttr(self.currentNS + "%s.elbow")\n' % self.sNames.controlNames['right_armIk'])
        string.append('\t\t\tif elbow <= 0:\n')
        string.append('\t\t\t\twhile dist > 0.1:\n')
        string.append('\t\t\t\t\tif progressWindow(progWin, query=True, isCancelled=True ) :\n')
        string.append('\t\t\t\t\t\tbreak\n')
        string.append('\t\t\t\t\tprogressWindow(progWin, edit=True, step=1)\n\n')        
        
        string.append('\t\t\t\t\tdist = getAttr(self.currentNS + "%s.distance")\n' % self.r_distNode)
        string.append('\t\t\t\t\telbow = getAttr(self.currentNS + "%s.elbow")\n' % self.sNames.controlNames['right_armIk'])
        string.append('\t\t\t\t\tsetAttr(self.currentNS + "%s.elbow",(elbow + 0.1))\n\n' % self.sNames.controlNames['right_armIk'])
        
        string.append('\t\t\tif elbow >= 360:\n')
        string.append('\t\t\t\twhile dist > 0.1:\n')
        string.append('\t\t\t\t\tif progressWindow(progWin, query=True, isCancelled=True ) :\n')
        string.append('\t\t\t\t\t\tbreak\n')
        string.append('\t\t\t\t\tprogressWindow(progWin, edit=True, step=1)\n')    
        
        string.append('\t\t\t\t\tdist = getAttr(self.currentNS + "%s.distance")\n' % self.r_distNode)
        string.append('\t\t\t\t\telbow = getAttr(self.currentNS + "%s.elbow")\n' % self.sNames.controlNames['right_armIk'])
        string.append('\t\t\t\t\tsetAttr(self.currentNS + "%s.elbow",(elbow - 0.1))\n' % self.sNames.controlNames['right_armIk'])
        string.append('\t\t\telse:\n')
        string.append('\t\t\t\twhile dist > 0.1:\n')
        string.append('\t\t\t\t\tif progressWindow(progWin, query=True, isCancelled=True ) :\n')
        string.append('\t\t\t\t\t\tbreak\n')
        string.append('\t\t\t\t\tprogressWindow(progWin, edit=True, step=1)\n')
        
        string.append('\t\t\t\t\tdist = getAttr(self.currentNS + "%s.distance")\n' % self.r_distNode)
        string.append('\t\t\t\t\telbow = getAttr(self.currentNS + "%s.elbow")\n' % self.sNames.controlNames['right_armIk'])
        string.append('\t\t\t\t\tsetAttr(self.currentNS + "%s.elbow",(elbow - 0.1))\n\n' % self.sNames.controlNames['right_armIk'])

        string.append('\t\t\tprogressWindow(progWin, edit=True, endProgress=True)\n')
        string.append('\t\t\tsetAttr(self.currentNS + "%s.FK_IK",1 )\n\n' % self.sNames.controlNames['right_hand'])

        #FK to IK
        string.append('\t\tif state == 1:\n')
        string.append('\t\t\tsetAttr(self.currentNS + "%s.rotate",ikShldrRotates[0],ikShldrRotates[1],ikShldrRotates[2])\n'%self.r_fkChain[0])
        
        #Only set the rotates for the non-locked elbow rotate value
        if self.joint_up == 1:
            string.append('\t\t\tsetAttr(self.currentNS + "%s.rotateX",ikElbow1Rotates[0])\n'%self.r_fkChain[1])
        elif self.joint_up == 2:
            string.append('\t\t\tsetAttr(self.currentNS + "%s.rotateY",ikElbow1Rotates[1])\n'%self.r_fkChain[1])
        elif self.joint_up == 3:
            string.append('\t\t\tsetAttr(self.currentNS + "%s.rotateZ",ikElbow1Rotates[2])\n'%self.r_fkChain[1])    
                                
        string.append('\t\t\tsetAttr(self.currentNS + "%s.rotate",ikWristRotates[0],ikWristRotates[1],ikWristRotates[2])\n'%self.r_fkChain[2])
        string.append('\t\t\tsetAttr(self.currentNS + "%s.FK_IK",0 )\n\n'%self.sNames.controlNames['right_hand'])
        
        return string
              
    #--- Reset Methods
    def resetGrp(self,group):
        """
        Returns string of a reset group function for the
        group FrameGrp object.
        """
        #Store function name in resetAllCmd:
        #Reset all: Calls all resetGrp functions, vs re-creating setAttr commands...
        self.resetAllCmd = self.resetAllCmd + '\t\tself.%s_resetGrp()\n'%group.grpName    
        
        resetStr = '\n\tdef %s_resetGrp(self,*args):\n'%group.grpName  
        resetStr = resetStr + '\t\t"""\n'  
        resetStr = resetStr + '\t\tReset all controller objects in group %s.\n'%group.grpName 
        resetStr = resetStr + '\t\t"""\n' 
        
        #Generate the string that writes the resetGrp function    
        for name,value in zip(group.objAndAttrNames,group.objDefaults):
            for n,v in zip(name,value):
                #Error catching: Like trying to set a connected attribute that was listed as keyable.
                resetStr = resetStr + '\t\ttry:\n'  
                resetStr = resetStr + '\t\t\tsetAttr(self.currentNS + "%s",%s)\n'%(n,v)
                
                resetStr = resetStr + '\t\texcept:\n'
                resetStr = resetStr + '\t\t\tpass\n'  
      
        return resetStr
    
    #--- List field methods  
    def loadList(self,list,*args):
        """
        Input:
            list = Path to textScrollList GUI object in Maya.
            
        Adds selection to the list. (textScrollList GUI object in Load
                                              Controls main GUI.)
                                              
        Returns: "Load Selection" command string for the given list. 
        """
        cmdString = 'from pymel.core import *\n'
        cmdString = cmdString + 'sel = ls(sl=True,fl=True)\n'
        cmdString = cmdString + 'for each in sel:\n'
        cmdString = cmdString + '    textScrollList("%s",e=True,a=each)'%list 
        
        return cmdString
        
    def resetList(self,list,*args):
        """
        Input:
            list = Path to textScrollList GUI object in Maya.
            
        Returns: "Reset Command" string for the given list.
        """
        cmdString = 'from pymel.core import *\n'
        cmdString = cmdString + 'textScrollList("%s",e=True,ra=True)'%list
        
        return cmdString
   
    def removeListItem(self,list,*args):
        """
        Input:
            list = Path to textScrollList GUI object in Maya.
        
        Returns: "Remove Selected Item" from the list.
        """
        cmdString = 'from pymel.core import *\n'
        cmdString = cmdString + 'selected = textScrollList("%s",q=True,si=True)\n'%list   
        cmdString = cmdString + 'try:\n'
        cmdString = cmdString + '    for each in selected:\n'
        cmdString = cmdString + '        textScrollList("%s",e=True,ri=each)\n'%list
        cmdString = cmdString + 'except:\n'
        cmdString = cmdString + '    pass\n'
        
        return cmdString
    



    
        
        
        
        
