################################################################################
#copyright (c) 2010, Mauricio Santos
#Name:       BlastMaster
#Author:     $Author: mauricio $
#Revised on: $Date: 2011-08-06 19:23:09 -0700 (Sat, 06 Aug 2011) $
#Added On:   6/4/2010
#SVN Ver:    $Revision: 131 $
#File: $HeadURL: file:///Users/mauricio/SVN_Repos/Maya_Tools/trunk/Tools/Rigging/General/BlastMaster.py $
#Description:
#               Generates a production standard play blast
#               HOLD --> Create copy of .ma play blasted
#               PENDING--> Call ALE Master ---> Create ALE file
#               HOLD--> Call Take Master ---> Commit take
#   History:    2010-05-28 - Initial creation
#                2010-06-12 - Finalized first release
#                2010-06-23 - Added file name to burn-in
################################################################################
__author__ = 'Mauricio Santos'
"""
Dev notes:
    Working on: 
        -Slate
            -Create slate @ frame: start time - 1
        -Timecode:
            -Start all @ 00:00:00:00 or at their TC based on frame #?
    Pending---> Call to ALE Master/Take Master pending  

"""
import maya.cmds as cmds
import maya.mel as mel
import os
import time
import EditMaster
        
class BlastMaster:
    """
        Generates a production standard play blast
        Create copy of .ma play blasted
        Call ALE Master ---> Create ALE file
        Call Take Master ---> Commit take
        Display play blast to user        
    """    
    def __init__(self,*args):
        #Create Timecode object
        self.timeCode = EditMaster.Timecode()
        
        self.currentPane = cmds.getPanel(withFocus= True)
        
        #User pane display settings
        self.userShowValues = {}
                       
        #Layout pane display settings                        
        self.layoutShowOptions = {
            'nurbsCurves':0,        
            'nurbsSurfaces':1,    
            'polymeshes':1,        
            'subdivSurfaces':0,    
            'lights':0,        
            'cameras':1,        
            'joints':0,        
            'ikHandles':0,        
            'deformers':0,        
            'dynamics':0,        
            'fluids':0,        
            'hairSystems':0,        
            'follicles':0,        
            'nCloths':0,        
            'nRigids':0,        
            'dynamicConstraints':0,    
            'locators':0,        
            'dimensions':0,        
            'pivots':0,        
            'handles':0,        
            'textures':0,        
            'strokes':0,        
            'manipulators':0,
            'cv':0,
            'hulls':0,
            'grid':0,
            'hud':1,
            'sel':0}

        #User camera display settings
        self.userCamDisplaySettings = {}
        #Layout camera display settings
        self.layoutCamDisplaySettings = {
            'displayFilmGate':0,
            'displayResolution':0,
            'displayGateMask':0,
            'displayFieldChart':0,
            'displaySafeAction':0,
            'displaySafeTitle':0,
            'displayFilmPivot':0,
            'displayFilmOrigin':0,
            'overscan':1}
        
    def playBlast(self,guiData,*args):
        """
        Store current state of pane's Show values into ---> self.userShowValues.
        Set the pane's Show values to those in the BM_SHOW_ option variables.
        Play blast with given options from GUI.
        Call ALE Master, sending relevant data.
        """     
        self.classScopeData = {}
        if(self.checkFPS()):
            if(os.path.exists(guiData['dir'])):
                #Set class variable to guiData
                self.classScopeData = guiData
                                
                #Set the output file name
                filename = '%s/%s.%s'%(guiData['dir'],
                                         guiData['info'],
                                         guiData['camera'])
                name = '%s.%s'%(guiData['info'],
                                         guiData['camera'])
  
                #Add min/max time to guiData dictionary
                startTime = cmds.playbackOptions(query=True,minTime=True)
                endTime = cmds.playbackOptions(query=True,maxTime=True)
                guiData['startTime'] = startTime
                guiData['endTime'] = endTime
                
                #Set class variable to guiData
                self.classScopeData = guiData
  
                #Set up the slate and
                #Switch off user HUD's and switch on editorial HUD's.
                #Also calls: 
                # createSlate()+storeCamDisplaySettings()+loadCamDisplayDefaults()
                self.setupCamera(guiData)
                
                cmds.select(clear=True)
                 
                #Get current OS
                currentSys = cmds.about(os=True)
                
                #Layout play blast
                if(guiData["phase"]=='Layout'):       
                    #Store pane's current Show values,
                    #Then set them to values from the Layout dictionary.
                    for each in self.layoutShowOptions.keys():
                        self.userShowValues[each]= mel.eval(
                                                    'modelEditor -q -' + each + 
                                                    ' ' + self.currentPane)
                        mel.eval('modelEditor -e -' + each + 
                                 ' ' + str(self.layoutShowOptions[each]) + 
                                 ' ' + self.currentPane)
                       
                    #Set the current panel to the user selected camera
                    mel.eval('lookThroughModelPanel %s %s'%(guiData['camera'],
                                                            self.currentPane) ) 
                    
                    #Mac
                    if('mac' in currentSys or 'linux' in currentSys):                        
                        widthHeight = (720,405)
                        showOrnaments = True
                        percent = 100
                        
                        #playblast command
                        try:
                            cmds.playblast(fmt='movie',filename=filename,
                                       widthHeight = widthHeight,
                                       startTime = startTime-1,
                                       endTime = endTime,
                                       showOrnaments = showOrnaments,
                                       percent = percent)
                        except:
                            cmds.confirmDialog( title='Error!', 
                                message='File: %s \n      already exists.'%name, 
                                button=['ok'], defaultButton='Yes', 
                                cancelButton='No', 
                                dismissString='No' )
                        
                    #Windows
                    if('nt' in currentSys or 'win64' in currentSys):
                        widthHeight = (720,405)
                        showOrnaments = True
                        percent = 100
                        
                        #playblast command
                        try:
                            cmds.playblast(fmt='movie',filename=filename,
                                       widthHeight = widthHeight,
                                       startTime = startTime-1,
                                       endTime = endTime,
                                       showOrnaments = showOrnaments,
                                       percent = percent)
                        except:
                            cmds.confirmDialog( title='Error!', 
                                message='File: %s \n      already exists.'%name, 
                                button=['ok'], defaultButton='Yes', 
                                cancelButton='No', 
                                dismissString='No' )
            
                #Store persistent data
                cmds.setAttr('TG_BM_NODE.name',guiData['name'],type='string')
                cmds.setAttr('TG_BM_NODE.dir',guiData['dir'],type='string')
                cmds.setAttr('TG_BM_NODE.mask_image_dir',guiData['image'],type='string')
                cmds.setAttr('TG_BM_NODE.slate_image_dir',guiData['slate'],type='string')
                
                #Store persistent Layout Data
                if(guiData['phase']=='Layout'):
                    cmds.setAttr('TG_BM_NODE.layout_cam',guiData['camera'],
                                 type="string")
                
                #Restore the panes view options
                self.restorePane()
                
                #Restores HUD / Camera display settings
                self.cleanUpCamera()
                
                #Generates ALE file
                self.callEditMaster()
                print ' ' #Simply to bump the HUD error's out of the cmd line display
                
            else:
                cmds.confirmDialog( title='Error!', 
                                message='Selected directory does not exist.', 
                                button=['ok'], defaultButton='Yes', 
                                cancelButton='No', 
                                dismissString='No' )
        
        else:
            cmds.confirmDialog( title='Error!', 
                                message='Frame rate not set to 24fps.', 
                                button=['ok'], defaultButton='Yes', 
                                cancelButton='No', 
                                dismissString='No' )
   
    #--- Camera/Pane setup & restore methods
    def setupCamera(self,guiData):
        """
        Setup the camera to display shot info and
        hide all cameras.
        """
        #Setup the Slate Image plane
        self.createSlate()
        
        #Create the Burn-in Image plane
        self.createBurnin()
        
        #Store user camera settings
        self.storeCamDisplaySettings()
        
        #Load default play blast camera settings
        self.loadCamDisplayDefaults()
        
        #Hide all cameras
        cameras = cmds.ls(type='camera')
        for each in cameras:
            cmds.setAttr('%s.visibility'%each,0)
            
        #Create HUDs
        self.createHUDs()

    def cleanUpCamera(self,*args):
        """
        Leave the scene the way we found it...
        Run after the playblast is complete.
        """
        #Remove the slate image plane
        self.removeSlate()
        
        #Remove burn-in image plane
        self.removeBurnin()
        
        #Remove BlastMater HUDs + Expressions and Restore user settings
        self.removeHUDs()
        
        #Restore the users display settings
        self.restoreCamDisplaySettings()
        
        #Make all cameras visible again
        temp = cmds.ls(type='camera')
        for each in temp:
            cmds.setAttr('%s.visibility'%each,1)
            
    #--- Slate methods      
    def createSlate(self,*args):
        """
        Create the slate image plane for the playblast
        """
        #Setup image plane
        #Get play blast camera shape node
        temp = cmds.listRelatives(self.classScopeData['camera'],shapes=True)
        camShape = temp[0]
        
        #Create image plane
        mel.eval('createImportedImagePlane { "%s" }  "%s" "image";'%(camShape,self.classScopeData['slate']))
                                
        temp = cmds.listConnections(camShape)
        
        #If other image planes exist, select the last one
        if len(temp) > 1:
            self.slatePlane = temp[len(temp)-1]
        else:
            self.slatePlane = temp[0]
        
        #Key the slates visibility. On for 1 frame.
        cmds.setKeyframe( self.slatePlane, attribute='alphaGain', 
                          t=( self.classScopeData['startTime'] - 1 ),v=1 )
        cmds.setKeyframe( self.slatePlane, attribute='alphaGain', 
                          t=( self.classScopeData['startTime'] ),v=0 )
  
    def removeSlate(self,*args):
        """
        Remove the slate image plane for the scene.
        """
        cmds.delete(self.slatePlane)
        
    #--- Burn-in methods      
    def createBurnin(self,*args):
        """
        Create the burn-in image plane for the playblast
        """
        #Get play blast camera shape node
        temp = cmds.listRelatives(self.classScopeData['camera'],shapes=True)
        camShape = temp[0]
        
        #Create image plane
        mel.eval('createImportedImagePlane { "%s" }  "%s" "image";'%(camShape,self.classScopeData['image']))
        temp = cmds.listConnections(camShape)
        
        #If other image planes exist, select the last one
        if len(temp) > 1:
            self.imagePlane = temp[len(temp)-1]
        else:
            self.imagePlane = temp[0]
        
        cmds.setAttr('%s.depth'%self.imagePlane,1)

        #Key the burn-ins visibility
        cmds.setKeyframe( self.imagePlane, attribute='alphaGain', 
                          t=( self.classScopeData['startTime'] - 1 ),v=0 )
        cmds.setKeyframe( self.imagePlane, attribute='alphaGain', 
                          t=( self.classScopeData['startTime'] ),v=1 )
        

    
    def removeBurnin(self,*args):
        """
        Remove the slate from the scene.
        """
        cmds.delete(self.imagePlane)
        
    #--- HUD creation/removal methods
    def createHUDs(self,*args):
        """
        Create the HUD's for playblasting
        """
        #Store user HUD settings in dictionary
        self.userHUD = {
            'selectDetails':cmds.optionVar(query='selectDetailsVisibility'),
            'objectDetails':cmds.optionVar(query='objectDetailsVisibility'),
            'polyCount':cmds.optionVar(query='polyCountVisibility'),
            'subdivDetails':cmds.optionVar(query='subdivDetailsVisibility'),
            'animationDetails':cmds.optionVar(query='animationDetailsVisibility'),
            'fbikDetails':cmds.optionVar(query='fbikDetailsVisibility'),
            'frameRate':cmds.optionVar(query='frameRateVisibility'),
            'currentFrame':cmds.optionVar(query='currentFrameVisibility'),
            'currentContainer':cmds.optionVar(query='currentContainerVisibility'),
            'cameraNames':cmds.optionVar(query='cameraNamesVisibility'),
            'focalLength':cmds.optionVar(query='focalLengthVisibility'),
            'viewAxis':cmds.optionVar(query='viewAxisVisibility'),
            'toolMessage':cmds.optionVar(query='toolMessageVisible')}

        #Set HUD for play blasting
        mel.eval('setSelectDetailsVisibility(0);')       
        mel.eval('setObjectDetailsVisibility(0);')   
        mel.eval('setSubdDetailsVisibility(0);')   
        mel.eval('setPolyCountVisibility(0);')   
        mel.eval('setAnimationDetailsVisibility(0);')   
        mel.eval('setFbikDetailsVisibility(0);')   
        mel.eval('setFrameRateVisibility(0);')   
        mel.eval('setCurrentFrameVisibility(0);')   
        mel.eval('setCurrentContainerVisibility(0);')   
        mel.eval('setCameraNamesVisibility(0);')   
        mel.eval('setFocalLengthVisibility(0);')   
        mel.eval('setViewAxisVisibility(0);')   
        mel.eval('setToolMessageVisibility(0);') 

        #Create HUDs    
        #Slate comment
        cmds.headsUpDisplay('HUDComment',rem=True)
        cmds.headsUpDisplay( 'HUDComment', 
                                label="   COMMENT: ",
                                ao=True,
                                padding=0,
                                ba='left',
                                section=6, 
                                block=4, 
                                blockSize='small',
                                dataFontSize='large',
                                c=(self.commentProc),
                                ct='playingBack' )       
            
        #File
        cmds.headsUpDisplay('HUDFile',rem=True)
        cmds.headsUpDisplay( 'HUDFile', 
                                label="   FILE: ",
                                ao=True,
                                padding=0,
                                ba='left',
                                section=5, 
                                block=2, 
                                blockSize='small',
                                dataFontSize='large',
                                c=(self.fileProc),
                                ct='playingBack' )        
        #Current Frame
        cmds.headsUpDisplay('HUDFrame',rem=True)
        cmds.headsUpDisplay( 'HUDFrame', ao=True, s=5, b=1, 
                             label=" ", blockSize="small",
                             dataFontSize='large', ba='right', dw=50, 
                             pre='currentFrame')
        
        #Duration
        cmds.headsUpDisplay('HUDDuration',rem=True)
        cmds.headsUpDisplay( 'HUDDuration', 
                                label="   DURATION: ",
                                ao=True,
                                padding=0,
                                ba='left',
                                section=6, 
                                block=6, 
                                blockSize='small',
                                dataFontSize='large',
                                c=(self.durationProc),
                                ct='playingBack' )
        
        #Camera
        cmds.headsUpDisplay('HUDCam',rem=True)
        cmds.headsUpDisplay( 'HUDCam', 
                                label="CAMERA: ",
                                ao=True,
                                padding=0,
                                ba='right',
                                section=7, 
                                block=2, 
                                blockSize='small',
                                dataFontSize='large',
                                c=(self.camProc),
                                ct='playingBack' ) 
        
        #Time code
        cmds.headsUpDisplay('HUDtc',rem=True)
        cmds.headsUpDisplay( 'HUDtc',
                                label=" ",
                                ao=True,
                                padding=0,
                                ba='right', 
                                section=7, 
                                block=1, 
                                blockSize='small',
                                dataFontSize='large',
                                c=self.tcProc,
                                ct='playingBack' )

        #Name
        cmds.headsUpDisplay('HUDName',rem=True)
        cmds.headsUpDisplay( 'HUDName',
                                label=" NAME: ",
                                ao=True,
                                padding=0,
                                ba='right', 
                                section=8, 
                                block=1, 
                                blockSize='small',
                                dataFontSize='large',
                                c=self.nameProc,
                                ct='playingBack' )
        
        #Date
        cmds.headsUpDisplay('HUDDate',rem=True)
        cmds.headsUpDisplay( 'HUDDate',
                                label=" DATE (m/d/y): ",
                                ao=True,
                                padding=0,
                                ba='right', 
                                section=8, 
                                block=0, 
                                blockSize='small',
                                dataFontSize='large',
                                c=self.dateProc,
                                ct='playingBack' )   

        #Create Timecode HUD refresh expression
        cmds.expression(n="TC_HUDRefreshExp",
                        s="headsUpDisplay -refresh HUDtc;",
                        ae=True)  
        
        #Slate HUD vis expressions 
        #Slate Length HUD vis expression string
        slateStr = 'if(`currentTime -query`== %i)\n'%(self.classScopeData['startTime']-1)
        slateStr = slateStr + '{ headsUpDisplay -edit -visible 1 HUDDuration;}\n' 
        slateStr = slateStr + 'else{ headsUpDisplay -edit -visible 0 HUDDuration;}'
        
        cmds.expression(n="Duration_HUDVisExp",
                        s=slateStr,
                        ae=True)  
        
        #Slate Comment HUD vis expression string
        commentStr = 'if(`currentTime -query`== %i)\n'%(self.classScopeData['startTime']-1)
        commentStr = commentStr + '{ headsUpDisplay -edit -visible 1 HUDComment;}\n' 
        commentStr = commentStr + 'else{ headsUpDisplay -edit -visible 0 HUDComment;}'
        
        cmds.expression(n="Comment_HUDVisExp",
                        s=commentStr,
                        ae=True) 
   
    def removeHUDs(self,*args):
        """
        Remove BlastMaster HUDs / Restore Users'
        """
        #Delete the HUD's 
        cmds.headsUpDisplay('HUDComment',rem=True)
        cmds.headsUpDisplay('HUDFile',rem=True)
        cmds.headsUpDisplay('HUDCam',rem=True)
        cmds.headsUpDisplay('HUDDuration',rem=True)
        cmds.headsUpDisplay('HUDFrame',rem=True)
        cmds.headsUpDisplay('HUDtc',rem=True)
        cmds.headsUpDisplay('HUDName',rem=True)
        cmds.headsUpDisplay('HUDDate',rem=True)
        
        #Reset HUD to user settings
        mel.eval('setSelectDetailsVisibility(%i);'%self.userHUD['selectDetails'])       
        mel.eval('setObjectDetailsVisibility(%i);'%self.userHUD['objectDetails'])   
        mel.eval('setSubdDetailsVisibility(%i);'%self.userHUD['subdivDetails'])   
        mel.eval('setPolyCountVisibility(%i);'%self.userHUD['polyCount'])   
        mel.eval('setAnimationDetailsVisibility(%i);'%self.userHUD['animationDetails'])   
        mel.eval('setFbikDetailsVisibility(%i);'%self.userHUD['fbikDetails'])   
        mel.eval('setFrameRateVisibility(%i);'%self.userHUD['frameRate'])   
        mel.eval('setCurrentFrameVisibility(%i);'%self.userHUD['currentFrame'])   
        mel.eval('setCurrentContainerVisibility(%i);'%self.userHUD['currentContainer'])   
        mel.eval('setCameraNamesVisibility(%i);'%self.userHUD['cameraNames'])   
        mel.eval('setFocalLengthVisibility(%i);'%self.userHUD['focalLength'])   
        mel.eval('setViewAxisVisibility(%i);'%self.userHUD['viewAxis'])   
        mel.eval('setToolMessageVisibility(%i);'%self.userHUD['toolMessage'])
        
        #Delete the HUD expressions
        cmds.delete("TC_HUDRefreshExp")
        cmds.delete("Duration_HUDVisExp")
        cmds.delete("Comment_HUDVisExp")
        
    #--- Camera Display methods    
    def storeCamDisplaySettings(self,*args):
        """
        Store the user camera display settings
        """
        cam = self.classScopeData['camera']
        camShape = cmds.listRelatives(cam,shapes=True)
        
        for attr in self.layoutCamDisplaySettings.keys():
            self.userCamDisplaySettings[attr] = \
                cmds.getAttr('%s.%s'%(camShape[0],attr))
    
    def loadCamDisplayDefaults(self,*args):
        """
        Set the camera to the default display options
        for an editorial layout play blast
        """
        cam = self.classScopeData['camera']
        camShape = cmds.listRelatives(cam,shapes=True)

        for attr in self.layoutCamDisplaySettings.keys():
                value = self.layoutCamDisplaySettings[attr]
                cmds.setAttr('%s.%s'%(camShape[0],attr),value)
    
    def restoreCamDisplaySettings(self,*args):
        """
        Restore user camera display settings
        """
        cam = self.classScopeData['camera']
        camShape = cmds.listRelatives(cam,shapes=True)
        
        for attr in self.userCamDisplaySettings.keys():
                value = self.userCamDisplaySettings[attr]
                cmds.setAttr('%s.%s'%(camShape[0],attr),value)
                
        #Clear list
        self.userCamDisplaySettings = {}
        
    #--- Hud methods: Used to generate HUD data
    def commentProc(self,*args):
        return self.classScopeData['comment'] 
    
    def fileProc(self,*args):
        return self.classScopeData['maya_scene'] 
    
    def durationProc(self,*args):
        startVal = self.classScopeData['startTime']
        endVal = self.classScopeData['endTime']
        
        runtime = endVal - startVal
        
        self.timeCode.totalFrames = runtime
        
        print startVal
        print endVal
        print runtime
        return self.timeCode.timecode
    
    def tcProc(self,*args):
        """
        Return the absolute time code using Edit Master
        """
        currentFrame = cmds.currentTime( query=True )
        self.timeCode.totalFrames = currentFrame
        return self.timeCode.timecode
    
    def camProc(self,*args):
        return self.classScopeData['camera']   
    
    def nameProc(self,*args):
        return self.classScopeData['name']
    
    def dateProc(self,*args):
        date = time.localtime()
        date = str(date[1]) + '/' + str(date[2]) + '/' + str(date[0])
        return date

    #--- General helper methods
    def restorePane(self,*args):
        """
        Restore current pane's Show values from before play blast.
        """         
        for each in self.userShowValues.keys():    
            mel.eval('modelEditor -e -' + each + ' ' + 
                     str(self.userShowValues[each]) + ' ' + self.currentPane)
       
        #Clear list so it doesn't grow
        self.userShowValues = []
    
    def checkFPS(self,*args):
        """
        Check that the current fps is 24
        film == 24fps
        """
        fps = cmds.currentUnit(query=True,time=True)
        if('film' in fps):
            return 1
        else:
            return 0
        
    #--- Edit Master: Create ALE file method
    def callEditMaster(self,*args):
        """
        Calls Edit Master:
            -Write ALE file
        """
        pass

        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
    