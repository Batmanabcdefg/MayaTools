from __future__ import with_statement # This line is only needed for 2008 and 2009
from pymel.core import *

################################################################################
#   Copyright (c) 2010 Mauricio Santos
#   Name:       AutoGUI
#   Author:     $Author: mauricio $
#   Revised on: $Date: 2011-08-06 19:23:09 -0700 (Sat, 06 Aug 2011) $
#   Added On:   7/10/2010
#   SVN Ver:    $Revision: 131 $
#   File:       $HeadURL: file:///Users/mauricio/SVN_Repos/Maya_Tools/trunk/Tools/Rigging/General/ms_AutoGUI.py $
#   Description:
#        Creates a customizable GUI for any items the user selects.
#
#   History:    2010-07-07 - Initial creation
#   History:    2010-10-03 - Begin refactoring with PyMEL
#                
################################################################################
__author__ = "Mauricio Santos"

"""
To do:
    -Add: Select all geometry list   ----> Select all geometery button for points caching.
    -Add: GUI shelf button icon selection field.   
    -Add: Selection Type drop down menu, vs having to choose only one. Simlar to namespace.

Dev Notes:
    Left off refactoring at: writeFile()
    
Additional Notes:
    Known issues: 
        A controller that is not uniquely named will not work with this script.
        All attributes with incoming connections should be locked and hidden. 
"""
import pydoc
import time


