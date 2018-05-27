################################################################################
#   copyright (c) 2010, Mauricio Santos
#   Name:       SmartOpen
#   Author:     $Author: mauricio $
#   Revised on: $Date: 2011-08-06 19:23:09 -0700 (Sat, 06 Aug 2011) $
#   Added On:   6/10/2010
#   SVN Ver:    $Revision: 131 $
#   File:       $HeadURL: file:///Users/mauricio/SVN_Repos/Maya_Tools/trunk/Tools/Rigging/General/SmartOpen.py $
#   Description:
#               Opens a Maya file, changing the version required to the 
#               version of Maya that is running. It also chenges any referenced
#               files as well.
#
#   History:    2010-06-25 - Initial creation
#               2010-07-04 - Fixed bug with accounting for spaces in reference 
#                            file paths in .ma file. 
#                            Added helper function: buildRefPath()
################################################################################

__author__ = 'Mauricio Santos'

"""
Dev Notes:
    Low Priority: Need to add support for Maya 2011

"""

import maya.cmds as cmds
import fileinput
import shutil as sh
import os

class SmartOpen():
    """
    Opens a Maya file, changing the version required to the 
    version of Maya that is running. It also chenges any referenced
    files as well.
    """
    def __init__(self,*args):
        """
        Initialize the Maya gui.
        """
        if(cmds.window("SmartOpenWin", exists=True)):
            cmds.deleteUI("SmartOpenWin", window=True)
        cmds.window("SmartOpenWin", title="Smart Open",menuBar=True,                                   
                                                        rtf=1,w=200,h=300)
        
        cmds.columnLayout()
        
        cmds.frameLayout(cl=True,cll=True,l="About",w=300)
        cmds.columnLayout()
        cmds.text('   ')
        cmds.text('   Select Maya .ma file to open. The file will be edited')
        cmds.text('   if it requires a different version of Maya than the one')
        cmds.text('   currently running so that it can be open by the current')
        cmds.text('   version.')
        cmds.text('   ')
        cmds.text('   ')
        cmds.text('   You may be prompted by SmartOpen and Maya to find a') 
        cmds.text('   reference file. This is normal.')
        cmds.text('   ')
        cmds.text('   ')
        cmds.text('   All reference files in the file will also be') 
        cmds.text('   updated.')
        cmds.text('   ')
        cmds.text('   Does not support Maya 2011.')
        cmds.text('   ')
        cmds.setParent('..')
        cmds.setParent('..')
        
        self.fileField = cmds.textFieldButtonGrp(l='File',bl="Browse",
                                                 bc=self.pickFile,ed=False,
                                                 cw3=[50,200,100])
        
        cmds.rowLayout(nc=2,cw2=(100,100))
        cmds.text('..')
        cmds.button(l='           Open',c=self.openFile,w=100)
        cmds.setParent('..')

        cmds.showWindow("SmartOpenWin")
        
    def pickFile(self,*args):
        """
        File chooser dialog
        """
        file = cmds.fileDialog(title='Open Maya file',dm='*.ma')
        cmds.textFieldButtonGrp(self.fileField,edit=True,fileName=file,ip=0)
        
    def openFile(self,*args):
        """
        Open the Maya file, changing the version required to the curent 
        version of Maya, as well as for any reference files.
        """
        file = cmds.textFieldButtonGrp(self.fileField,query=True,text=True)
        
        cmds.deleteUI("SmartOpenWin",window=True)
        
        #Check the file
        self.swapLines(file)
        
        #Check reference files and change them if needed.
        self.getRefFiles(file)

        #Open the file
        cmds.file(file,force=True,type='mayaAscii',open=True)
        
    def swapLines(self,file):
        """
        In given file.ma:
        Changes the "requires maya "version" into the running version of Maya
        """
        version = cmds.about(v=True)
        
        #Check for file validity
        if not os.path.isfile(file):
            file = self.promptForFile(file)
        
        if('2008' in version):
            replaceLine_1 = 'requires maya "2010";'    
            replaceLine_2 = 'requires maya "2009";'     
            insertLine = 'requires maya "2008";' 
        if('2009' in version):
            replaceLine_1 = 'requires maya "2010";'    
            replaceLine_2 = 'requires maya "2008";'     
            insertLine = 'requires maya "2009";'
        if('2010' in version):
            replaceLine_1 = 'requires maya "2008";'    
            replaceLine_2 = 'requires maya "2009";'     
            insertLine = 'requires maya "2010";'
        """
        if('2011' in version):
            replaceLine_1 = 'requires maya  "2010";'    
            replaceLine_2 = 'requires maya "2009";'     
            insertLine = 'requires maya "2011";'
        """
        changed = 0
        for line in fileinput.input(file,inplace=1):
            if line.strip().startswith(replaceLine_1):
                line = line.replace(replaceLine_1,insertLine)  
                changed = 1         
            elif line.strip().startswith(replaceLine_2):
                line = line.replace(replaceLine_2,insertLine)
                changed = 1
            print line,
        
        fileinput.close() 

        if changed:
            print "Updated: " + file
        else:
            print "Update not required: " + file
   
    def getRefFiles(self,file,*args):
        """
        Scan .ma file for reference file names.
        Prompt the user to browse to them if their path is invalid.
        """
        version = cmds.about(v=True)
        rootFile = open(file,'r')
        
        refLines = []
        refFiles = []
        
        for line in rootFile:
            if line.strip().startswith('file -rdi'):
                refLines.append(line)
        
        count = 0
        refPath = ""
        for each in refLines:        
            temp1 = refLines[count].split()
            #No spaces in path name
            if len(temp1) == 7:
                refPath = temp1[7][1:-2]
            #Spaces in path name
            if len(temp1) > 7:
                refPath = self.buildRefPath(temp1)
            refFiles.append(refPath)
            count = count + 1
            
        for each in refFiles:
            print each
            self.editRef(each)
            
    def buildRefPath(self,path):
        """
        Given fragmanet of a path produced by a split method, this pieces 
        them back together, preserving the spaces. 
        This assumes a constant format in all .ma files.
        """
        count = 0
        fixed = ""
        for each in path:
            if count >= 7:
                fixed = fixed + " " + each
            count = count + 1
        return fixed 
            
    def editRef(self,file):
        """
        Edit reference file if needed.
        """
        self.swapLines(file)
    
    def promptForFile(self,file):
        """
        When a file is not found, this method asks the user to find it.
        """
        temp = os.path.split(file)
        file = cmds.fileDialog(title='Please Find Reference File: %s'%temp[1][:-2],dm='*.ma')
        return file
        
            
        
        
        
        
        
        
        
        
        
        
        
        
        
        