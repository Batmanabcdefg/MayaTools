from __future__ import with_statement # This line is only needed for 2008 and 2009
from pymel.core import *

import os as os
import sys


"""
Copyright (c) 2010, Mauricio Santos-Hoyos
Name: ms_toolBox.py
Author: Mauricio Santos-Hoyos
Contact: mauricioptkvp@hotmail.com
Version: 1.01
Description:
       Given a directory,
       create a formLayout with buttons that launch
       each .py and/or .pyc file in the directory.

To do:
    Generated window:
        -Dockable
            Can reorient vertically or horizontally to dock
        -Remember previous settings
        -Support tabs (multiple directories, aka shelves)
        -Rescan directory for new files on open.

    Functionality:
        -Shelves:
            What are they:
                A tab inside of a user created

            Recreate any user saved data and create buttons for all .py scripts in the directory
            using the options selected on initial shelf creation.

        -Add shelf:
            Get directory and options from user.
            Create new tab in name_mshToolBox.
                -Opens: dir/name_mshToolBox.py
                -Writes tab to 'name_mshToolBoxWin'
                -Close name_mshToolBox.py


        -Save/Delete shelves:

            Auto save on close: Won't kill user if they forget to save after performing changes,
                like adding poses, or script buttons

            Determine how to save shelf data:

                 Python:
                     shelves/pickles?
                     Object Database (SQLAlchemy)

                name_toolBox.(py,xml,dbm,c++,java..?) = Write data to recreate windows in the state that
                 the user last closed the window.


            Determine where to save shelf data:

                TEMP_DIR = ?
                    -Write name_toolBox.(py,xml,dbm,...) to Maya's temp dir?
                                    OR
                    -Write name_toolBox.py to maya.env SCRIPTS_DIR / ( project/Tools/internal/ directory )

                Add button to shelf:

                    import name_mshToolBox
                    reload( name_mshToolBox ) (optional)
                    name_mshToolBox.name_mshToolBox()



History:
    2010-10-03 : Initial creation.
    2010-10-08 : Added PYTHONPATH option.
    2010-10-16 : Added multiple window support. Window naming based on directory name.


Procedure:
    HOLD-Prompt user for number of directories (num)
    -Prompt user for actual directory.
    -Create main window
    -HOLD(For each directory,) create a tab/forLayout with buttons

Dev notes:

"""

class ms_toolBox():
    """
       Given a directory,
       create a formLayout with buttons that launch
       each .py and/or .pyc file in the directory.
    """
    def __init__(self,*args):
        """
            Prompt user for option and directory.
        """
        if(window('ms_toolBoxWin1',exists=True)):
            deleteUI('ms_toolBoxWin1',window=True)

        with window('ms_toolBoxWin1',title='Tool Box v1.0') as mainWin:
            with formLayout() as form:
                    self.reloadField = radioButtonGrp(label='Add reload line?:',nrb=2,labelArray2=('no','yes'),sl=2)
                    self.pathField = radioButtonGrp(label='Add to PYHTONPATH?:',nrb=2,labelArray2=('no','yes'),sl=2)
                    self.typeField = radioButtonGrp(label='File type:',nrb=3,labelArray3=('.py','.pyc','both'),sl=1)
                    self.dirField = textFieldButtonGrp(label='Directory:',bl='Browse',bc=self.getDir,
                                                       text='/pipeline_folder/GoogleDrive/MayaTools/SingleFiles')

                    with rowLayout(nc=2,cw2=(200,80)):
                        text(' ')
                        button(label='Open Tool Box',bgc=(0.3,0.9,0.3),c=self.buildToolBox)
                    form.redistribute()
            mainWin.show()

    def buildToolBox(self,*args):
        """
            Create window with a tab>formLayout panel with
            buttons to every python script in a given directory.
        """
        directory = textFieldButtonGrp(self.dirField,query=True,text=True)
        type = radioButtonGrp(self.typeField,query=True,sl=True)
        reload = radioButtonGrp(self.reloadField,query=True,sl=True)
        pathOption = radioButtonGrp(self.pathField,query=True,sl=True)

        #Get directory contents
        files = os.listdir(directory)

        #Get folder name
        temp = os.path.split(directory)
        dirName = temp[1]

        pyFiles = []
        for each in files:
            if type == 1:
                if '.py' in each and '.pyc' not in each:
                    pyFiles.append(each)
            elif type == 2:
                if '.pyc' in each:
                    pyFiles.append(each)
            elif type == 3:
                if '.py' in each or '.pyc' in each:
                    pyFiles.append(each)

        if(window('%s_MainWin'%dirName, exists=True)):
            deleteUI('%s_MainWin'%dirName,window=True)

        with window('%s_MainWin'%dirName,title='%s Tool Box'%dirName,rtf=True) as mainWin:
            with scrollLayout():
                with formLayout() as form:
                    for each in pyFiles:
                        if reload == 1:
                            label = each.split('.')
                            button(label=label[0],command='import %s as xx\nxx.%s()'%(label[0],label[0]))
                        else:
                            label = each.split('.')
                            button(label=label[0],command='import %s as xx\nreload(xx)\nxx.%s()'%(label[0],label[0]))
                    form.redistribute()
            mainWin.show()

        #Add to PYTHONPATH
        if pathOption == 2:
            self.addToPath(directory)

    def addToPath(self,directory):
        """
         Add directory to PYTHONPATH for this session.
        """
        sys.path.append(directory)

    def getDir(self,*args):
        """
         prompt user to browser for directory.
        """
        dir = promptForFolder()
        textFieldButtonGrp(self.dirField,edit=True,text=dir)

