################################################################################
#   copyright (c) 2010, Mauricio Santos
#   Name:       BlastMaster_GUI
#   Author:     $Author: mauricio $
#   Revised on: $Date: 2011-08-06 19:23:09 -0700 (Sat, 06 Aug 2011) $
#   Added On:   6/10/2010
#   SVN Ver:    $Revision: 131 $
#   File:       $HeadURL: file:///Users/mauricio/SVN_Repos/Maya_Tools/trunk/Tools/Rigging/General/BlastMaster_GUI.py $
#   Description:
#               GUI for BlastMaster. Builds GUI then it calls:
#        BlastMaster.py + BlastMaster_Options.py
#
#   History:    2010-06-09 - Initial creation
#                2010-06-12 - Finalized first release
#                2010-07-08 - No more Seq/Shot/Take fields. Using file name only.
#                             Renaming output playblast files to: "filename.cam.mov"
################################################################################

__author__ = 'Mauricio Santos'

import maya.cmds as cmds
import BlastMaster as bm
import os
reload(bm) #Remove after development done

"""
Dev notes:
    TODO:
    Call to ALE Master/Take Master... pending
   
    GUI fields:
        self.sequenceField 
        self.shotField 
        self.takeField 
        self.nameField 
        self.commentField
        
        self.camMenu 
        self.phaseMenu 
        self.dirField
"""

#Gloabl variables
options_checkBoxes = []

