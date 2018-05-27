import pymel.core as pm
import maya.cmds as cmds
import maya.mel as mel
import os
import sys
import shutil

import os
import pdb

class Exporter(object):
    
    def __init__(self):
        '''
        Export animation.
        '''
        self.noSelError = 'Nothing selected! Please select the MAINC control of a rig.'
        
        win = 'ExportRigsWin'
        if pm.window(win, exists=1):
            pm.deleteUI(win, window=1)
        
        pm.window(win, title='Export Animation', rtf=1)
        pm.columnLayout(adj=1)
        pm.text('Select rig "MAINC" control.')
        self.fNameFld = pm.textFieldGrp(l='Name for export file', text='anim_01')
        pm.button(l='Export Anim', c=self.exportSelected)
        
        pm.showWindow(win)
        
        
    def exportSelected(self, *args):
        '''Export selected rig'''
        # Get information
        fName = pm.textFieldGrp(self.fNameFld, q=1, text=1)
        animFile = pm.cmds.file(q=1, sn=1)
        exportFile = os.path.dirname(animFile) + os.path.sep + fName + '.fbx'
        
        if os.path.exists(exportFile):
            answer = pm.confirmDialog( title='FBX File exists', message='Overwrite?', 
                              button=['Yes','No'], 
                              defaultButton='Yes', 
                              cancelButton='No', 
                              dismissString='No' )
            if answer == 'No':
                print 'Export canceled.'
                return
        
        try:
            root = pm.ls(sl=1)[0]
        except:
            raise Exception(self.noSelError)
        pm.select(root.replace('MAINCtrl', 'MAINSHJnt'), r=1)
        root = pm.ls(sl=1)[0]
        
        # Import reference
        self._importRef(sel=root)
        
        # Bake animation on SH
        self._bakeAnim( root=root.name() )
        
        # Delete constraint
        self._delConstraints(jnt=root)
        
        # Move out of rig heirarchy
        pm.parent(root, w=1)
        
        # Export selected heirarchy
        self._fbxExport(selection=root, 
                        fileName=exportFile)     
        
        print "Export complete.\n\n"

            
    def _delConstraints(self, jnt=None):
        pm.select(jnt, hi=1, r=1)
        sel = pm.ls(sl=1)
        for each in sel:
            try:
                children = pm.listRelatives(each)
            except:
                pass
            for child in children:
                if 'Constraint' in str(type(child)):
                    try:
                        pm.delete(child)
                    except:
                        pass

                      
    def _bakeAnim(self, root):
        '''
        Given root:
        - Bake the heirarchy animation data
        - Reset timeline to 1 if wasn't already set to 1
        '''
        print 'Starting: bakeAnim()...'
        # Getting time range from scene
        startFrame = int( pm.playbackOptions(q=1, min=1) )
        endFrame = int( pm.playbackOptions(q=1, max=1) )

        pm.select(root, hi=1, r=1)

        # Set timeline to start at frame 1
        if startFrame != 1:
            if startFrame < 1:
                tChange = (-(startFrame))+1
            elif startFrame > 1:
                tChange = (-(startFrame-1))
        
            pm.keyframe(e=1, time=(startFrame, endFrame), relative=1, timeChange=tChange)
            pm.playbackOptions(e=1, min=1, max=endFrame+tChange )
            
        pm.bakeResults(root, 
                       t=(startFrame, endFrame), 
                       simulation=True, hi='below' )
        
        print 'bakeAnim(): Baked anim onto %s' % root
        print 'bakeAnim(): Range baked: %s - %s' % (startFrame, endFrame) 
        print 'End: bakeAnim()'
        
        
    def _importRef(self, sel=None):
        ''' Given a selected object, import reference '''
        # only first object selected will be considered
        print 'Starting: importRef()...'
        if not sel:
            raise Exception(self.noSelError)
        
        # Finding name of the referenced node
        try:
            refNode = cmds.referenceQuery( sel.name(), referenceNode = True )
        except:
            refNode = None
            
        if refNode:
            # Find out if it is a reference of a reference
            topRef = cmds.referenceQuery( sel.name(), referenceNode=True, tr=True  )
            
            if refNode != topRef:
                print 'importRef(): %s is sub-referenced.' % sel
                fileNameTN = cmds.referenceQuery( topRef,filename = True  )
                fileNameN = cmds.referenceQuery( refNode, filename = True )
                
                cmds.file( fileNameTN , importReference = 1 )
                cmds.file( fileNameN, importReference = 1 )
                
            else:
                fileNameN = cmds.referenceQuery( refNode, filename = True )
                cmds.file( fileNameN, importReference = 1 )
                
        else: 
            cmds.warning('This is Not a referenced object!' )
            print 'refNode: %s' % refNode
            print 'sel: %s' % sel
            raise Exception( '%s is not a referenced object.' % sel )

        print 'End: importRef().'
        
        
    def _fbxExport(self, selection=None, 
                  fileName=None):
        '''
        Selection: Names of objects to export
        rig/asset/anim/camera: Determine FBX options
        '''
        try:
            pm.parent(selection, w=True)
        except:
            pm.select(selection, r=1)
        
        fileN = fileName

        startFrame = int( cmds.playbackOptions(q=1, min=1) )
        endFrame = int( cmds.playbackOptions(q=1, max=1) )        
        
        # FBX OPTIONS
        # Geometry
        mel.eval("FBXExportSmoothingGroups -v true")
        mel.eval("FBXExportHardEdges -v false")
        mel.eval("FBXExportTangents -v false")
        #mel.eval("FBXExportSmoothMesh -v true")
        mel.eval("FBXExportInstances -v false")
        #mel.eval("FBXExportReferencedContainersContent -v false")
              
        mel.eval("FBXExportApplyConstantKeyReducer -v true")
        mel.eval("FBXExportBakeResampleAnimation -v true")
        mel.eval("FBXExportBakeComplexAnimation -v true")
        mel.eval("FBXExportBakeComplexStart -v "+str(startFrame))
        mel.eval("FBXExportBakeComplexEnd -v "+str(endFrame))
        mel.eval("FBXExportBakeComplexStep -v 1")
        mel.eval("FBXExportUseSceneName -v false")
        mel.eval("FBXExportQuaternion -v euler")
            
        mel.eval("FBXExportCameras -v false")
            
        # Constraints
        mel.eval("FBXExportConstraints -v false")
        # Lights
        mel.eval("FBXExportLights -v false")
        # Embed Media
        mel.eval("FBXExportEmbeddedTextures -v false")
        # Connections
        mel.eval("FBXExportInputConnections -v false")
        # Axis Conversion
        mel.eval("FBXExportUpAxis y")
        # version
        mel.eval("FBXExportFileVersion FBX201100")
        # Type
        mel.eval("FBXExportInAscii -v true")
        
        # Export!
        mel.eval('FBXExport -f "'+ fileN +'" -exportFormat "fbx" -s;')
        print '\n\nExported: %s' % fileN
        
if __name__ == '__main__':
    Exporter()