class FrameGrp():
    """
    Stores the data from a custom GUI creation group, i.e. L_Arm group.
    Used to generate gui.py file.
    
    Methods:
        createDictionary(keys,values) #Creates dictionry of key/value pairs.
        
    Properties:
        self.objNames = []          #List of objects in gui group scroll list
        self.objAttrNames = []      #2D List of attr names per object [object[attrs]]
        self.objDefaults = []       #2D List of attr names per object [attr[values]]
        self.objAndAttrNames = []   #List of "objName.attr" per attr, per object.
        self.grpName = ''           #Name of the the specific GUI group.
        self.guiName = ''           #Name entered by user for the GUI.
        self.selType = ''           #Selection type chosen by user.
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


class ms_AutoGUI():
    """
    The main method to create GUI / write gui.py file
    """
    def __init__(self,*args):
        """
        Initial prompt: How many GUI groups?
        """  
        # Version number
        self.version = 1.0
        
        #start prompt
        if(window("autoGUIWin",exists=True)):
            deleteUI("autoGUIWin",window=True)
            
        with window("autoGUIWin",rtf=True,title="Auto GUI v1.0") as mainWin:
            with columnLayout():
                #Number of GUI groups
                with rowLayout(nc=2,cw2=(20,100)):
                    text(' ')
                    self.groupNumField = intFieldGrp(label="Number of GUI groups:",value1=2)
                
                #Save to directory
                self.dirField = cmds.textFieldButtonGrp(label='  Save to directory:',bl='Browse',
                                                  cw2=(100,200),
                                                  bc=self.loadDir,
                                                  text='C:/Users/mauricio/Desktop')
            
                #Continue button
                with rowLayout(nc=2,cw2=(100,100)):
                    cmds.text(' ')
                    cmds.button(label="     -=Continue=-",c=self.contolListGUI,w=100,bgc=(0.4,0.9,0.4))
            
            mainWin.show()
    
    def loadDir(self,*args):
        dir = promptForFolder()
        textFieldButtonGrp(self.dirField,e=True,text=dir)
        
    def contolListGUI(self,*args):
        """
        Display the scroll list(s) where the user loads items 
        they want to create the GUI for.        
        """
        #--- Initialize variables
        self.saveToDir = cmds.textFieldGrp(self.dirField,query=True,text=True)
        self.guiGrpList = []        #Holds paths to GUI text scroll lists.
        self.guiGrpNameFields = []  #Holds name fields for each group name that the user entered.
        
        # Store the number of groups the user has entered, 
        # then destroy the useless window that once had value!Ha ha!
        numGrps = intFieldGrp(self.groupNumField,query=True,value1=True)
        deleteUI("autoGUIWin",window=True)
        
        if(window("controlListWin",exists=True)):
            deleteUI("controlListWin",window=True)
            
        with window("controlListWin",rtf=True,title="Auto GUI v1.1") as mainWin:
        
            with scrollLayout(horizontalScrollBarThickness=16,
                            verticalScrollBarThickness=16):
                with columnLayout():
                    #GUI Name
                    self.guiNameField = textFieldGrp(label='GUI Name:',w=300,cw2=(100,100),text='Troll')
                    
                    #Selection Type option
                    self.selectionRB = radioButtonGrp(label='Selection Type:',nrb=3, 
                                                labelArray3 = ('add','tgl','replace'),
                                                sl=3,vr=True,cw2=(100,60))
                    #---Groups
                    count = 0
                    while(count < numGrps):
                        # Make sure first group is expanded
                        exp = ''
                        if count == 0: 
                            exp = False                         
                        else:
                            exp = True
                        
                        with frameLayout(label="Group %s"%(count+1),cl=exp,cll=True,w=210):
                            with columnLayout():
                                text("Enter Group Name:")
                        
                                #Name fields and text scroll list fields
                                self.guiGrpNameFields.append(textField(w=200))
                                self.guiGrpList.append(textScrollList(numberOfRows=25, w=200, ams = True))
                                
                                #Format functions as strings for list buttons
                                loadCmd = self.loadList(self.guiGrpList[count])
                                resetCmd = self.resetList(self.guiGrpList[count])
                                removeItemCmd = self.removeListItem(self.guiGrpList[count])
                                
                                button(label="     Load ", c = loadCmd,w=200)
                                button(label="     Reset", c = resetCmd,w=200)
                                button(label="     Remove", c = removeItemCmd,w=200)
                                                                
                                count = count + 1
            
                    #Continue button
                    button(label="-=Create GUI=-",c=self.createObjects,w=200,bgc=(0.4,0.9,0.4))
            
            #Show Window
            mainWin.show()
    
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
            self.guiName = ''           #Name entered by user for the GUI.
            self.selType = ''           #Selection type chosen by user.
            self.saveDir = ''           #Path to user selected save to directory for GUI file.
        
        Note: Namespaces: This can be a built in aspect of the script when 
            generating final object names for file output.
        """
        #Initializing variables
        guiName = textFieldGrp(self.guiNameField,q=True,text=True)
        selectionVal = radioButtonGrp(self.selectionRB,q=True,sl=True)
        self.frameGrps = []  #List of FrameGrp data objects
        
        if(selectionVal == 1):
            selType = 'add'
        if(selectionVal == 2):
            selType = 'tgl'
        if(selectionVal == 3):
            selType = 'replace'
        
        #Get the group names into a list
        grpNames = []
        count = 0
        for each in self.guiGrpNameFields:
            grpNames.append( textField('%s'%each,query=True,text=True))
        
        #For each group, create a FrameGrp object and store the data.
        count = 0            
        for list,name in zip(self.guiGrpList,grpNames):
            
            #Create FrameGrp Object
            frameGrpObj = FrameGrp() 
            
            #Save to dir
            frameGrpObj.saveDir = self.saveToDir
            
            #Store gui name
            frameGrpObj.guiName = guiName
            
            #Store "obj_name" 's for all controller in group
            fullPathNames = []
            frameGrpObj.objNames = textScrollList(list,query=True,ai=True)

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
            frameGrpObj.selType = selType
            
            #Add to list of groups (FrameGrp objects)
            self.frameGrps.append(frameGrpObj)
            
            #Write the file
            self.writeFile()
            
        #Delete the build window
        deleteUI("controlListWin",window=True)
        
    def writeFile(self,*args):
        """
        Now, armed with self.frameGrps, we write the file.
        
        GUI notes:
        -Buttons per Control:       'Select'     , 'Key'     , 'Reset'
        -Buttons per Frame:       'Select Grp' , 'Key Grp' , 'Reset Grp'    
        -Main GUI buttons:        'Select All' , 'Key All' , 'Reset All' 
        """
        date = time.localtime()
        date = str(date[1]) + '/' + str(date[2]) + '/' + str(date[0])

        self.resetAll = ''
        
        #List of GUI creation strings. Written to file
        string = []
        
        string.append('from __future__ import with_statement\n')
        string.append('from pymel.core import *\n\n')        
        
        #Create the GUI file header
        string.append('# Created by: AutoGUI v%s\n'%self.version)
        string.append('# Created on: %s\n'%date)
        string.append('# File Name: %s_gui.py\n' %self.frameGrps[0].guiName)
        string.append('#\n')
        string.append('# This file generates a GUI inside of Maya.\n') 
        string.append('# Load it into the script editor and run it.\n\n\n')
        
        #Create top GUI part

        #Create class definition:
        string.append('"""\n')
        string.append('Create a GUI in Maya for %s\n'%self.frameGrps[0].guiName)
        string.append('"""\n')
        string.append('class %s_gui():\n'%self.frameGrps[0].guiName) 
                
        #__init__()
        string.append('\n    def __init__(self,*args):\n')
        string.append('        """\n')
        string.append('        Initialize namespace variables and call buildGUI().\n')
        string.append('        """\n')
        string.append('        self.currentNS = ":"\n')
        string.append('        self.namespaceField = ""\n')    
        string.append('        self.buildGUI()\n')           
        
        #Build_GUI()
        string.append('\n    def buildGUI(self,*args):\n')
        string.append('        """\n')
        string.append('        Build the Maya GUI.\n')
        string.append('        """\n')
        string.append('        if(window("' + self.frameGrps[0].guiName + 'GUIWin", exists=True)):\n')
        string.append('            deleteUI("' + self.frameGrps[0].guiName + 'GUIWin",window=True)\n')
        string.append('        with window("' + self.frameGrps[0].guiName +
                         'GUIWin",rtf=True,title="' + self.frameGrps[0].guiName + ' GUI")as win:\n')
        string.append('\n')
        string.append('            with scrollLayout():\n')
        string.append('                with columnLayout():\n')
        
        #Namespace drop down menu
        string.append('\n')
        string.append('                    with rowLayout(nc=2,cw2=(50,100)):\n')
        string.append('                        text("  ")\n')
        string.append('                        self.namespaceField = optionMenu( label="Namespace:")\n')
        string.append('                    optionMenu(self.namespaceField,edit=True,cc=self.nsChange)\n')
        string.append('                    self.addNamespaces()\n\n')
        
        #list of strings that define reset group functions
        self.resetGrpCmds = ''
        
        #string that defines reset all functions
        self.resetAllCmd = '\n    def resetAll(self,*args):\n'  
        self.resetAllCmd = self.resetAllCmd + '        """\n'  
        self.resetAllCmd = self.resetAllCmd + '        Reset all controller objects\n' 
        self.resetAllCmd = self.resetAllCmd + '        """\n' 
        
        #---Create custom frames
        for group in self.frameGrps:
            string.append('                    #--- %s : Custom Frame Group\n'%group.grpName)
            string.append('                    with frameLayout(label="%s",cl=True,cll=True,w=220):\n'%group.grpName)
            string.append('                        with columnLayout():\n')
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
                string.append('                            with rowLayout(nc=4,w=200,cw4=(100,10,50,50)):\n')
                string.append('                                button(label="'+ obj + '",c=' + selectCmd[counter] + ',w=100,bgc=(0.7,0.9,0.7))\n')
                string.append('                                text(" ")\n')
                string.append('                                button(label="    Key",c=' + keyCmd[counter] + ',w=50,bgc=(0.8,0.8,0.8))\n')
                string.append('                                button(label="  Reset",c='+reset+',w=50,bgc=(0.6,0.6,0.6))\n')
                
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
            string.append('                            with rowLayout(nc=4,w=200,cw4=(10,70,70,70)):\n')
            string.append('                                text(" ")\n')
            string.append('                                button(label="Select Grp",c=' + str(selectGrp) + ',w=65,bgc=(0.5,0.9,0.5))\n')
            string.append('                                button(label=" Key Grp",c=' + str(keyGrp) + ',w=65,bgc=(0.8,0.8,0.8))\n')
            string.append('                                button(label=" Reset Grp",c=self.%s_resetGrp,w=65,bgc=(0.6,0.6,0.6))\n'%group.grpName)
   
        #GUI bottom 
        selectAll = '"select(\''
        keyAll = '"setKeyframe(\''
        
        for group in self.frameGrps:
            for obj in group.objNames:
                selectAll = selectAll + '" + self.currentNS + "' + obj + '\',\''
                keyAll = keyAll + '" + self.currentNS + "' + obj + '\',\''
        selectAll = selectAll[:-1] + self.frameGrps[0].selType + '=True)"' 
        keyAll = keyAll[:-2] + ')"'

        string.append('\n              #---Bottom of GUI: Select/Key/Reset All Buttons\n') 
        string.append('                text(" ")\n') 
        string.append('                separator(w=230)\n')
        string.append('                with rowLayout(nc=2,w=200,cw2=(80,100)):\n')
        string.append('                    text(" ")\n')
        string.append('                    text("--All-- Buttons        ",font="boldLabelFont")\n')
        
        string.append('                with rowLayout(nc=4,w=200,cw4=(10,70,70,70)):\n')
        string.append('                    text(" ")\n')
        string.append('                    button(label="Select All",c=' + str(selectAll) + ',w=65,bgc=(0.3,0.9,0.3))\n')
        string.append('                    button(label=" Key All",c=' + str(keyAll) + ',w=65,bgc=(0.7,0.7,0.7))\n')
        string.append('                    button(label=" Reset All",c=self.resetAll,w=65,bgc=(0.4,0.4,0.4))\n')       

        string.append('            showWindow("' + group.guiName + 'GUIWin")\n')

        #Add in the addNamespaces methods to the gui file.
        string.append('\n    #--- Namespace methods\n')
        string.append(self.addNamespaces()) 
        string.append(self.nsChangeCmd()) 
        
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
#        string.append('\tmel.eval(\'dockControl -allowedArea \"all\" -area \"right\" -floating off -content $layOut1 -label \"'+self.frameGrps[0].guiName+'_GUI\";\')\n')
#        string.append('\tmel.eval(\'control -e -parent $layOut1 %s;\'%window)\n')

        #Create/Open the file in location selected by user
        try:
            file = open('%s/%s_gui.py'%(self.frameGrps[0].saveDir,self.frameGrps[0].guiName),
                        'w')
        except:
            print "Could not create: %s/%s_gui.py"%(self.frameGrps[0].saveDir,self.frameGrps[0].guiName)
        
        #Write string to file
        file.writelines(string)
        
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
        string = '\n    def addNamespaces(self,*args):\n'
        string = string + '        """\n'
        string = string + '        Add scene namespaces to the gui namespace drop down menu.\n'
        string = string + '        self.namespaceField = path/name to GUI drop down menu.\n'
        string = string + '        """\n'
        string = string + '        sceneNS = namespaceInfo(listOnlyNamespaces=True)\n'
        string = string + '\n'
        string = string + '        #Add the current namespace to top of option menu.\n'
        string = string + '        menuItem(label=self.currentNS,p=self.namespaceField)\n'
        string = string + '\n'
        string = string + '        #Add the root namespace to option menu if its not the self.currentNS.\n'
        string = string + '        if self.currentNS != ":":\n'
        string = string + '            menuItem(label=":",p=self.namespaceField)\n'
        string = string + '\n'
        string = string + '        #Add namespaces to option menu.\n'
        string = string + '        for each in sceneNS:\n' 
        string = string + '            #UI and shared are namespaces common to all scenes\n'
        string = string + '            if ("UI" in each) or ("shared" in each) or (self.currentNS[len(self.currentNS)-1] in each):\n'
        string = string + '                continue\n'
        string = string + '            #Add all other namespaces to option menu.\n'
        string = string + '            else:\n'
        string = string + '                menuItem(label=each+":",p=self.namespaceField)\n'

        return string
    
    def nsChangeCmd(self,*args):
        """
        Return: nsChange() as a string
        """
        string = '\n    def nsChange(self,*args):\n'
        string = string + '        """\n'
        string = string + '        When user changes namespace drop down menu,\n'
        string = string + '        recreate the GUI and update self.currentNS\n'
        string = string + '        with the drop down menu item selected by user.\n'
        string = string + '        """\n'
        string = string + '        self.currentNS = optionMenu(self.namespaceField,query=True,value=True)\n'
        string = string + '        self.buildGUI()\n'
        
        return string
                
    #--- Reset Methods
    def resetGrp(self,group):
        """
        Returns string of a reset group function for the
        group FrameGrp object.
        """
        #Store function name in resetAllCmd:
        #Reset all: Calls all resetGrp functions, vs re-creating setAttr commands...
        self.resetAllCmd = self.resetAllCmd + '        self.%s_resetGrp()\n'%group.grpName    
        
        resetStr = '\n    def %s_resetGrp(self,*args):\n'%group.grpName  
        resetStr = resetStr + '        """\n'  
        resetStr = resetStr + '        Reset all controller objects in group %s.\n'%group.grpName 
        resetStr = resetStr + '        """\n' 
        
        #Generate the string that writes the resetGrp function    
        for name,value in zip(group.objAndAttrNames,group.objDefaults):
            for n,v in zip(name,value):
                #Error catching: Like trying to set a connected attribute that was listed as keyable.
                resetStr = resetStr + '        try:\n'  
                resetStr = resetStr + '            setAttr(self.currentNS + "%s",%s)\n'%(n,v)
                
                resetStr = resetStr + '        except:\n'
                resetStr = resetStr + '            pass\n'  
      
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
    
#---Update documentation: Send .html docs to location (Can be online) <--- Latest docs always published


#Learning notes: if __name__ == '__main__': guard (Needs verification)
#
#    When this file(module) is executed, a Main thread(process) is spawned for this code to "run", like a small child, frollicking away
#    into an unknow future. There may be giant bugs in it's way that it must happilly obliderate...
#    Thus the caller is identified as '__main__' because main == root of the thread.
#    So a form of execution hierarchy is formed, like namespaces in Maya, or C++, except
#    that they're not paths to an object, but paths to a process: __main__:swapLines.
#    The actual execution is assumed to be parallel to all other __main__ level processes,
#    within this Python interpreter process, which is running inside the Maya process.

#Only if executed as a script
#if __name__ == '__main__':


    
        
        
        
        