class BlastMaster_GUI:
    """
        Generates a production standard play blast
        Hold-Create copy of .ma play blasted
        Call ALE Master ---> Create ALE file
        Hold-Call Take Master ---> Commit take        
    """    
    def __init__(self,*args):
        #Create/Store/Load persistent node data, node: 'TG_BM_NODE'
        self.tg_bmNode()
        #Build/Display the GUI
        self.buildGUI()

    def buildGUI(self,*args):
        """
        Create the Maya GUI
        """
        if(cmds.window("BlastMasterWin", exists=True)):
            cmds.deleteUI("BlastMasterWin", window=True)
        cmds.window("BlastMasterWin", title="Blast Master",menuBar=True, rtf=1,w=200,h=300)

        ###Help Menu
        cmds.menu( label='Help', helpMenu=True )
        cmds.menuItem( 'Wiki Link', 
           label='Wiki Help: http://www.crudephysics.com/greeksWiki/index.php?title=BlastMaster',
           annotation="Displays online help URL.")        
        
        cmds.columnLayout()
        
        cmds.text(' ')
        self.nameField = cmds.textFieldGrp(label='Artist Name:',
                                        cl2=('right','right'),cw2=(90,100))
        
        #Saving absolute dag paths to layout objects for Form layout placement
        slateLayout = cmds.rowLayout(nc=2,cw2=(5,100))
        cmds.text(' ')
        self.commentField = cmds.textFieldGrp(label='   Slate Comment:'
                                              ,cw2=(85,200))
        cmds.setParent('..')


        cmds.text(' ')
        cameraLayout = cmds.rowLayout(nc=2,cw2=(50,100))
        cmds.text(' ')
        self.camMenu = cmds.optionMenu( label='Camera:')
        self.addCameras()
        cmds.setParent('..')
        
        phaseLayout = cmds.rowLayout(nc=2,cw2=(50,100))
        cmds.text(' ')
        self.phaseMenu = cmds.optionMenu( label='Phase: ')
        cmds.menuItem( label='Layout' )
        cmds.setParent('..')

        cmds.text(' ')
        self.dirField = cmds.textFieldGrp(label='  Save to directory:',
                                          cw2=(110,220),
                                          text=cmds.workspace(query=True,dir=True))

        self.imageField = cmds.textFieldButtonGrp(label='16_9_overscan.png:',
                                                  bl='Browse',
                                                  bc=self.loadImageDir,
                                                  cw3=(110,200,100))
        self.slateField = cmds.textFieldButtonGrp(label='Slate.png:',
                                                  bl='Browse',
                                                  bc=self.loadSlateDir,
                                                  cw3=(110,200,100))

        cmds.text(' ')
        buttonLayout = cmds.rowLayout(nc=2,cw2=(130,100))
        cmds.text(' ')
        cmds.button(label='        Play Blast',command=self.playBlast,w=100)
        cmds.setParent('..')

        #Layout onto the form layout
        """
        cmds.formLayout(form, edit=True,
            attachForm = [(self.sequenceField,'left',5),
                          (self.sequenceField,'right',5),
                          (self.shotField, 'left',5),
                          (self.shotField,'right',5),
                          (self.takeField, 'left',5),
                          (self.takeField,'right',5),
                          (self.nameField, 'left',5),
                          (self.nameField,'right',5),
                          (slateLayout, 'left',5),
                          (slateLayout,'right',5),
                          (cameraLayout, 'left',5),
                          (cameraLayout,'right',5),
                          (phaseLayout, 'left',5),
                          (phaseLayout,'right',5),
                          (self.dirField, 'left',5),
                          (self.dirField,'right',5),
                          (self.imageField, 'left',5),
                          (self.imageField,'right',5),
                          (buttonLayout,'right',5),
                          (buttonLayout,'left',5),
                          (buttonLayout,'bottom',5)],
            attachControl = [(self.sequenceField,'bottom',5,self.shotField),
                             (self.shotField,'bottom',5,self.takeField),
                             (self.takeField,'bottom',5,self.nameField),
                             (self.nameField,'bottom',5,slateLayout),
                             (slateLayout,'bottom',5,cameraLayout),
                             (cameraLayout,'bottom',5,phaseLayout),
                             (phaseLayout,'bottom',5,self.imageField),
                             (self.imageField,'bottom',5,self.dirField),
                             (self.dirField,'bottom',5,buttonLayout)],
            attachNone = [(buttonLayout,'top')] )
        """           
                
        #Set field values
        name = cmds.getAttr('TG_BM_NODE.name')
        layout_camera = cmds.getAttr('TG_BM_NODE.layout_cam')
        image = cmds.getAttr('TG_BM_NODE.mask_image_dir')
        slate = cmds.getAttr('TG_BM_NODE.slate_image_dir')
        dir = cmds.getAttr('TG_BM_NODE.dir')
        
        try:
            cmds.textFieldGrp(self.nameField,edit=True,text=name)
        except:
            pass
        try:
            cmds.textFieldButtonGrp(self.slateField,edit=True,text=slate)
        except:
            pass
        try:
            cmds.optionMenu(self.camMenu,edit=True,value=layout_camera)
        except:
            pass
        try:
            cmds.textFieldButtonGrp(self.imageField,edit=True,text=image)
        except:
            pass
        try:
            cmds.textFieldGrp(self.dirField,edit=True,text=dir)
        except:
            pass
        
        cmds.showWindow("BlastMasterWin")
    
    def tg_bmNode(self,*args):
        """
        Creates node to store persistent data in the scene,
        if it does not already exist, and add attributes
        to hold data.
        """
        #The node
        if(not cmds.objExists('TG_BM_NODE')):
            self.bmNode = cmds.group(name='TG_BM_NODE',em=True)
        cmds.select(clear=True)
            
        #Artist Name  
        if(not cmds.objExists('TG_BM_NODE.name')):
            cmds.addAttr('TG_BM_NODE',longName='name',
                         dataType='string',k=True,h=False)
            
        #16_9_overscan.png directory
        if(not cmds.objExists('TG_BM_NODE.mask_image_dir')):
            cmds.addAttr('TG_BM_NODE',longName='mask_image_dir',
                         dataType='string',k=True,h=False)
            
        #Slate.png directory
        if(not cmds.objExists('TG_BM_NODE.slate_image_dir')):
            cmds.addAttr('TG_BM_NODE',longName='slate_image_dir',
                         dataType='string',k=True,h=False)
            
        #Blast directory 
        if(not cmds.objExists('TG_BM_NODE.dir')):
            cmds.addAttr('TG_BM_NODE',longName='dir',
                         dataType='string',k=True,h=False)
        
        #Layout specific attributes         
        if(not cmds.objExists('TG_BM_NODE.layout_cam')):
            cmds.addAttr('TG_BM_NODE',longName='layout_cam',
                     dataType='string',k=True,h=False)
          
    
    def playBlast(self,*args):
        """   
        Create instance of BlastMaster, then 
        play blast based on user settings.
        If play blast is successful, Write persistent data to TG_BM_NODE
        """
        #Get the scene name and format it for display
        sceneName = ' '
        temp = cmds.file(query=True,sn=True)
        if(temp): #Not empty
            temp2 = os.path.split(temp)
            sceneName = temp2[1]
            
        #SequenceShot.Take from file name
        info = sceneName[:-3]

        #Pass GUI data as a dictionary
        guiData = {
         'info':info,
         'name':cmds.textFieldGrp(self.nameField,query=True,text=True),
         'comment':cmds.textFieldGrp(self.commentField,query=True,text=True),
         'camera':cmds.optionMenu(self.camMenu,query=True,value=True),
         'phase':cmds.optionMenu(self.phaseMenu,query=True,value=True),
         'image':cmds.textFieldButtonGrp(self.imageField,query=True,text=True),
         'slate':cmds.textFieldButtonGrp(self.slateField,query=True,text=True),
         'maya_scene':sceneName,
         'dir':cmds.textFieldGrp(self.dirField,query=True,text=True)}
                     
        blast = bm.BlastMaster()
        blast.playBlast(guiData)
            
    def addCameras(self,*args):
        """
        Add scene cameras to GUI drop-down menu 
        """
        cameras = cmds.listCameras()
        for each in cameras:
            cmds.menuItem(label=each,p=self.camMenu)
            
    def loadImageDir(self,*args):
        """ 
        opens dialog so user can browse to the overscan image.
        This will not be neccessary once standard paths for the Tools shelf 
        and icons/images are in place.
        """
        dir = cmds.fileDialog( directoryMask='*.png' )
        cmds.textFieldButtonGrp(self.imageField,edit=True,text=dir)

    def loadSlateDir(self,*args):
        """ 
        opens dialog so user can browse to the overscan image.
        This will not be neccessary once standard paths for the Tools shelf 
        and icons/images are in place.
        """
        dir = cmds.fileDialog( directoryMask='*.png' )
        cmds.textFieldButtonGrp(self.slateField,edit=True,text=dir)

        
        


        
        